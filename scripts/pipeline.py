#!/usr/bin/env python3
"""Check a declared Blender asset graph and current evidence; Python standard library only.

validate MANIFEST [--require-ready] checks the plan and all claimed verified nodes.
gate MANIFEST --node ID checks dependencies before building that node.
next MANIFEST lists buildable nodes, including stale nodes that need rebuilding.
preflight MANIFEST [--node ID] checks declared worst-case topology before Blender evaluation.
This never builds files, changes statuses, or certifies visual/semantic truth.
"""

import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.dont_write_bytecode = True  # Keep bundled script runs from writing cache files into the skill.
from geometry_cost import BUDGET_METRICS, assess, control_cases

KINDS = {"part": 0, "assembly": 1, "module": 2, "scene": 3}
STATUSES = {"planned", "building", "verified"}
GEOMETRY_TYPES = {"MESH", "CURVE", "SURFACE", "FONT", "META", "VOLUME", "POINTCLOUD", "CURVES", "GREASEPENCIL"}


class Invalid(ValueError):
    pass


def need(condition, message):
    if not condition:
        raise Invalid(message)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def valid_bounds(dimensions, contract):
    axes = contract.get("bounds_axes", ["X", "Y", "Z"])
    return (isinstance(dimensions, list) and len(dimensions) == 3 and
            all(number(x) and x >= 0 for x in dimensions) and
            all(dimensions["XYZ".index(axis)] > 0 for axis in axes))


def digest(path):
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def local_path(root, value):
    need(nonempty(value), "Expected a project-relative path")
    need("\\" not in value and not re.match(r"^[A-Za-z]:", value), f"Non-portable path: {value}")
    part = Path(value)
    need(not part.is_absolute() and ".." not in part.parts, f"Path escapes project: {value}")
    result = (root / part).resolve()
    need(result.is_relative_to(root), f"Path escapes project via symlink: {value}")
    return result


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_manifest(path):
    root = Path(path).resolve().parent
    data = read_json(path)
    need(isinstance(data, dict) and data.get("schema_version") == 1, "Expected manifest schema_version 1")
    project = data.get("project")
    need(isinstance(project, dict), "Missing project object")
    need(project.get("units") == "meters" and project.get("up_axis") == "Z", "Authoring contract must use meters/Z-up")
    entries = data.get("nodes")
    need(isinstance(entries, list) and entries, "nodes must be a nonempty list")
    nodes, paths, roots = {}, set(), set()
    for node in entries:
        need(isinstance(node, dict), "Each node must be an object")
        node_id = node.get("id")
        need(nonempty(node_id) and re.fullmatch(r"[a-z][a-z0-9_-]*", node_id), f"Invalid node ID: {node_id}")
        need(node_id not in nodes, f"Duplicate node ID: {node_id}")
        need(node.get("kind") in KINDS, f"{node_id}: invalid kind")
        need(node.get("status") in STATUSES, f"{node_id}: invalid status")
        file = local_path(root, node.get("file"))
        need(file.suffix == ".blend" and file not in paths, f"{node_id}: require one unique .blend source file")
        collection = node.get("root_collection")
        need(nonempty(collection) and collection not in roots, f"{node_id}: require a unique public root_collection")
        deps = node.get("deps")
        need(isinstance(deps, list) and all(nonempty(x) for x in deps), f"{node_id}: deps must be an ID list")
        need(len(set(deps)) == len(deps), f"{node_id}: duplicate dependency")
        need(node["kind"] == "part" or deps, f"{node_id}: a parent needs at least one child; otherwise make it a part")
        method = node.get("method", {})
        need(isinstance(method, dict) and all(nonempty(method.get(k)) for k in ("selected", "why", "alternative")),
             f"{node_id}: record selected method, why, and alternative")
        contract = node.get("contract", {})
        need(isinstance(contract, dict) and nonempty(contract.get("pivot")), f"{node_id}: describe the pivot contract")
        axes = contract.get("bounds_axes", ["X", "Y", "Z"])
        need(isinstance(axes, list) and axes and all(isinstance(x, str) and x in {"X", "Y", "Z"} for x in axes) and
             len(axes) == len(set(axes)), f"{node_id}: bounds_axes must list unique nonempty X/Y/Z axes")
        if "dimensions_m" in contract:
            dims = contract["dimensions_m"]
            need(valid_bounds(dims, contract), f"{node_id}: invalid dimensions_m")
            need(number(contract.get("tolerance_m")) and contract["tolerance_m"] >= 0, f"{node_id}: missing dimension tolerance_m")
        sockets = contract.get("sockets", [])
        need(isinstance(sockets, list) and all(nonempty(x) for x in sockets), f"{node_id}: invalid sockets list")
        budget = node.get("budget", {})
        need(isinstance(budget, dict) and budget, f"{node_id}: record at least one provisional budget")
        need(set(budget) <= set(BUDGET_METRICS), f"{node_id}: unknown budget key")
        need(all(isinstance(x, int) and not isinstance(x, bool) and x > 0 for x in budget.values()), f"{node_id}: budget limits must be positive integers")
        need(isinstance(node.get("procedural", False), bool), f"{node_id}: procedural must be a boolean")
        if node.get("procedural"):
            assess(node)
        else:
            need("complexity" not in node, f"{node_id}: complexity requires procedural=true")
        inline = node.get("inline_geometry", [])
        need(isinstance(inline, list) and all(isinstance(x, dict) and nonempty(x.get("name")) and nonempty(x.get("reason")) for x in inline),
             f"{node_id}: inline_geometry needs exact object names and reasons")
        need(isinstance(node.get("evidence", {}), dict), f"{node_id}: evidence must be an object")
        paths.add(file)
        roots.add(collection)
        nodes[node_id] = node

    for node_id, node in nodes.items():
        for dep in node["deps"]:
            need(dep in nodes, f"{node_id}: unknown dependency {dep}")
            need(dep != node_id, f"{node_id}: self dependency")
            need(KINDS[nodes[dep]["kind"]] <= KINDS[node["kind"]] and nodes[dep]["kind"] != "scene",
                 f"{node_id}: dependency on a higher level or a scene: {dep}")
    visiting, done, order = set(), set(), []

    def visit(node_id):
        need(node_id not in visiting, f"Dependency cycle at {node_id}")
        if node_id in done:
            return
        visiting.add(node_id)
        for dep in nodes[node_id]["deps"]:
            visit(dep)
        visiting.remove(node_id)
        done.add(node_id)
        order.append(node_id)

    for node_id in nodes:
        visit(node_id)

    deliverables = project.get("deliverables")
    need(isinstance(deliverables, list) and deliverables and all(x in nodes for x in deliverables), "project.deliverables must name existing nodes")
    reachable = set()

    def reach(node_id):
        if node_id not in reachable:
            reachable.add(node_id)
            for dep in nodes[node_id]["deps"]:
                reach(dep)

    for node_id in deliverables:
        reach(node_id)
    for node_id, node in nodes.items():
        need(node_id in reachable or nonempty(node.get("library_only_reason")), f"{node_id}: orphan asset; connect it or record library_only_reason")

    requirements = data.get("requirements")
    need(isinstance(requirements, list) and requirements, "Map requested requirements explicitly")
    requirement_ids, check_ids, required_checks = set(), set(), {x: set() for x in nodes}
    for req in requirements:
        need(isinstance(req, dict) and nonempty(req.get("id")) and nonempty(req.get("description")), "Invalid requirement")
        need(req["id"] not in requirement_ids, f"Duplicate requirement {req['id']}")
        requirement_ids.add(req["id"])
        mapped = req.get("nodes")
        acceptance = req.get("acceptance")
        need(isinstance(mapped, list) and all(x in nodes for x in mapped), f"{req['id']}: invalid requirement node mapping")
        if nonempty(req.get("excluded_reason")):
            need(mapped == [] and acceptance == [], f"{req['id']}: excluded requirements must have empty nodes/acceptance")
            continue
        need(mapped and isinstance(acceptance, list) and acceptance, f"{req['id']}: requirement has no assets/checks")
        for check in acceptance:
            need(isinstance(check, dict) and nonempty(check.get("id")) and nonempty(check.get("description")), f"{req['id']}: invalid acceptance check")
            need(check.get("node") in mapped, f"{req['id']}: check node must be in requirement.nodes")
            need(check["id"] not in check_ids, f"Duplicate acceptance check {check['id']}")
            check_ids.add(check["id"])
            required_checks[check["node"]].add(check["id"])
    return root, data, nodes, order, required_checks


def inspect_evidence(root, project, node, nodes, required_checks, hashes):
    node_id = node["id"]
    reasons = []

    def check(condition, message):
        if not condition:
            reasons.append(message)

    try:
        file = local_path(root, node["file"])
        check(file.is_file(), "source file missing")
        if not file.is_file():
            return reasons
        current_hash = hashes.setdefault(file, digest(file)) if file not in hashes else hashes[file]
        evidence = node.get("evidence", {})
        audit_path = local_path(root, evidence.get("audit"))
        report = read_json(audit_path)
        audit_hash = digest(audit_path)
        need(isinstance(report, dict), "audit must be an object")
        check(report.get("schema_version") == 1 and report.get("node_id") == node_id, "audit identity mismatch")
        check(report.get("source_sha256") == current_hash, "source changed since audit")
        check(report.get("root_collection") == node["root_collection"] and report.get("root_exists") is True, "public root missing/mismatched")
        check(report.get("source_saved") is True, "audit captured an unsaved or dirty Blender file")
        check(report.get("root_in_active_scene") is True, "public root not present in audited scene")
        check(report.get("errors") == [], "Blender audit has errors or absent error list")
        check(report.get("missing_files") == [], "missing external files or absent file check")
        check(nonempty(report.get("blender_version")), "audit has no Blender runtime version")
        metrics = report.get("metrics", {})
        need(isinstance(metrics, dict), "missing audit metrics")
        for key, limit in node["budget"].items():
            metric = BUDGET_METRICS[key]
            value = metrics.get(metric)
            check(number(value) and 0 <= value <= limit, f"missing/invalid/over-budget {metric}")
        contract = node["contract"]
        dims = metrics.get("dimensions_m")
        check(valid_bounds(dims, contract), "empty or invalid evaluated bounds")
        check(report.get("unit_scale") == 1.0 and report.get("unit_system") == "METRIC", "audit units differ from meter contract")
        if "dimensions_m" in contract and isinstance(dims, list) and len(dims) == 3 and all(number(x) for x in dims):
            check(all(abs(a - b) <= contract["tolerance_m"] for a, b in zip(dims, contract["dimensions_m"])), "dimensions outside contract tolerance")
        socket_names = report.get("sockets", {})
        check(isinstance(socket_names, dict) and all(x in socket_names for x in contract.get("sockets", [])), "declared attachment socket missing")
        local_geometry = report.get("local_geometry")
        need(isinstance(local_geometry, list), "audit has no local_geometry list")
        if node["kind"] != "part":
            allowed = {x["name"] for x in node.get("inline_geometry", [])}
            check(set(local_geometry) <= allowed, "parent contains undeclared owned geometry: " + ", ".join(sorted(set(local_geometry) - allowed)))
        libraries = report.get("libraries")
        references = report.get("references")
        need(isinstance(libraries, list) and isinstance(references, list), "audit has no library/reference lists")
        for lib in libraries:
            need(isinstance(lib, dict), "invalid library report entry")
            path = Path(lib.get("path", "")).resolve()
            check(path.is_file() and lib.get("sha256") == (hashes.setdefault(path, digest(path)) if path.is_file() and path not in hashes else hashes.get(path)),
                  "linked source changed/missing: " + str(path))
            if project.get("relative_libraries", True):
                check(str(lib.get("stored_path", "")).startswith("//"), "absolute linked-library path: " + str(path))
        for dep in node["deps"]:
            dep_file = local_path(root, nodes[dep]["file"])
            check(any(isinstance(x, dict) and x.get("path") and Path(x["path"]).resolve() == dep_file for x in libraries),
                  "child source absent from library audit: " + dep)
            check(any(isinstance(x, dict) and x.get("path") and Path(x["path"]).resolve() == dep_file and x.get("collection") == nodes[dep]["root_collection"] for x in references),
                  "child root is not referenced inside parent: " + dep)
        resources = report.get("resources")
        need(isinstance(resources, list), "audit has no external resources list")
        for resource in resources:
            need(isinstance(resource, dict) and nonempty(resource.get("path")), "invalid external resource")
            path = Path(resource["path"]).resolve()
            check(path.is_file() and resource.get("sha256") == (digest(path) if path.is_file() else None),
                  "external resource changed/missing: " + str(path))
        visuals = evidence.get("visuals")
        need(isinstance(visuals, list) and visuals, "no inspected visual evidence")
        for item in visuals:
            need(isinstance(item, dict), "invalid visual evidence entry")
            path = local_path(root, item.get("file"))
            check(path.is_file() and item.get("sha256") == (digest(path) if path.is_file() else None), "visual missing or changed")
            check(item.get("source_sha256") == current_hash and nonempty(item.get("review")), "visual review missing/stale")
            check(item.get("audit_sha256") == audit_hash, "visual review belongs to an older audit/dependency state")
        checks = evidence.get("checks", [])
        need(isinstance(checks, list), "checks must be a list")
        passed = set()
        for item in checks:
            need(isinstance(item, dict), "invalid check entry")
            check(item.get("passed") is True and item.get("source_sha256") == current_hash and item.get("audit_sha256") == audit_hash and nonempty(item.get("observed")), "failed/stale/undocumented acceptance check")
            if item.get("passed") is True and item.get("source_sha256") == current_hash and item.get("audit_sha256") == audit_hash and nonempty(item.get("observed")):
                passed.add(item.get("id"))
        check(required_checks <= passed, "missing required checks: " + ", ".join(sorted(required_checks - passed)))
        divergence = report.get("render_divergence", [])
        need(isinstance(divergence, list), "invalid render_divergence list")
        if divergence:
            production = read_json(local_path(root, evidence.get("production_audit")))
            need(isinstance(production, dict), "invalid production audit")
            check(production.get("evaluation_mode") == "RENDER", "production audit is not from a render dependency graph")
            check(production.get("schema_version") == 1 and production.get("node_id") == node_id and production.get("source_sha256") == current_hash,
                  "production audit identity/source mismatch")
            check(production.get("root_collection") == node["root_collection"] and production.get("root_exists") is True,
                  "production audit public root mismatch")
            check(production.get("source_saved") is True and production.get("root_in_active_scene") is True,
                  "production audit unsaved source or inactive public root")
            check(production.get("unit_scale") == 1.0 and production.get("unit_system") == "METRIC" and
                  nonempty(production.get("blender_version")) and production.get("blender_version") == report.get("blender_version"),
                  "production audit runtime/units missing or different")
            check(production.get("errors") == [] and production.get("missing_files") == [], "production audit failed")
            check(production.get("libraries") == libraries and production.get("resources") == resources,
                  "production dependency/resource state differs from current audit")
            production_metrics = production.get("metrics")
            need(isinstance(production_metrics, dict), "missing production metrics")
            production_dims = production_metrics.get("dimensions_m")
            valid_production_dims = valid_bounds(production_dims, contract)
            check(valid_production_dims, "empty or invalid production bounds")
            if "dimensions_m" in contract and valid_production_dims:
                check(all(abs(a - b) <= contract["tolerance_m"] for a, b in zip(production_dims, contract["dimensions_m"])),
                      "production dimensions outside contract tolerance")
            for key, limit in node["budget"].items():
                metric = BUDGET_METRICS[key]
                value = production_metrics.get(metric)
                check(number(value) and 0 <= value <= limit, "missing/over-budget production " + metric)
        if node.get("procedural"):
            entry = evidence.get("complexity_tests", {})
            test_path = local_path(root, entry.get("file"))
            check(entry.get("sha256") == digest(test_path), "parameter test file changed")
            tests = read_json(test_path)
            need(isinstance(tests, dict), "invalid parameter test report")
            check(tests.get("schema_version") == 1 and tests.get("node_id") == node_id and
                  tests.get("source_sha256") == current_hash and tests.get("audit_sha256") == audit_hash,
                  "parameter test identity/source/audit state mismatch")
            expected = control_cases(node)
            required_cases = {name: (controls, "VIEWPORT") for name, controls in expected.items()}
            if divergence:
                required_cases["render_maximum"] = (expected["maximum"], "RENDER")
            observed_cases = tests.get("cases")
            need(isinstance(observed_cases, list) and all(isinstance(x, dict) for x in observed_cases), "invalid parameter cases")
            names = [x.get("name") for x in observed_cases]
            need(all(nonempty(x) for x in names) and len(names) == len(set(names)), "duplicate/invalid parameter case names")
            observed_cases = {x["name"]: x for x in observed_cases}
            for name, (controls, mode) in required_cases.items():
                case = observed_cases.get(name, {})
                actual = case.get("actual_controls")
                check(isinstance(actual, dict) and actual == controls and all(number(x) for x in actual.values()),
                      "missing/wrong control readback for " + name)
                check(case.get("evaluation_mode") == mode, "wrong evaluation mode for " + name)
                check(case.get("errors") == [] and case.get("behavior_passed") is True and nonempty(case.get("observed")),
                      "missing/failed geometry behavior check for " + name)
                for key, limit in node["budget"].items():
                    metric = BUDGET_METRICS[key]
                    value = case.get("metrics", {}).get(metric)
                    check(number(value) and 0 <= value <= limit, "missing/over-budget " + name + " " + metric)
    except (Invalid, OSError, ValueError, TypeError, KeyError, AttributeError) as error:
        reasons.append(str(error))
    return reasons


def evaluate(root, data, nodes, order, required_checks):
    ready, reasons, hashes = {}, {}, {}
    for node_id in order:
        node = nodes[node_id]
        current = [] if node["status"] == "verified" else ["status is " + node["status"]]
        if node["status"] == "verified":
            current += inspect_evidence(root, data["project"], node, nodes, required_checks[node_id], hashes)
        current += ["dependency not ready: " + dep for dep in node["deps"] if not ready[dep]]
        reasons[node_id], ready[node_id] = current, not current
    return ready, reasons


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["validate", "gate", "next", "preflight"])
    parser.add_argument("manifest")
    parser.add_argument("--node")
    parser.add_argument("--require-ready", action="store_true")
    args = parser.parse_args()
    try:
        root, data, nodes, order, checks = load_manifest(args.manifest)
        if args.command == "preflight":
            need(args.node is None or args.node in nodes, "unknown --node")
            selected = [nodes[args.node]] if args.node else list(nodes.values())
            result = {"ok": True, "topology_plans": [assess(node) for node in selected if node.get("procedural")],
                      "note": "Estimates only; builders must clamp controls and perform actual evaluated checks"}
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0
        ready, reasons = evaluate(root, data, nodes, order, checks)
        errors = []
        if args.command == "gate":
            need(args.node in nodes, "gate needs --node with an existing asset ID")
            errors = [f"{dep}: {', '.join(reasons[dep])}" for dep in nodes[args.node]["deps"] if not ready[dep]]
        elif args.command == "validate":
            errors = [f"{node_id}: {', '.join(reasons[node_id])}" for node_id in order
                      if not ready[node_id] and (args.require_ready or nodes[node_id]["status"] == "verified")]
        candidates = [x for x in order if not ready[x] and all(ready[d] for d in nodes[x]["deps"])]
        result = {"ok": not errors, "errors": errors, "ready_to_build": candidates,
                  "verified": [x for x in order if ready[x]],
                  "blocked": {x: reasons[x] for x in order if not ready[x]}}
        if args.command == "next" and not candidates and not all(ready.values()):
            result["ok"] = False
            result["errors"].append("No buildable assets; inspect blocked dependencies")
    except (Invalid, OSError, ValueError, TypeError, KeyError, AttributeError) as error:
        result = {"ok": False, "errors": [str(error)]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
