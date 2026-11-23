"""Read-only camera framing of selected mesh bounds, in the current scene/frame.

inspect_frame(camera, objects) projects evaluated bounding-box corners for PERSP/ORTHO.
face_angle(camera, object, local_normal) reports a caller-specified surface direction.
No camera placement, visibility changes, render, save or import-time work.
"""
import math
from pathlib import Path
import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view


def _camera(camera):
    if camera is None or camera.type!='CAMERA':raise ValueError('Choose an existing camera')
    if camera.name not in bpy.context.scene.objects:raise ValueError('Camera is not in active scene')
    if camera.data.type not in {'PERSP','ORTHO'}:raise ValueError('Only perspective/orthographic cameras supported')
    return camera.evaluated_get(bpy.context.evaluated_depsgraph_get())


def _mesh(obj):
    if obj.type!='MESH' or obj.mode!='OBJECT':raise ValueError('Choose a mesh in Object Mode')
    if obj.name not in bpy.context.view_layer.objects:raise ValueError('Target is not in active view layer')
    ev=obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    if not ev.data.vertices:raise ValueError('Target has no evaluated mesh vertices')
    return ev


def inspect_frame(camera, objects):
    """Full-frame bounds; crop borders, occlusion, visibility and artistic quality not certified."""
    camera=_camera(camera);scene=bpy.context.scene;objects=list(objects)
    if not 1<=len(objects)<=64:raise ValueError('Choose 1..64 target meshes')
    measurements=[]
    pixels=[scene.render.resolution_x*scene.render.resolution_percentage/100,
            scene.render.resolution_y*scene.render.resolution_percentage/100]
    for obj in objects:
        ev=_mesh(obj)
        points=[world_to_camera_view(scene,camera,ev.matrix_world@Vector(c)) for c in ev.bound_box]
        depth=[min(p.z for p in points),max(p.z for p in points)]
        front=depth[0]>0
        rectangle=[[min(p[i] for p in points) for i in range(2)],
                   [max(p[i] for p in points) for i in range(2)]] if front else None
        inside=front and all(0<=p.x<=1 and 0<=p.y<=1 and camera.data.clip_start<=p.z<=camera.data.clip_end for p in points)
        measurements.append(dict(object=obj.name,depth=depth,all_corners_in_front=front,
            ndc_bounds=rectangle,bounds_inside_full_frame=inside,
            projected_extent_pixels=[(rectangle[1][i]-rectangle[0][i])*pixels[i] for i in range(2)] if front else None,
            object_hide_render=obj.hide_render,viewport_visible=obj.visible_get()))
    return dict(scene=scene.name,frame=scene.frame_current,camera=camera.name,projection=camera.data.type,
        resolution_pixels=pixels,render_border_enabled=scene.render.use_border,targets=measurements,
        not_checked=['occlusion','render visibility through collections/view layers','compositor crop',
                     'render border coverage','unrealized instances','surface readability','depth of field',
                     'render-only modifier differences'],
        note='Conservative evaluated mesh bounds, not exact silhouette. Crossing camera plane makes 2D extent undefined.')


def face_angle(camera, obj, local_normal):
    """View angle at evaluated bound center; caller supplies the intended surface's local normal."""
    camera=_camera(camera);ev=_mesh(obj)
    if len(local_normal)!=3 or not all(math.isfinite(x) for x in local_normal):raise ValueError('Use a finite 3D local normal')
    normal=Vector(local_normal)
    if normal.length<1e-12:raise ValueError('Normal must be nonzero')
    center=sum((Vector(c) for c in ev.bound_box),Vector())/8
    center=ev.matrix_world@center
    direction=(camera.matrix_world.to_3x3()@Vector((0,0,1)) if camera.data.type=='ORTHO'
               else camera.matrix_world.translation-center)
    if direction.length<1e-12:raise ValueError('Camera coincides with target center')
    normal=(ev.matrix_world.to_3x3().inverted().transposed()@normal).normalized()
    cosine=max(-1,min(1,normal.dot(direction.normalized())))
    return dict(object=obj.name,camera=camera.name,local_normal=list(local_normal),
                world_normal=list(normal),sample_world=list(center),signed_cosine=cosine,
                angle_degrees=math.degrees(math.acos(cosine)),
                note='0 faces camera; 90 edge-on; 180 faces away. Assumes supplied normal describes the surface; no curved/deformed normal inference.')


def main():
    import argparse,json,sys
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--expect-file',required=True);p.add_argument('--scene')
    p.add_argument('--camera',help='Default: currently active camera, without assigning one')
    p.add_argument('--object',action='append',required=True)
    p.add_argument('--face',nargs=4,action='append',default=[],metavar=('OBJECT','NX','NY','NZ'))
    p.add_argument('--output-json')
    args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    sys.path.insert(0,str(Path(__file__).resolve().parent))
    from api_probe import identity
    names=args.object+[f[0] for f in args.face]+([args.camera] if args.camera else [])
    result=dict(identity=identity(args.expect_file,names))
    if args.scene and bpy.context.scene.name!=args.scene:raise ValueError('Wrong active scene')
    camera=bpy.data.objects[args.camera] if args.camera else bpy.context.scene.camera
    result['framing']=inspect_frame(camera,[bpy.data.objects[n] for n in args.object])
    result['faces']=[face_angle(camera,bpy.data.objects[f[0]],list(map(float,f[1:]))) for f in args.face]
    encoded=json.dumps(result,ensure_ascii=False)
    if args.output_json:
        path=Path(args.output_json).resolve()
        if path==Path(args.expect_file).resolve() or path.suffix.lower()!='.json':raise ValueError('Use a separate .json report path')
        path.write_text(encoded+'\n',encoding='utf-8')
    print(encoded)


if __name__=='__main__':main()
