"""Bounded 2D rectangular tile footprints. Pure Python; no Blender or scene effects."""
import math

def rect_tiles(bounds, tile_size, joint, *, phase=(0,0), max_tiles=10000):
    """Return clipped footprints on caller's plane, all in the same length unit.

    bounds=(umin,umax,vmin,vmax), tile_size=(width,height), joint is clear gap.
    phase is the lower-left corner of lattice cell (0,0), not a normalized fraction.
    No fit-to-width stretching, automatic sliver deletion, holes or border trim.
    Caller chooses phase/cuts and builds geometry/instances with their own transforms.
    """
    if len(bounds)!=4 or len(tile_size)!=2 or len(phase)!=2:raise ValueError('Expected 4 bounds and 2D size/phase')
    if not all(math.isfinite(x) for x in (*bounds,*tile_size,*phase,joint)):raise ValueError('Finite lengths required')
    u0,u1,v0,v1=bounds;w,h=tile_size
    if u1<=u0 or v1<=v0 or min(w,h)<=0 or joint<0:raise ValueError('Positive area/tile dimensions and nonnegative gap required')
    if not isinstance(max_tiles,int) or max_tiles<1:raise ValueError('Positive piece bound required')
    su,sv=w+joint,h+joint;pu,pv=phase
    ir=range(math.floor((u0-pu-w)/su)+1,math.ceil((u1-pu)/su))
    jr=range(math.floor((v0-pv-h)/sv)+1,math.ceil((v1-pv)/sv))
    if len(ir)*len(jr)>max_tiles:raise ValueError('Layout exceeds piece budget')
    out=[]
    tol=1e-12*max(w,h)
    for j in jr:
        for i in ir:
            a,b=pu+i*su,pv+j*sv
            r=(max(u0,a),min(u1,a+w),max(v0,b),min(v1,b+h))
            if r[1]-r[0]<=tol or r[3]-r[2]<=tol:continue
            out.append(dict(cell=(i,j),bounds=r,cut=(r[0]>a+tol,r[1]<a+w-tol,r[2]>b+tol,r[3]<b+h-tol)))
    return out
