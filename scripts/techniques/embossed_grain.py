"""A shallow cellular height source, not a complete leather material.

Run inside Blender. Coordinates belong to the caller's ShaderNodeTree and are in
metres (or convert feature_size to their units). Returns a scalar height socket;
creates only field nodes. Does not assign materials, normals, color, save or render.
"""
import math
from numbers import Real


def embossed_height(tree, coordinates, *, feature_size, warp_fraction=.6,
                    groove_fraction=.12):
    """Return normalized rounded cell height for a bounded embossed-grain study.

    feature_size is nominal Voronoi spacing, not a guaranteed cell diameter.
    warp_fraction controls a centered low-frequency coordinate warp.
    groove_fraction is the positive cell-distance range mapped to a rounded valley.
    Each call creates a new independent branch; edit an existing branch for reuse.
    """
    for name,value in [('feature_size',feature_size),('warp_fraction',warp_fraction),
                       ('groove_fraction',groove_fraction)]:
        if isinstance(value,bool) or not isinstance(value,Real) or not math.isfinite(value):
            raise ValueError(name+' must be a finite number')
    if feature_size<=0 or warp_fraction<0 or groove_fraction<=0:
        raise ValueError('Positive feature_size/groove_fraction and nonnegative warp_fraction required')
    if getattr(tree,'bl_idname',None)!='ShaderNodeTree':
        raise ValueError('Expected a ShaderNodeTree')
    if not getattr(coordinates,'is_output',False) or coordinates.node.id_data!=tree:
        raise ValueError('Coordinate output must belong to this tree')
    nodes,links=tree.nodes,tree.links
    warp=nodes.new('ShaderNodeTexNoise');warp.name='Grain warp'
    warp.inputs['Scale'].default_value=1/(feature_size*4)
    warp.inputs['Detail'].default_value=1;warp.location=(-900,-160)
    links.new(coordinates,warp.inputs['Vector'])
    center=nodes.new('ShaderNodeVectorMath');center.operation='SUBTRACT'
    center.inputs[1].default_value=(.5,.5,.5);center.location=(-680,-160)
    links.new(warp.outputs['Color'],center.inputs[0])
    amplitude=nodes.new('ShaderNodeVectorMath');amplitude.operation='SCALE';amplitude.name='Warp amplitude'
    amplitude.inputs['Scale'].default_value=feature_size*warp_fraction;amplitude.location=(-460,-160)
    links.new(center.outputs['Vector'],amplitude.inputs[0])
    position=nodes.new('ShaderNodeVectorMath');position.operation='ADD';position.location=(-240,100)
    links.new(coordinates,position.inputs[0]);links.new(amplitude.outputs['Vector'],position.inputs[1])
    cells=nodes.new('ShaderNodeTexVoronoi');cells.name='Embossed grain'
    cells.feature='DISTANCE_TO_EDGE';cells.voronoi_dimensions='3D'
    cells.inputs['Scale'].default_value=1/feature_size;cells.location=(-20,100)
    links.new(position.outputs['Vector'],cells.inputs['Vector'])
    height=nodes.new('ShaderNodeMapRange');height.name='Rounded grain valleys'
    height.interpolation_type='SMOOTHERSTEP';height.clamp=True; height.location=(220,100)
    for key,value in [('From Min',0),('From Max',groove_fraction),('To Min',0),('To Max',1)]:
        height.inputs[key].default_value=value
    links.new(cells.outputs['Distance'],height.inputs['Value'])
    return height.outputs['Result']
