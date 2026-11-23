# Read molded plastic through its finish and curved reflection

**Use:** opaque molded furniture shells, trim, housings or handles. Establish whether the
reference is polished, satin, textured, translucent, painted or recycled with visible pigment
specks. These are distinct finishes. Smooth plastic can be complete with constant base color
and roughness; do not automatically add noise to every channel or paint dark edges.

**Contract:** a representative face plus rounded edge and known thickness, under a useful
reflected source. Curvature and parting lines belong to the object. Fine mold texture belongs
to the finish; it is not aggregate, chips or pores. If wear matters, place it by contact and
handling rather than uniformly across the surface. Keep the clean base independently usable.

For a fresh/caller-owned Principled `surface` in `tree`, whose BSDF already feeds the active
Material Output, this optional fine-relief branch uses Object coordinates in metres and an
object whose scale is identity:

```python
surface.inputs['Metallic'].default_value = 0
surface.inputs['IOR'].default_value = dielectric_ior
surface.inputs['Transmission Weight'].default_value = 0
surface.inputs['Subsurface Weight'].default_value = 0
surface.inputs['Coat Weight'].default_value = 0
surface.inputs['Roughness'].default_value = finish_roughness
coord = tree.nodes.new('ShaderNodeTexCoord')
grain = tree.nodes.new('ShaderNodeTexNoise')
grain.noise_dimensions = '3D'
grain.inputs['Scale'].default_value = 1 / feature_spacing
grain.inputs['Detail'].default_value = 0
tree.links.new(coord.outputs['Object'], grain.inputs['Vector'])
bump = tree.nodes.new('ShaderNodeBump')
bump.inputs['Strength'].default_value = 1
bump.inputs['Distance'].default_value = relief_depth
tree.links.new(grain.outputs['Fac'], bump.inputs['Height'])
tree.links.new(bump.outputs['Normal'], surface.inputs['Normal'])
```

Choose positive `feature_spacing` and nonnegative `relief_depth` in the coordinate/scene
units. Base Color remains the separately chosen pigment. The roughness constant captures
unresolved microsurface scattering; optional Bump supplies spatially resolved variation.
Do not duplicate a strong version of the same field in both channels by default. A colored
polymer remains dielectric: metallic response is not a shortcut to a brighter highlight.
Paint, clear coat and transmitting plastic require their own justified branches.

**First proof:** compare two roughness values with unchanged geometry, pigment, lights and
view. The reflected source should broaden/change, not merely tint the object. Compare relief
on/off separately. If the detail image is a uniform color patch, first put a curved edge or
reflected strip in view. Raising noise depth cannot replace the missing diagnostic highlight.
Keep this diagnostic lighting separate from the intended presentation lighting and save the
configuration needed to repeat it. A pixel difference alone does not establish visible grain.

Inspect the normal delivery size as well as a close view. Denoising can suppress weak grain;
if that grain is a required cue, test a small adequately sampled crop before increasing relief.
Retain a clean surface when the reference calls for it. [Shader authoring](../texture-authoring-workflow.md)
owns source/filtering choices; [surface families](../surface-families.md) covers other finishes.

**Evidence boundary:** Cycles 5.2.1 author sample uses IOR 1.46, roughness 0.34, optional
0.45 mm nominal noise spacing and 8 μm bump distance. A 0.16/0.55 roughness comparison is
a response test, not measured polypropylene data. No subsurface glow, recycled fleck pattern,
coat, scratches, export parity or independent Pi application is certified.
[Evidence](provenance.md#upholstery-and-plastic-extraction).

[Vitra material reference](https://www.vitra.com/en-se/magazine/details/the-eames-plastic-chair-for-a-more-sustainable-future) ·
[Dielectric and microsurface behavior](https://experienceleague.adobe.com/en/docs/substance-3d/general-knowledge/openpbr/openpbr-overview)
