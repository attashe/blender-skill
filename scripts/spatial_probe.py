"""Read-only spatial measurements inside Blender, current scene/frame/viewport graph.

pair_clearance(first_objects, second_objects, axis=(1,0,0)) measures ordered projected
intervals of evaluated mesh vertices. Positive = separation, negative = interval overlap;
neither implies shortest surface distance or a collision test.
first_hit(origin, direction, distance) samples the active scene in world coordinates.
No scene changes, selection, frame changes, automatic repairs or import-time work.
"""
import math
from pathlib import Path
import bpy
from mathutils import Vector


def _vector(values, *, direction=False):
    if len(values)!=3 or not all(math.isfinite(v) for v in values):
        raise ValueError('Expected three finite world coordinates')
    v=Vector(values)
    if direction:
        if v.length<1e-12: raise ValueError('Direction must be nonzero')
        v.normalize()
    return v


def _points(objects, max_vertices):
    if not isinstance(max_vertices,int) or max_vertices<1:
        raise ValueError('max_vertices must be a positive integer')
    if not objects: raise ValueError('Choose at least one mesh object')
    graph=bpy.context.evaluated_depsgraph_get()
    points=[]
    for obj in objects:
        if obj.type!='MESH' or obj.mode!='OBJECT':
            raise ValueError(f'{obj.name}: requires a mesh in Object Mode')
        if obj.name not in bpy.context.view_layer.objects:
            raise ValueError(f'{obj.name}: not in active view layer')
        evaluated=obj.evaluated_get(graph)
        try:
            mesh=evaluated.to_mesh()
            if not mesh or not mesh.vertices: raise ValueError(f'{obj.name}: no evaluated vertices')
            if len(points)+len(mesh.vertices)>max_vertices:
                raise ValueError('Vertex limit exceeded; choose a smaller sample')
            points.extend(evaluated.matrix_world @ v.co for v in mesh.vertices)
        finally:
            evaluated.to_mesh_clear()
    return points


def pair_clearance(first_objects, second_objects, axis=(1,0,0), *, max_vertices=100000):
    """Projected extent gap from FIRST's maximum to SECOND's minimum along +axis."""
    first_objects=list(first_objects); second_objects=list(second_objects)
    if set(first_objects)&set(second_objects): raise ValueError('Groups must be disjoint')
    axis=_vector(axis,direction=True)
    seed=min((Vector((1,0,0)),Vector((0,1,0)),Vector((0,0,1))),key=lambda v:abs(v.dot(axis)))
    u=axis.cross(seed).normalized(); v=axis.cross(u).normalized()
    a=_points(first_objects,max_vertices); b=_points(second_objects,max_vertices)
    intervals=[]
    for direction in [axis,u,v]:
        av=[p.dot(direction) for p in a]; bv=[p.dot(direction) for p in b]
        lo_a,hi_a=min(av),max(av); lo_b,hi_b=min(bv),max(bv)
        intervals.append(dict(direction=list(direction),first=[lo_a,hi_a],second=[lo_b,hi_b],
                              interval_overlap=min(hi_a,hi_b)-max(lo_a,lo_b)))
    gap=intervals[0]['second'][0]-intervals[0]['first'][1]
    return dict(first=[o.name for o in first_objects],second=[o.name for o in second_objects],
                axis=list(axis),signed_clearance=gap,units='world Blender units',
                meters_per_unit=bpy.context.scene.unit_settings.scale_length,
                projections=intervals,measurement='ordered projected extents of evaluated mesh vertices',
                not_checked=['shortest surface distance','actual collision','physical wall thickness',
                             'unrealized instances','render-only modifiers'])


def first_hit(origin, direction, distance):
    """First evaluated scene hit; never filters hidden cutters/occluders or assumes a target."""
    origin=_vector(origin); direction=_vector(direction,direction=True)
    if not math.isfinite(distance) or distance<=0: raise ValueError('distance must be finite and positive')
    scene=bpy.context.scene
    hit,point,normal,index,obj,matrix=scene.ray_cast(bpy.context.evaluated_depsgraph_get(),origin,direction,distance=distance)
    return dict(origin=list(origin),direction=list(direction),max_distance=distance,hit=bool(hit),
                object=obj.name if hit else None,location=list(point) if hit else None,
                distance=(point-origin).length if hit else None,
                face_index=index if hit else None,
                scope='Scene.ray_cast at current frame/viewport graph; not render visibility or full opening coverage')


def main():
    import argparse,json,sys
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--expect-file',required=True)
    p.add_argument('--scene',help='Assert the active scene, never switch it')
    p.add_argument('--first',action='append',default=[],help='Repeat for parts in first group')
    p.add_argument('--second',action='append',default=[],help='Repeat for parts in second group')
    p.add_argument('--axis',nargs=3,type=float,default=[1,0,0])
    p.add_argument('--ray',nargs=7,type=float,action='append',default=[],metavar=('OX','OY','OZ','DX','DY','DZ','DIST'))
    p.add_argument('--max-vertices',type=int,default=100000)
    p.add_argument('--output-json')
    args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    sys.path.insert(0,str(Path(__file__).resolve().parent))
    from api_probe import identity
    result=dict(identity=identity(args.expect_file,args.first+args.second))
    if args.scene and bpy.context.scene.name!=args.scene: raise ValueError('Wrong active scene')
    if bool(args.first)!=bool(args.second): raise ValueError('Provide both --first and --second')
    if not args.first and not args.ray: raise ValueError('Choose a pair or at least one ray')
    if len(args.ray)>32: raise ValueError('At most 32 rays per probe')
    if args.first:
        result['pair']=pair_clearance([bpy.data.objects[n] for n in args.first],
                                     [bpy.data.objects[n] for n in args.second],args.axis,max_vertices=args.max_vertices)
    result['rays']=[first_hit(r[:3],r[3:6],r[6]) for r in args.ray]
    encoded=json.dumps(result,ensure_ascii=False)
    if args.output_json:
        path=Path(args.output_json).resolve()
        if path==Path(args.expect_file).resolve() or path.suffix.lower()!='.json':
            raise ValueError('Use a .json report path different from the input scene')
        path.write_text(encoded+'\n',encoding='utf-8')
    print(encoded)


if __name__=='__main__':main()
