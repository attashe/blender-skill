# Separate embossed upholstery grain from its polymer finish

**Use:** smooth or finely embossed PU/PVC-like upholstery, leatherette or a coated cushion.
Identify the actual finish from a viewed swatch and a curved furnished example. "Leather"
does not imply biological skin SSS, velvet sheen, deep wrinkles or a glossy clear coat.
The covered cushion shape, welt and seams belong to geometry; a pore field cannot build them.

**Choose the source:** for characteristic pores, broken/branching creases, logos or close
product matching, use a suitable licensed scan/map or authored pattern. The small procedural
[height builder](../../scripts/techniques/embossed_grain.py) below is a controllable approximation
of shallow cellular embossing. It does not model arbitrary natural leather or reconstruct
the manufacturer's swatch. Do not keep enlarging its cells when the required pattern differs.

## A small field-to-finish branch

**Inputs:** caller-owned ShaderNodeTree `tree` and a fresh/unlinked Principled `surface`,
known coordinate units, feature spacing and relief depth. With Object coordinates, this
example expects identity object scale and one Blender unit per metre. A differently sized
part can share the material after its local geometry is sized in metres. Generated coordinates
would instead normalize to its bounds and change grain size between parts.

Import `embossed_height` from the helper after adding the skill's `scripts/techniques` to
the Python path. The helper returns a height socket and changes no geometry, assignment or
material output. The caller connects the existing Principled BSDF to the active Surface output.

```python
from embossed_grain import embossed_height
coord = tree.nodes.new('ShaderNodeTexCoord')
height = embossed_height(tree, coord.outputs['Object'], feature_size=grain_spacing)
bump = tree.nodes.new('ShaderNodeBump')
bump.inputs['Strength'].default_value = 1
bump.inputs['Distance'].default_value = relief_depth
tree.links.new(height, bump.inputs['Height'])
tree.links.new(bump.outputs['Normal'], surface.inputs['Normal'])
surface.inputs['Metallic'].default_value = 0
surface.inputs['IOR'].default_value = dielectric_ior
surface.inputs['Transmission Weight'].default_value = 0
surface.inputs['Subsurface Weight'].default_value = 0
surface.inputs['Roughness'].default_value = base_roughness
surface.inputs['Coat Weight'].default_value = coat_weight
surface.inputs['Coat Roughness'].default_value = coat_roughness
tree.links.new(bump.outputs['Normal'], surface.inputs['Coat Normal'])
```

`grain_spacing` is nominal cellular spacing, not a guaranteed cell diameter. `relief_depth`
scales a normalized height field in scene units. Bump perturbs shading normals; it does not
add physical thickness or change silhouette. Keep pigment largely independent of this height
unless the reference shows a color relationship. Darkening every valley can turn a subtle
emboss into cracked stone. A photo's valley shadows are not automatically albedo marks.

Coat is optional. Here its normal follows the embossed substrate; a genuinely leveling
coating may need a smoother normal. Do not leave a flat coat normal accidentally, or add
another full-strength glossy shader to simulate a finish. Roughness, IOR and coat weight
solve different questions; use [material composition](../material-composition.md) if unsure.

**First proof:** keep camera/light/exposure fixed and compare relief on/off, then coat on/off.
Change grain spacing without changing relief depth to distinguish frequency from amplitude.
Inspect a broad curved highlight and a delivery-size close view. Keep the whole furniture
view calm: subpixel grains should not be inflated to remain individually visible from afar.
Use [rest coordinates](rest-coordinates.md) for deforming upholstery; the simple Object route
here is for rigid/static parts. Reopen the material and inspect an actual render.

**Evidence boundary:** Cycles 5.2.1 author study used nominal 1.2 mm spacing, 45 μm bump
distance, roughness 0.38 and a restrained 0.16/0.30 coat. Those are authored controls, not
measured Brisa properties. No physical coating thickness, natural-leather fidelity, deformation
or independent Pi use is certified. [Evidence](provenance.md#upholstery-and-plastic-extraction).

[PU upholstery reference](https://www.leeindustries.com/Upholstery/Detail/Fabric/BRISA/99911977) ·
[Bump controls](https://docs.blender.org/manual/en/3.0/render/shader_nodes/vector/bump.html)
