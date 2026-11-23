#!/usr/bin/env python3
"""Audit a saved asset inside Blender. No modeling or status changes.

blender -b FILE.blend --python audit_blend.py -- --node-id ID --root-collection ROOT --output REPORT.json
Or runpy.run_path(SCRIPT, init_globals={"AUDIT_PARAMS": {...}})["result"] through Blender MCP.
AUDIT_PARAMS keys: node_id, root_collection, output (absolute report path).
Optional AUDIT_DEPSGRAPH must be an actual Blender render/viewport graph supplied by the host.
Requires Blender bpy; do not run as a replacement for live visual or behavior checks.
"""

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path


def digest(path):
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def resolve_library_path(library):
    """Resolve a linked library to an absolute path.

    Blender stores a library's path relative to the file being saved, and that includes libraries reached through
    another library: a scene linking a module which links an assembly stores the assembly path relative to the scene.
    Resolving only against the library parent's directory therefore produces a doubled prefix (assets/assets/...)
    and reports an existing file as missing. Try the audited file's own directory first, then the parent's, and keep
    whichever resolves to a real file; if neither exists return the root-relative path so a genuinely missing file is
    still reported.
    """
    import bpy
    tries = []
    try:
        tries.append(bpy.path.abspath(library.filepath))
    except Exception:
        pass
    try:
        if library.parent is not None:
            tries.append(bpy.path.abspath(library.filepath, library=library.parent))
    except Exception:
        pass
    for candidate in tries:
        try:
            path = Path(candidate).resolve()
        except Exception:
            continue
        if path.is_file():
            return path
    # bpy.path.abspath only applies a library's directory to paths carrying the // prefix, so a stored path without it
    # silently resolves against the current file. Join it to the parent library's resolved directory instead.
    if library.parent is not None and library.filepath:
        stored = library.filepath
        if stored.startswith("//"):
            stored = stored[2:]
        try:
            guess = resolve_library_path(library.parent).parent / stored
            if guess.is_file():
                return guess.resolve()
        except Exception:
            pass
    try:
        return Path(tries[0]).resolve()
    except Exception:
        return Path(str(library.filepath))


def audit(params, depsgraph=None):
    import bpy
    from mathutils import Vector

    started = time.perf_counter()
    allowed = {"node_id", "root_collection", "output"}
    if set(params) != allowed or not all(isinstance(x, str) and x for x in params.values()):
        raise ValueError("AUDIT_PARAMS requires exactly node_id, root_collection, output strings")
    source = Path(bpy.data.filepath).resolve() if bpy.data.filepath else None
    if source is None or not source.is_file():
        raise ValueError("Save the intended .blend file before auditing it")
    output = Path(params["output"])
    if not output.is_absolute() or output.suffix.lower() != ".json" or output.resolve() == source:
        raise ValueError("Use an absolute .json report path different from the source file")
    root = bpy.data.collections.get(params["root_collection"])
    report = {"schema_version": 1, "node_id": params["node_id"], "source_sha256": digest(source),
              "source_saved": not bpy.data.is_dirty, "blender_version": bpy.app.version_string,
              "root_collection": params["root_collection"], "root_exists": root is not None,
              "unit_scale": bpy.context.scene.unit_settings.scale_length,
              "unit_system": bpy.context.scene.unit_settings.system,
              "errors": [], "missing_files": [], "libraries": [], "references": [], "resources": [],
              "local_geometry": [], "sockets": {}, "render_divergence": [], "curve_settings": []}
    active_collections, seen = set(), set()

    def scene_collections(collection):
        if collection.as_pointer() in active_collections:
            return
        active_collections.add(collection.as_pointer())
        for child in collection.children:
            scene_collections(child)

    scene_collections(bpy.context.scene.collection)
    report["root_in_active_scene"] = root is not None and root.as_pointer() in active_collections
    members, refs, source_objects = set(), {}, {}

    def reference(collection):
        if collection.library:
            library = collection.library
            path = resolve_library_path(library)
            refs[(str(path), collection.name)] = {"path": str(path), "collection": collection.name}

    def traverse(collection):
        if collection.as_pointer() in seen:
            return
        seen.add(collection.as_pointer())
        reference(collection)
        if collection.hide_viewport != collection.hide_render:
            report["render_divergence"].append(f"Collection visibility differs: {collection.name}")
        for obj in collection.objects:
            members.add(obj.as_pointer())
            source_objects[obj.as_pointer()] = obj
            if obj.instance_collection is not None:
                reference(obj.instance_collection)
                traverse(obj.instance_collection)
        for child in collection.children:
            traverse(child)

    if root:
        traverse(root)
        geometry_types = {"MESH", "CURVE", "SURFACE", "FONT", "META", "VOLUME", "POINTCLOUD", "CURVES", "GREASEPENCIL"}
        for obj in root.all_objects:
            if obj.type in geometry_types and obj.library is None and obj.override_library is None:
                report["local_geometry"].append(obj.name)
            if obj.type == "EMPTY" and obj.name.startswith("SOCKET_"):
                report["sockets"][obj.name] = list(obj.matrix_world.translation)
    else:
        report["errors"].append("Public root collection missing")
    report["references"] = list(refs.values())
    if getattr(bpy.context.scene.render, "use_simplify", False):
        report["render_divergence"].append("Scene Simplify settings require production verification")
    checked_groups = set()

    def inspect_group(group):
        if group is None or group.as_pointer() in checked_groups:
            return
        checked_groups.add(group.as_pointer())
        for node in group.nodes:
            if node.bl_idname == "GeometryNodeIsViewport":
                report["render_divergence"].append(f"Is Viewport branch requires render verification: {group.name}")
            if hasattr(node, "node_tree"):
                inspect_group(node.node_tree)

    for obj in source_objects.values():
        if obj.type in {"MESH", "CURVE", "SURFACE", "FONT", "META", "CURVES"}:
            if obj.hide_viewport != obj.hide_render:
                report["render_divergence"].append(f"Object visibility differs: {obj.name}")
            for modifier in obj.modifiers:
                if modifier.show_viewport != modifier.show_render:
                    report["render_divergence"].append(f"Modifier visibility differs: {obj.name}/{modifier.name}")
                if hasattr(modifier, "levels") and hasattr(modifier, "render_levels") and modifier.levels != modifier.render_levels:
                    report["render_divergence"].append(f"Subdivision levels differ: {obj.name}/{modifier.name}")
                if modifier.type == "NODES":
                    inspect_group(modifier.node_group)
        if obj.type in {"CURVE", "SURFACE"} and hasattr(obj.data, "splines"):
            data = obj.data
            settings = {"object": obj.name, "type": obj.type,
                        "control_points": sum(len(s.bezier_points) if s.type == "BEZIER" else len(s.points) for s in data.splines)}
            for key in ("resolution_u", "resolution_v", "render_resolution_u", "render_resolution_v", "bevel_resolution", "bevel_depth"):
                if hasattr(data, key):
                    settings[key] = getattr(data, key)
            settings["splines"] = [{"type": spline.type, **{key: getattr(spline, key) for key in
                                    ("resolution_u", "resolution_v", "order_u", "order_v", "use_cyclic_u", "use_cyclic_v")
                                    if hasattr(spline, key)}} for spline in data.splines]
            report["curve_settings"].append(settings)
            for axis in ("u", "v"):
                preview = getattr(data, "resolution_" + axis, None)
                render = getattr(data, "render_resolution_" + axis, 0)
                if preview is not None and render and render != preview:
                    report["render_divergence"].append(f"Curve/surface render resolution differs: {obj.name}/{axis}")

    for library in bpy.data.libraries:
        path = resolve_library_path(library)
        exists = path.is_file()
        report["libraries"].append({"path": str(path), "stored_path": library.filepath,
                                    "sha256": digest(path) if exists else None})
        if not exists:
            report["missing_files"].append(str(path))
    resources = {}
    for category in (bpy.data.images, bpy.data.fonts, bpy.data.sounds, bpy.data.movieclips, bpy.data.volumes):
        for item in category:
            file = getattr(item, "filepath", "")
            if not file or file == "<builtin>" or getattr(item, "packed_file", None) or getattr(item, "packed_files", None):
                continue
            path = Path(bpy.path.abspath(file, library=item.library)).resolve()
            if getattr(item, "source", None) in {"TILED", "SEQUENCE"} or getattr(item, "is_sequence", False):
                report["errors"].append(f"Check all sequence/UDIM resources separately: {item.name}")
            elif not path.is_file():
                report["missing_files"].append(str(path))
            elif path not in resources:
                resources[path] = {"path": str(path), "sha256": digest(path)}
    report["resources"] = list(resources.values())

    depsgraph = depsgraph if depsgraph is not None else bpy.context.evaluated_depsgraph_get()
    report["evaluation_mode"] = depsgraph.mode
    expanded_triangles, expanded_vertices, evaluated_objects, instances = 0, 0, 0, 0
    geometry_cache, object_costs, minimum, maximum = {}, {}, [float("inf")] * 3, [-float("inf")] * 3
    for instance in depsgraph.object_instances:
        obj = instance.object
        original = obj.original
        parent = instance.parent.original if instance.parent is not None else None
        if original.as_pointer() not in members and (parent is None or parent.as_pointer() not in members):
            continue
        evaluated_objects += 1
        instances += int(instance.is_instance)
        if obj.type not in {"MESH", "CURVE", "SURFACE", "FONT", "META", "CURVES"}:
            if obj.type in {"VOLUME", "POINTCLOUD", "GREASEPENCIL"}:
                report["errors"].append(f"Geometry type needs a dedicated audit: {obj.name} ({obj.type})")
            continue
        # Key on the ORIGINAL object, not the evaluated one. Evaluated object pointers are recycled while
        # iterating object_instances: in the planning room two pointers covered 112 visits across 15
        # distinct objects, so caching by evaluated pointer reused one object's vertices for another and
        # transformed them with the other's matrix, inflating both the bounds and the per-object costs.
        key = original.as_pointer()
        if key not in geometry_cache:
            mesh = None
            try:
                mesh = obj.to_mesh()
                if mesh is None:
                    raise ValueError("evaluated to_mesh returned no mesh")
                mesh.calc_loop_triangles()
                vertices = [tuple(v.co) for v in mesh.vertices]
                geometry_cache[key] = (len(mesh.loop_triangles), vertices)
            except Exception as error:
                report["errors"].append(f"Cannot measure {obj.name}: {error}")
                geometry_cache[key] = (0, [])
            finally:
                if mesh is not None:
                    obj.to_mesh_clear()
        triangles, vertices = geometry_cache[key]
        expanded_triangles += triangles
        expanded_vertices += len(vertices)
        if key not in object_costs:
            object_costs[key] = {"object": original.name, "type": obj.type,
                                 "evaluated_vertices": len(vertices), "evaluated_triangles": triangles,
                                 "occurrences": 0, "expanded_triangles": 0, "expanded_vertices": 0}
        object_costs[key]["occurrences"] += 1
        object_costs[key]["expanded_triangles"] += triangles
        object_costs[key]["expanded_vertices"] += len(vertices)
        for vertex in vertices:
            world = instance.matrix_world @ Vector(vertex)
            for axis in range(3):
                minimum[axis] = min(minimum[axis], world[axis])
                maximum[axis] = max(maximum[axis], world[axis])
    valid_bounds = minimum[0] != float("inf")
    report["metrics"] = {"expanded_triangles": expanded_triangles,
                         "expanded_vertices": expanded_vertices,
                         "instances": instances,
                         "unique_evaluated_triangles": sum(x[0] for x in geometry_cache.values()),
                         "evaluated_objects": evaluated_objects,
                         "dimensions_m": [maximum[i] - minimum[i] for i in range(3)] if valid_bounds else [0, 0, 0],
                         "measurement_seconds": time.perf_counter() - started}
    report["largest_objects"] = sorted(object_costs.values(), key=lambda x: x["expanded_triangles"], reverse=True)[:20]
    report["render_divergence"] = sorted(set(report["render_divergence"]))
    report["scope"] = f"Actual {depsgraph.mode} dependency graph, public root and referenced collection instances; world-space bounds"
    report["errors"] = sorted(set(report["errors"]))
    report["missing_files"] = sorted(set(report["missing_files"]))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def cli():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--node-id", required=True)
    parser.add_argument("--root-collection", required=True)
    parser.add_argument("--output", required=True)
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    args = parser.parse_args(argv)
    try:
        result = audit({"node_id": args.node_id, "root_collection": args.root_collection, "output": args.output})
        print(json.dumps(result, ensure_ascii=False))
        return 0 if not result["errors"] and not result["missing_files"] and result["source_saved"] else 1
    except ImportError:
        print(json.dumps({"ok": False, "error": "Run inside Blender (bpy is unavailable in host Python)"}))
        return 1


if "AUDIT_PARAMS" in globals():
    result = audit(AUDIT_PARAMS, globals().get("AUDIT_DEPSGRAPH"))
elif __name__ == "__main__":
    raise SystemExit(cli())
