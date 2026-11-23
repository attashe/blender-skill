"""Read-only, scoped topology/winding measurements. Run inside Blender.

Import has no side effects. inspect_mesh() uses a temporary evaluated mesh/BMesh and
never repairs, selects, applies modifiers or saves the object. Measurements are not
a watertightness, self-intersection, thickness or appearance certificate.
"""
import math
from pathlib import Path
import bmesh
import bpy
from mathutils import Vector


def inspect_mesh(obj, *, evaluated=True, epsilon=1e-6, max_faces=100000):
    """Inspect one mesh in local units; epsilon is a caller-chosen length tolerance.

    Signed volume is interpreted only for coherent closed nondegenerate components.
    Separate nested cavity boundaries may intentionally have negative winding.
    Object transform determinant is separate: reflection is not a reason to blindly
    flip the source mesh. Modifiers use the current scene/frame's viewport depsgraph.
    """
    if obj.type != 'MESH' or obj.mode != 'OBJECT':
        raise ValueError('One mesh in Object Mode is required')
    if not math.isfinite(epsilon) or epsilon <= 0 or max_faces < 1:
        raise ValueError('Positive finite tolerance and face bound required')
    eo = obj.evaluated_get(bpy.context.evaluated_depsgraph_get()) if evaluated else obj
    mesh = eo.to_mesh() if evaluated else obj.data
    bm = bmesh.new()
    try:
        if len(mesh.polygons) > max_faces:
            raise ValueError('Sample exceeds max_faces; choose a smaller target/stage')
        bm.from_mesh(mesh)
        bm.faces.index_update()
        bm.verts.index_update()
        pending = set(bm.faces)
        groups = []
        while pending:
            seed = pending.pop()
            group = {seed}; stack = [seed]
            while stack:
                face = stack.pop()
                for edge in face.edges:
                    for adjacent in edge.link_faces:
                        if adjacent in pending:
                            pending.remove(adjacent);group.add(adjacent);stack.append(adjacent)
            groups.append(group)
        groups.sort(key=lambda group: min(f.index for f in group))
        components = []
        for group in groups:
            faces = sorted(group, key=lambda f: f.index)
            edges = {e for f in faces for e in f.edges}
            vertices = {v for f in faces for v in f.verts}
            bad_edges = sum(not e.is_manifold for e in edges)
            inconsistent = sum(e.is_manifold and not e.is_contiguous for e in edges)
            degenerate = sum(f.calc_area() <= epsilon**2 for f in faces)
            bad_vertices = sum(not v.is_manifold for v in vertices)
            # Same vertex cycle, including reversed winding, is a duplicate face.
            # Distinct overlapping shells with separate vertices remain out of scope.
            signatures = set()
            for face in faces:
                ids = [v.index for v in face.verts]
                start = ids.index(min(ids))
                forward = tuple(ids[start:] + ids[:start])
                backward = (forward[0],) + tuple(reversed(forward[1:]))
                signatures.add(min(forward, backward))
            duplicates = len(faces) - len(signatures)
            closed = bool(faces) and not (bad_edges or inconsistent or degenerate or bad_vertices or duplicates)
            # Invalid components have no interpretable shell volume. Do not reconstruct
            # their faces: duplicate faces can make BMesh.faces.new raise before reporting.
            raw_volume = None
            if closed:
                center = sum((v.co for v in vertices), Vector()) / len(vertices)
                copy = bmesh.new()
                try:
                    mapping = {v: copy.verts.new(v.co-center) for v in vertices}
                    for face in faces:
                        copy.faces.new([mapping[v] for v in face.verts])
                    copy.normal_update()
                    raw_volume = copy.calc_volume(signed=True)
                finally:
                    copy.free()
            sign = ('positive' if raw_volume > epsilon**3 else
                    'negative' if raw_volume < -epsilon**3 else 'near_zero') if closed else 'uninterpreted'
            components.append(dict(faces=len(faces),sample_face_indices=[f.index for f in faces[:8]],
                boundary_edges=sum(e.is_boundary for e in edges),nonmanifold_edges=bad_edges,
                inconsistent_edges=inconsistent,nonmanifold_vertices=bad_vertices,
                degenerate_faces=degenerate,duplicate_faces=duplicates,coherent_closed=closed,
                raw_signed_volume_local=raw_volume,volume_sign=sign))
        matrix = eo.matrix_world
        world_points = [matrix @ v.co for v in bm.verts]
        bounds = ([[min(v[i] for v in world_points) for i in range(3)],
                   [max(v[i] for v in world_points) for i in range(3)]] if world_points else None)
        result = dict(object=obj.name,mesh=obj.data.name,evaluated=evaluated,
            frame=bpy.context.scene.frame_current,scene=bpy.context.scene.name,
            local_length_tolerance=epsilon,world_transform_determinant=matrix.to_3x3().determinant(),
            world_bounds=bounds,
            world_axis_extents=[bounds[1][i]-bounds[0][i] for i in range(3)] if bounds else None,
            vertices=len(bm.verts),edges=len(bm.edges),faces=len(bm.faces),
            wire_edges=sum(e.is_wire for e in bm.edges),
            isolated_vertices=sum(not v.link_edges for v in bm.verts),components=components,
            not_checked=['self_intersections','duplicate_overlapping_shells','physical_thickness',
                         'intended_cavity_orientation','opening_clearance','custom_shading_normals',
                         'render_only_modifier_differences'])
        return result
    finally:
        bm.free()
        if evaluated: eo.to_mesh_clear()


def main():
    import argparse,json,sys
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--expect-file',required=True)
    p.add_argument('--scene')
    p.add_argument('--object',action='append',required=True)
    p.add_argument('--source',action='store_true',help='Inspect base mesh instead of evaluated mesh')
    p.add_argument('--epsilon',type=float,default=1e-6)
    p.add_argument('--output-json')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    if not bpy.data.filepath or Path(bpy.data.filepath).resolve()!=Path(a.expect_file).resolve():
        raise ValueError('Loaded file does not match --expect-file')
    scene=bpy.data.scenes[a.scene] if a.scene else bpy.context.scene
    if scene!=bpy.context.scene:
        raise ValueError('Requested scene is not active; activate it explicitly before probing')
    reports=[]
    for name in a.object:
        obj=scene.objects.get(name)
        if obj is None:raise ValueError(f'Object {name!r} is absent from active scene')
        reports.append(inspect_mesh(obj,evaluated=not a.source,epsilon=a.epsilon))
    result=dict(file=bpy.data.filepath,version=bpy.app.version_string,objects=reports,
                note='Successful execution is not an asset quality verdict; inspect components and intended construction.')
    payload=json.dumps(result,indent=2)
    if a.output_json:Path(a.output_json).write_text(payload,encoding='utf-8')
    else:print(payload)


if __name__=='__main__':main()
