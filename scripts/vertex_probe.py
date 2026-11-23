"""Read-only Blender diagnostics for an existing armature-bound mesh."""
import math

import bpy
from mathutils.kdtree import KDTree


def mirrored_weights(mesh, rig, bone_name, radius, *, tolerance=None, limit=12):
    """Rank source vertices near a rest joint by left/right deform-weight difference.

    Reflect across the armature's local X=0 plane. Radius and matching tolerance
    are in armature-local units. A match must be unique within tolerance in both
    directions. Scores are sums of absolute differences in stored group weights.
    Posed world coordinates are supplied for an armature-only viewport stack.
    """
    if mesh.type != "MESH" or rig.type != "ARMATURE" or mesh.is_evaluated or rig.is_evaluated:
        raise ValueError("Pass the original mesh object and its armature object")
    if mesh.data.is_editmode or rig.data.is_editmode:
        raise ValueError("Finish mesh or armature Edit Mode before reading stored vertices and bones")
    modifiers = [m for m in mesh.modifiers if m.show_viewport]
    if not any(m.type == "ARMATURE" and m.object == rig and m.use_vertex_groups for m in modifiers):
        raise ValueError("The mesh needs an enabled Armature modifier using this rig's vertex groups")
    if not math.isfinite(radius) or radius <= 0:
        raise ValueError("radius must be finite and positive")
    if tolerance is None:
        tolerance = radius * 0.001
    if not math.isfinite(tolerance) or tolerance <= 0 or type(limit) is not int or limit <= 0:
        raise ValueError("Use a finite positive tolerance and a positive integer limit")

    center = rig.data.bones[bone_name].head_local
    if abs(center.x) <= tolerance:
        raise ValueError("Choose a rest joint on one side of the armature's X=0 plane")
    graph = bpy.context.evaluated_depsgraph_get()
    posed = mesh.evaluated_get(graph)
    to_rig = rig.evaluated_get(graph).matrix_world.inverted() @ posed.matrix_world
    vertices = mesh.data.vertices
    keys = mesh.data.shape_keys
    rest = keys.reference_key.data if keys else vertices
    positions = [to_rig @ vertex.co for vertex in rest]
    tree = KDTree(len(positions))
    for index, point in enumerate(positions):
        tree.insert(point, index)
    tree.balance()

    def partner(index):
        point = positions[index]
        hits = tree.find_range((-point.x, point.y, point.z), tolerance)
        if len(hits) == 1:
            other = hits[0][1]
            if point.x * positions[other].x < 0:
                return other
        return None

    deform = {bone.name for bone in rig.data.bones if bone.use_deform}
    names = {g.index: g.name for g in mesh.vertex_groups if g.name in deform}
    flipped = {number: bpy.utils.flip_name(name) for number, name in names.items()}

    def weights(index, group_names):
        return {group_names[g.group]: g.weight for g in vertices[index].groups
                if g.group in group_names and g.weight > 0}

    region = [index for index, point in enumerate(positions)
              if point.x * center.x > 0 and (point - center).length <= radius]
    ranked = []
    for index in region:
        other = partner(index)
        if other is None or partner(other) != index:
            continue
        actual = weights(index, names)
        expected = weights(other, flipped)
        difference = sum(abs(actual.get(k, 0) - expected.get(k, 0)) for k in actual.keys() | expected.keys())
        ranked.append((difference, index, other))
    ranked.sort(key=lambda row: (-row[0], row[1]))

    direct = all(m.type == "ARMATURE" for m in modifiers) and len(posed.data.vertices) == len(vertices)
    candidates = []
    for difference, index, other in ranked[:limit]:
        candidates.append(dict(index=index, mirror_index=other, weight_l1=difference,
                               weights=weights(index, names), expected_weights=weights(other, flipped),
                               posed_world=list(posed.matrix_world @ posed.data.vertices[index].co) if direct else None))
    return dict(in_region=len(region), matched=len(ranked), unmatched=len(region) - len(ranked),
                posed_positions_available=direct, candidates=candidates)
