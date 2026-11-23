"""One explicit UV/color/roughness/OpenGL-normal surface, not a finished material preset."""
import math
import bpy

def image_surface(name, *, uv_map, color, roughness=None, normal=None,
                  roughness_default=.5, normal_strength=1):
    """Create a new editable material from already-loaded Image datablocks.

    Caller owns image roles/colorspaces; data maps must be Non-Color. Does not modify
    images/objects, load files, assign/pack/save/render, or infer maps from color.
    Existing same-named materials are retained; Blender gives the new one a unique name.
    No coating, variation, face mask or generated end-grain; add only the needed response.
    """
    if not name or not uv_map:raise ValueError('Material and UV names required')
    if not 0<=roughness_default<=1 or not math.isfinite(normal_strength) or normal_strength<0:
        raise ValueError('Valid roughness and nonnegative normal strength required')
    for role,im in [('Color',color),('Roughness',roughness),('Normal',normal)]:
        if role!='Color' and im is None:continue
        if not isinstance(im,bpy.types.Image) or min(im.size)<=0:raise ValueError(f'{role}: loaded image required')
        if role!='Color' and im.colorspace_settings.name!='Non-Color':raise ValueError(f'{role}: Non-Color data image required')
    m=bpy.data.materials.new(name);m.use_nodes=True;t=m.node_tree;t.nodes.clear()
    def node(kind,name,xy):
        n=t.nodes.new(kind);n.name=name;n.label=name;n.location=xy;return n
    uv=node('ShaderNodeUVMap','Surface UV',(-700,0));uv.uv_map=uv_map
    bs=node('ShaderNodeBsdfPrincipled','Surface', (100,0));bs.inputs['Roughness'].default_value=roughness_default
    out=node('ShaderNodeOutputMaterial','Surface output',(450,0));out.is_active_output=True
    t.links.new(bs.outputs['BSDF'],out.inputs['Surface'])
    for i,(role,im,socket) in enumerate([('Color',color,'Base Color'),('Roughness',roughness,'Roughness'),('Normal',normal,None)]):
        if im is None:continue
        tex=node('ShaderNodeTexImage',role,(-450,300-i*300));tex.image=im;tex.extension='REPEAT'
        t.links.new(uv.outputs['UV'],tex.inputs['Vector'])
        if socket:t.links.new(tex.outputs['Color'],bs.inputs[socket])
        else:
            nm=node('ShaderNodeNormalMap','Tangent normal',(-100,-300));nm.space='TANGENT';nm.uv_map=uv_map;nm.inputs['Strength'].default_value=normal_strength
            t.links.new(tex.outputs['Color'],nm.inputs['Color']);t.links.new(nm.outputs['Normal'],bs.inputs['Normal'])
    return m
