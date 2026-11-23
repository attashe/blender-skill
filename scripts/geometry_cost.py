#!/usr/bin/env python3
"""Estimate bounded topology before Blender evaluation; no Blender or mesh allocation.

Input is one node JSON with procedural=true, complexity.controls, complexity.model and budget.
Models describe explicit simple topology, not arbitrary GN graphs. Estimates must be verified
in Blender; declaring a bound does not clamp a Blender socket by itself.
"""

import argparse
import json
from pathlib import Path


BUDGET_METRICS = {
    "max_expanded_triangles": "expanded_triangles",
    "max_expanded_vertices": "expanded_vertices",
    "max_instances": "instances",
    "max_evaluated_objects": "evaluated_objects",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def integer(value):
    return isinstance(value, int) and not isinstance(value, bool)


def control_cases(node):
    controls = node.get("complexity", {}).get("controls")
    require(isinstance(controls, dict) and controls, "procedural node needs complexity.controls")
    cases = {"minimum": {}, "nominal": {}, "maximum": {}}
    for name, limits in controls.items():
        require(isinstance(name, str) and name and isinstance(limits, dict), "invalid topology control")
        values = [limits.get(x) for x in ("min", "value", "max")]
        require(all(integer(x) for x in values) and 0 <= values[0] <= values[1] <= values[2],
                f"{name}: require integer 0 <= min <= value <= max")
        for case, value in zip(cases, values):
            cases[case][name] = value
    return cases


def estimate(model, controls, depth=0):
    require(isinstance(model, dict) and depth < 24, "invalid or excessively nested topology model")

    def value(key, minimum=0):
        result = model.get(key)
        if isinstance(result, str):
            require(result in controls, f"unknown topology control {result}")
            result = controls[result]
        require(integer(result) and result >= minimum, f"{key}: invalid topology count")
        return result

    def flag(key, default=False):
        result = model.get(key, default)
        require(isinstance(result, bool), f"{key}: require a boolean")
        return result

    kind = model.get("type")
    if kind == "mesh":
        vertices, triangles, instances = value("vertices"), value("triangles"), 0
    elif kind == "sweep":
        path_closed, profile_closed = flag("path_cyclic"), flag("profile_cyclic", True)
        path, profile = value("path_points", 3 if path_closed else 2), value("profile_points", 3 if profile_closed else 2)
        caps = flag("caps")
        require(not caps or profile_closed and not path_closed, "caps require an open path and closed simple profile")
        vertices = path * profile
        triangles = 2 * (path if path_closed else path - 1) * (profile if profile_closed else profile - 1)
        triangles += 2 * (profile - 2) if caps else 0
        instances = 0
    elif kind == "grid":
        u, v = value("u_points", 2), value("v_points", 2)
        vertices, triangles, instances = u * v, 2 * (u - 1) * (v - 1), 0
    elif kind == "subdivide_quads":
        faces, levels = value("base_quads", 1), value("levels")
        require(levels <= 16, "subdivision level >16 rejected before exponent/evaluation")
        faces *= 4 ** levels
        vertices, triangles, instances = 4 * faces, 2 * faces, 0
    elif kind == "repeat":
        count = value("count")
        child = estimate(model.get("geometry"), controls, depth + 1)
        vertices, triangles = count * child["expanded_vertices"], count * child["expanded_triangles"]
        instances = count * (1 + child["instances"])
    elif kind == "join":
        children = model.get("geometry")
        require(isinstance(children, list) and children, "join needs geometry list")
        estimates = [estimate(x, controls, depth + 1) for x in children]
        vertices, triangles, instances = (sum(x[key] for x in estimates) for key in
                                          ("expanded_vertices", "expanded_triangles", "instances"))
    else:
        raise ValueError(f"unsupported topology model: {kind}")
    return {"expanded_vertices": vertices, "expanded_triangles": triangles, "instances": instances}


def assess(node):
    require(node.get("procedural") is True, "declare procedural=true for a topology-generating system")
    require(isinstance(node.get("complexity"), dict), "missing complexity object")
    cases = control_cases(node)
    estimates = {name: estimate(node["complexity"].get("model"), controls) for name, controls in cases.items()}
    budget = node.get("budget", {})
    require(isinstance(budget, dict), "budget must be an object")
    for required in ("max_expanded_triangles", "max_expanded_vertices"):
        require(integer(budget.get(required)) and budget[required] > 0, "procedural system needs " + required)
    if estimates["maximum"]["instances"]:
        require(integer(budget.get("max_instances")) and budget["max_instances"] > 0, "repetition needs max_instances")
    for key, limit in budget.items():
        require(key in BUDGET_METRICS and integer(limit) and limit > 0, "invalid budget key/value: " + key)
        metric = BUDGET_METRICS[key]
        if metric in estimates["maximum"]:
            require(estimates["maximum"][metric] <= limit,
                    f"maximum {metric} estimate {estimates['maximum'][metric]} exceeds {limit}; reduce controls or redesign")
    return {"node_id": node.get("id"), "controls": cases, "estimates": estimates,
            "scope": "Explicit sweep/grid/quad-subdivision/repetition topology only; not a Blender measurement"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("node_json")
    args = parser.parse_args()
    try:
        result = {"ok": True, **assess(json.loads(Path(args.node_json).read_text(encoding="utf-8")))}
    except (ValueError, OSError, TypeError, KeyError, AttributeError) as error:
        result = {"ok": False, "errors": [str(error)]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
