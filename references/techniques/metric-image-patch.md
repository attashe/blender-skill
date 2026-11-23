# Put a directional image on a dimensioned flat patch

**Use:** acquired maps must keep feature size/direction on a board, panel or flat interior
surface. This is UV placement and a map contract, not image-to-PBR recovery or a universal wood
material. For camera photographs needing rectification/delighting, choose the
[reference-derived route](../reference-derived-assets.md) first.

## Input contract

Actually inspect the source color image. Record its physical width/height, map roles, normal
convention and permitted use. Separate adjacent-board seams in a floor scan from the grain
of a single board. Use another source/crop if its visible joints contradict the modeled part.
Define U across the intended pattern and V along it; the image's actual grain may require
exchanging these axes. A 0.5 m square image covering a 0.10 × 0.30 m patch occupies
0.20 × 0.60 UV units. Non-square images need two physical dimensions. Offset changes the
selected source region, not the physical scale. Do not repack/rescale these UVs blindly.

## Small implementation

[metric_patch.py](../../scripts/techniques/metric_patch.py) supplies `planar_uv(...)` for
selected coplanar face indices on an editable mesh in Object Mode. Origin and axes are
mesh-local. `metres_per_unit` converts the local geometry unit; the Object and its parents
must have rigid transforms with applied scale. The function rejects unsupported scale,
shear, reflection and nonplanarity before assigning UVs. It never unwraps the rest of the mesh,
packs, renders or saves. UV writes affect all users of a shared Mesh: decide ownership first.

```python
from metric_patch import planar_uv  # add SKILL/scripts/techniques to sys.path
planar_uv(obj, face_indices, uv_name='SurfaceUV', origin=patch_origin,
          u_axis=across, v_axis=along, metres_per_unit=unit_scale,
          image_size_m=(source_width_m, source_height_m), offset=(0.12, 0.08))
```

Use separate patches with deliberate origins/orientations for different planes. This is not
a seamless unwrap of a curved corner. Preserve/unwrap continuity where the construction calls
for it. Long-grain maps cannot establish exposed solid-wood end grain: a veneer edge band and
a cut through timber are different surfaces. Do not call a rotated long-grain patch end grain.

## Connect the maps and then choose the finish

For the first connected surface, [image_surface.py](../../scripts/techniques/image_surface.py)
creates only the editable UV → supplied maps → Principled → Output graph below. It takes
already-loaded images and the UV name; it does not assign objects, alter source images,
choose a finish, pack or render. **One color image is sufficient**; roughness and normal
maps are optional. Existing same-named materials are preserved. Color-only starting point:

```python
from image_surface import image_surface
material = image_surface('Board base', uv_map='SurfaceUV', color=color_image)
# Assign to the intended material slot; view this base before adding layers or masks.
```

If acquired roughness/normal maps are available, pass `roughness=roughness_image` and/or
`normal=opengl_normal_image` to the same call. Those Image datablocks must already be
Non-Color; the normal map uses OpenGL. Their absence is not a reason to rebuild the graph.

Use one explicit UV Map node for all registered maps. Color uses its declared color encoding
(commonly sRGB); roughness and normal data use Non-Color. Image color space is an Image
datablock setting shared by its users. Reuse an existing assignment only with the same role.

```text
UV Map (SurfaceUV) → each Image Texture.Vector
color.Color → Principled.Base Color
roughness.Color → [optional deliberate finish remap] → Principled.Roughness
OpenGL normal.Color → Normal Map.Color → Principled.Normal
Normal Map: Tangent, UV map = SurfaceUV
Principled → active Material Output.Surface
```

Use the actual socket/node contract from [API diagnostics](../api-diagnostics.md) if unfamiliar.
Keep the normal convention explicit; converting DirectX and then selecting DirectX again
would double-correct it. A tile's dark grain is not automatically a height or roughness map.
AO is not a mandatory multiplier on base color. Select a clean substrate and its finish:
do not add another glossy coat blindly to a source that already represents the desired coating.
For an intentional new finish, keep roughness remapping/normal strength/coat independently
editable; compare under a broad highlight. No fixed values are a general oak preset.

Before rejecting a map as constant, verify its original bit depth and decoded values.
Converting a 16-bit Pillow `I;16` image directly with `convert('L')` can clip its samples
to 255 instead of scaling them: a varied roughness map then appears all-white. Inspect the
original range with its known encoding or Blender's decoded Non-Color float pixels.
Do not normalize every integer image by 255 or infer a normal convention from its mean color.

**First proof:** differently sized patches retain measured metres per UV span; a rigidly
rotated copy retains the same visible grain and relevant modifiers; compare a low-relief base
and chosen response without changing light/camera. Save/reopen and check actual dependencies.
Meaningful source regions and side/cut treatment still need an artist's visual comparison.

Extracted from a viewed, packed white-oak veneer study in Blender 5.2.1 LTS. Tested on metre
and centimetre inputs, doubled dimensions, rotations, invalid axes/planes/transforms, and
the reopened two-part sample. This validates metric flat-patch mapping and the demonstrated
finish. In a later independent Pi veneer trial, the metric helper produced seven correctly
scaled top/side/edge patches, including a rotated board; the packed saved view reproduced.
The worker still rebuilt its shader and diagnostic scripts: it misread the optional map
inputs, and API errors consumed work. The image-surface helper is author-tested; its
independent adoption remains unproven. These results validate the limited planar sample,
not a complete wood material or an efficient end-to-end workflow.
Raw-photo recovery and exposed solid end grain are outside this tested slice.
[Open the oak veneer study](../../assets/studies/oak-veneer/scene.blend) · [Rendered detail](../../assets/studies/oak-veneer/preview.png).

[Normal Map](https://docs.blender.org/manual/en/latest/render/shader_nodes/displacement/normal_map.html) ·
[Image color interpretation](https://docs.blender.org/manual/en/latest/editors/image/image_settings.html) ·
[Broader UV workflow](../uv-workflow.md)
