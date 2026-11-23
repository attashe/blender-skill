"""Read-only, scoped Blender RNA/animation inspection. Run inside Blender.

identity(expected_file, objects=()) verifies the input.
member(instance_or_rna_type, name) describes one actual RNA member.
find_ops(query, limit=6) finds registered operators and checks their current poll.
control(object_or_pose_bone, limit=12) reports only that control's state.
animation(bpy_struct, limit=12) resolves its ID owner and assigned Action slot.
No import-time work, frame changes, scene edits or automatic repairs.
The CLI writes a JSON report only when --output-json is supplied.
"""
import difflib
from pathlib import Path

import bpy
from bpy_extras import anim_utils


def identity(expected_file, objects=()):
    actual = bpy.data.filepath
    if not actual or Path(actual).resolve() != Path(expected_file).resolve():
        raise ValueError(f"Wrong input: {actual!r}; expected {str(expected_file)!r}")
    missing = [name for name in objects if name not in bpy.data.objects]
    if missing:
        raise ValueError(f"Required objects missing: {missing}")
    scene=bpy.context.scene
    camera=scene.camera
    return dict(file=actual, version=bpy.app.version_string,
                frame=scene.frame_current,
                fps=scene.render.fps / scene.render.fps_base,
                scene=scene.name, view_layer=bpy.context.view_layer.name,
                active_camera=camera.name if camera else None,
                camera_in_scene=bool(camera and camera.name in scene.objects),
                engine=scene.render.engine,
                resolution=[scene.render.resolution_x,scene.render.resolution_y],
                resolution_percentage=scene.render.resolution_percentage,
                state_scope='Loaded memory; reopen without setup edits to verify saved state')


def member(target, name):
    """Describe a property/function; a missing name is data, never a guessed fallback."""
    rna = target.bl_rna
    result = dict(type=rna.identifier, requested=name, found=False)
    prop = rna.properties.get(name)
    if prop is not None:
        result.update(found=True, kind='property', value_type=prop.type,
                      readonly=prop.is_readonly, description=prop.description)
        if prop.type == 'ENUM':
            result['enum_identifiers'] = [item.identifier for item in prop.enum_items]
            result['enum_note'] = 'RNA items; dynamic/context choices may be incomplete'
        if hasattr(prop, 'array_length'):
            result['array_length'] = prop.array_length
    elif (func := rna.functions.get(name)) is not None:
        result.update(found=True, kind='function', description=func.description,
                      parameters=[dict(name=p.identifier, type=p.type,
                                       required=p.is_required, output=p.is_output)
                                  for p in func.parameters])
    else:
        names = list(rna.properties.keys()) + list(rna.functions.keys())
        result['nearby_members'] = difflib.get_close_matches(name, names, n=6, cutoff=.35)
        result['next'] = 'Check the owning type/needed operation; nearby names are not replacements'
    return result


def _limit(value):
    if not isinstance(value, int) or not 1 <= value <= 64:
        raise ValueError('limit must be an integer from 1 to 64')
    return value


def _bounded(values, limit):
    return dict(items=values[:limit], total=len(values), truncated=len(values) > limit)


def find_ops(query, limit=6):
    """Match all terms in an operator ID or RNA label. An exact ID also shows enums."""
    limit = _limit(limit)
    query = query.strip().casefold().removeprefix("bpy.ops.")
    terms = query.split()
    if not terms:
        raise ValueError("Supply an operator ID or one or more search words")
    hits = []
    unreadable = 0
    for namespace in dir(bpy.ops):
        if namespace.startswith("_"):
            continue
        group = getattr(bpy.ops, namespace)
        for name in dir(group):
            if name.startswith("_"):
                continue
            op_id = f"{namespace}.{name}"
            op = getattr(group, name)
            try:
                rna = op.get_rna_type()
            except (AttributeError, KeyError, ReferenceError, RuntimeError):
                unreadable += 1
                continue
            text = f"{op_id} {rna.name}".casefold()
            if all(term in text for term in terms):
                words = op_id.replace(".", "_").split("_")
                rank = (op_id != query, -sum(t in words for t in terms), len(words), op_id)
                hits.append((rank, op_id, op, rna))
    rows = []
    for _, op_id, op, rna in sorted(hits, key=lambda hit: hit[0])[:limit]:
        props = [p for p in rna.properties if p.identifier != "rna_type"]
        row = dict(id=op_id, label=rna.name, params=[f"{p.identifier}:{p.type.lower()}" for p in props[:16]])
        if len(props) > 16:
            row["param_count"] = len(props)
        if op_id == query:
            enums = {p.identifier: _bounded([item.identifier for item in p.enum_items], 16)
                     for p in props[:16] if p.type == "ENUM"}
            if enums:
                row["enums"] = enums
        try:
            row["poll"] = op.poll()
        except Exception as exc:
            row.update(poll=None, poll_error=f"{type(exc).__name__}: {str(exc)[:160]}")
        rows.append(row)
    result = dict(total=len(hits), ops=rows)
    if unreadable:
        result["unreadable_operator_count"] = unreadable
    return result


def animation(target, limit=12):
    """Assigned slot + matching drivers, scoped by target.path_from_id().

    Does not flatten NLA or claim its curves are the evaluated motion.
    The Blender utility returns the first matching channelbag, not all layers.
    """
    limit = _limit(limit)
    owner = target.id_data
    prefix = '' if isinstance(target, bpy.types.ID) else target.path_from_id()
    result = dict(owner=owner.name, owner_type=owner.bl_rna.identifier, path=prefix)
    ad = getattr(owner, 'animation_data', None)
    if ad is None:
        return dict(result, action=None, curves=_bounded([], limit),
                    drivers=_bounded([], limit), nla=_bounded([], limit))

    def relevant(path):
        return not prefix or path == prefix or path.startswith(prefix + '.') or path.startswith(prefix + '[')

    action, slot = ad.action, ad.action_slot
    result.update(action=action.name if action else None,
                  slot=slot.identifier if slot else None)
    bag = anim_utils.action_get_channelbag_for_slot(action, slot)
    curves = []
    for fc in bag.fcurves if bag else ():
        if relevant(fc.data_path):
            curves.append(dict(path=fc.data_path, index=fc.array_index, mute=fc.mute,
                               keys=len(fc.keyframe_points), extrapolation=fc.extrapolation,
                               modifiers=[m.type for m in fc.modifiers]))
    drivers = []
    for fc in ad.drivers:
        if relevant(fc.data_path):
            sources = [dict(variable=v.name, variable_type=v.type,
                            id=t.id.name if t.id else None, path=t.data_path,
                            bone=t.bone_target, transform=t.transform_type, space=t.transform_space)
                       for v in fc.driver.variables for t in v.targets]
            drivers.append(dict(path=fc.data_path, index=fc.array_index, mute=fc.mute,
                                expression=fc.driver.expression, sources=_bounded(sources, limit)))
    nla = [dict(name=t.name, mute=t.mute, solo=t.is_solo, strips=len(t.strips)) for t in ad.nla_tracks]
    result.update(curves=_bounded(curves, limit), drivers=_bounded(drivers, limit),
                  nla=_bounded(nla, limit),
                  scope='First channelbag for assigned slot; NLA listed, not evaluated')
    return result


def surface(obj, limit=12):
    """Stored mesh/material/UV/stack facts; no evaluation or appearance claim."""
    limit = _limit(limit)
    if not isinstance(obj, bpy.types.Object) or obj.type != 'MESH':
        raise TypeError('surface expects one Mesh Object')
    mesh = obj.data
    slots = [dict(index=i, material=slot.material.name if slot.material else None,
                  link=slot.link,
                  mesh_material=mesh.materials[i].name if mesh.materials[i] else None)
             for i, slot in enumerate(obj.material_slots)]
    uvs = [dict(name=uv.name, active_render=uv.active_render) for uv in mesh.uv_layers]
    modifiers = [dict(name=m.name, type=m.type, viewport=m.show_viewport, render=m.show_render)
                 for m in obj.modifiers]
    return dict(mesh=mesh.name, mesh_users=mesh.users, dimensions=list(obj.dimensions),
                vertices=len(mesh.vertices), faces=len(mesh.polygons),
                material_slots=_bounded(slots, limit), uv_maps=_bounded(uvs, limit),
                modifiers=_bounded(modifiers, limit),
                scope='Stored assignments; dimensions use current object state, not a fit/topology test')


def control(target, limit=12):
    """Compact Object/PoseBone state, with ID owner and existing animation."""
    limit = _limit(limit)
    if not isinstance(target, (bpy.types.Object, bpy.types.PoseBone)):
        raise TypeError('control expects Object or PoseBone; use member() for other RNA types')
    custom = [dict(name=k, value=v if isinstance(v, (str, int, float, bool)) else '<non-scalar>')
              for k, v in target.items()]
    constraints = [dict(name=c.name, type=c.type, mute=c.mute, influence=c.influence)
                   for c in target.constraints]
    mode = target.rotation_mode
    rotation = (target.rotation_quaternion if mode == 'QUATERNION' else
                target.rotation_axis_angle if mode == 'AXIS_ANGLE' else target.rotation_euler)
    result = dict(name=target.name, type=target.bl_rna.identifier,
                parent=target.parent.name if target.parent else None,
                location=list(target.location), rotation_mode=mode,
                rotation=list(rotation), scale=list(target.scale),
                custom=_bounded(custom, limit), constraints=_bounded(constraints, limit),
                animation=animation(target, limit))
    if isinstance(target, bpy.types.Object) and target.type == 'MESH':
        result['surface'] = surface(target, limit)
    return result


def main():
    """Optional background entrypoint; load the input before this script."""
    import argparse
    import json
    import sys
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expect-file', help='Input .blend to verify. Optional for --find-ops alone.')
    parser.add_argument('--find-ops', action='append', default=[], metavar='QUERY')
    parser.add_argument('--object', action='append', default=[])
    parser.add_argument('--bone', nargs=2, action='append', default=[], metavar=('RIG', 'BONE'))
    parser.add_argument('--rna', nargs=2, action='append', default=[], metavar=('TYPE', 'MEMBER'))
    parser.add_argument('--tree', action='append', default=[], metavar='OWNER:NAME')
    parser.add_argument('--node', nargs=2, action='append', default=[], metavar=('OWNER:NAME', 'NODE'))
    parser.add_argument('--input', nargs=3, action='append', default=[], metavar=('OWNER:NAME', 'NODE', 'SOCKET'))
    parser.add_argument('--depth', type=int, default=2)
    parser.add_argument('--max-nodes', type=int, default=8)
    parser.add_argument('--limit', type=int, default=12)
    parser.add_argument('--output-json', help='Optional caller-owned report path; scene is never saved')
    args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else [])
    _limit(args.limit)
    result = {}
    if args.expect_file:
        result['identity'] = identity(args.expect_file, args.object + [r for r, b in args.bone])
        result['controls'] = [control(bpy.data.objects[n], args.limit) for n in args.object]
        result['controls'] += [control(bpy.data.objects[r].pose.bones[b], args.limit) for r, b in args.bone]
        result['members'] = [member(getattr(bpy.types, t), m) for t, m in args.rna]
    elif not args.find_ops or any((args.object, args.bone, args.rna, args.tree, args.node, args.input)):
        parser.error('--expect-file is required for scene inspection')
    if args.find_ops:
        result['operators'] = {q: find_ops(q, args.limit) for q in args.find_ops}
    errors = 0
    if args.tree or args.node or args.input:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import node_probe
        result['node_queries'] = []
        for kind, requests in (('tree', [(t,) for t in args.tree]), ('node', args.node), ('input', args.input)):
            for request in requests:
                record = dict(query=kind, request=request)
                try:
                    tree = node_probe.resolve_tree(request[0])
                    if kind == 'tree':
                        value = node_probe.describe_tree(tree, args.limit)
                    elif kind == 'node':
                        value = node_probe.describe_node(tree.nodes[request[1]], args.limit)
                    else:
                        value = node_probe.trace_input(tree.nodes[request[1]], request[2],
                                                      args.depth, args.max_nodes, args.limit)
                    record.update(status='ok', result=value)
                except Exception as exc:
                    errors += 1
                    record.update(status='probe_error', error_type=type(exc).__name__, error=str(exc))
                result['node_queries'].append(record)
    encoded = json.dumps(result, ensure_ascii=False)
    if args.output_json:
        output = Path(args.output_json).resolve()
        if bpy.data.filepath and output == Path(bpy.data.filepath).resolve():
            raise ValueError('Report path must differ from the input scene')
        output.write_text(encoded + '\n', encoding='utf-8')
    print(encoded)
    if errors:
        raise RuntimeError(f'{errors} node queries failed; partial results preserved, failed checks are not verified')


if __name__ == '__main__':
    main()
