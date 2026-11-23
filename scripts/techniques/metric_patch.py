"""Metric UVs for a selected planar patch. No import-time scene changes."""
import math
from mathutils import Vector

def planar_uv(obj, faces, *, uv_name, origin, u_axis, v_axis,
              metres_per_unit, image_size_m, offset=(0,0), plane_tolerance_m=1e-5):
    """Assign loop UVs; axes/origin are mesh-local, dimensions are physical metres.

    Rectilinear flat patch only. Object transform must be rigid with applied scale.
    Does not unwrap curved surfaces, pack islands or infer wood end grain.
    Existing UV values outside the selected faces are retained.
    """
    if obj.type!='MESH' or obj.mode!='OBJECT':raise ValueError('Use an editable mesh in Object Mode')
    indices=list(faces)
    if not indices or len(set(indices))!=len(indices):raise ValueError('Choose distinct face indices')
    if any(not isinstance(i,int) or not 0<=i<len(obj.data.polygons) for i in indices):raise ValueError('Invalid face index')
    if not uv_name or not isinstance(uv_name,str):raise ValueError('Name the UV layer')
    if not math.isfinite(metres_per_unit) or metres_per_unit<=0:raise ValueError('Positive unit scale required')
    if len(image_size_m)!=2 or not all(math.isfinite(x) and x>0 for x in image_size_m):raise ValueError('Positive physical image width/height required')
    if len(offset)!=2 or not all(math.isfinite(x) for x in offset):raise ValueError('Finite UV offset required')
    if not math.isfinite(plane_tolerance_m) or plane_tolerance_m<0:raise ValueError('Invalid plane tolerance')
    def vec(x):
        if len(x)!=3 or not all(math.isfinite(v) for v in x):raise ValueError('Use finite 3D vectors')
        return Vector(x)
    p,u,v=vec(origin),vec(u_axis),vec(v_axis)
    if min(u.length,v.length)<1e-9:raise ValueError('Nonzero UV axes required')
    u.normalize();v.normalize()
    if abs(u.dot(v))>1e-6:raise ValueError('Orthogonal UV axes required')
    matrix=obj.matrix_world.to_3x3();gram=matrix.transposed()@matrix
    if matrix.determinant()<=0 or any(abs(gram[r][c]-(1 if r==c else 0))>1e-5 for r in range(3) for c in range(3)):
        raise ValueError('Apply object/parent scale or shear first; rigid transforms only')
    n=u.cross(v);pending=[]
    for i in indices:
        for li in obj.data.polygons[i].loop_indices:
            point=obj.data.vertices[obj.data.loops[li].vertex_index].co-p
            if abs(point.dot(n))*metres_per_unit>plane_tolerance_m:raise ValueError('Selected patch is not on the stated plane')
            pending.append((li,(point.dot(u)*metres_per_unit/image_size_m[0]+offset[0],point.dot(v)*metres_per_unit/image_size_m[1]+offset[1])))
    uv=obj.data.uv_layers.get(uv_name) or obj.data.uv_layers.new(name=uv_name)
    for li,co in pending:uv.data[li].uv=co
    return dict(uv_map=uv.name,faces=len(indices),loops=len(pending),image_size_m=list(image_size_m))
