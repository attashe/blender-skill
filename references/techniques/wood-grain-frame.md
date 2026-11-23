# Grain, cut and finish on manufactured timber

**Use:** a board, framed door, furniture or panel where generic waves/noise read as stripes,
clouds or a ribbed surface. Start from the viewed reference's cut, finish and viewing distance.
This is a diagnostic route from partial material trials, not a validated oak shader preset.

## Establish the board's coordinate frame

Distinguish the longitudinal fiber axis, the across-grain face direction and the exposed cut.
Align each rail/stile/board deliberately. Rotating a material by 90 degrees is meaningful only
with known source-local axes. Object coordinates can carry a pattern with a rigid part;
Generated normalizes its bounds and may change feature size between different board dimensions.
A common Empty intentionally supplies shared alignment; it is not automatically board-local.
Re-centering origins is optional and does not itself prove that the shader follows the part.

Inspect two visible faces and the relevant end/corner. A field varying only along a face's
normal can be nearly constant across that face while making stripes on its neighbor.
Changing the band direction or adding cross-axis variation may repair coverage but does not
establish the grain of a particular cut. Choose suitable face/cut maps, an explicit 3D grain
model or a hybrid when different faces need different structure. Do not claim end grain from
a diagonal continuation of the same bands alone.

An Image Texture in **Flat** projection uses the mapped X/Y plane; a 3D Object vector
does not make the image volumetric. If one mapped coordinate is constant across an edge
face, the photo collapses into stretched lines there even when the top looks correct.
Compare two surface directions on each visible face before tuning saturation, bump or coat.
Use deliberately oriented face UVs or another suitable projection; Box blending alone does
not identify veneer wrapping versus a real wood cut.
Normals can select the face/projection, but its image coordinates come from **position or UV**.
`Normal.z` is constant across a flat face; multiplying it cannot supply distance along an edge.
Choose two position directions lying in that face, then rotate the grain within that 2D plane.
A 90-degree rotation out of the plane can collapse a working top projection as well.
For example, an XY face needs two varying coordinates from X/Y, while an XZ side needs
X/Z; this describes coverage, not the correct grain/cut. A scale of 2 only represents a
0.5 m image patch when both source coordinates actually measure surface distance.
See [image projection](https://docs.blender.org/manual/en/5.1/render/shader_nodes/textures/image.html).

For a supplied veneer color image or map set on flat faces, the
[metric image patch](metric-image-patch.md) provides small `planar_uv` and `image_surface`
helpers: orient each face patch, then connect a simple UV/image base before adding finish
layers. A color image alone is enough to use this route. It does not establish exposed
solid-wood end grain or the reference's exact finish.

## Match structure before decorating it

| Observation | Next useful comparison |
| --- | --- |
| Equally spaced parallel bars dominate | Compare their spacing, continuity and contrast with a similar-sized reference patch. Modulate or replace the source when its repeated structure is wrong; simply lowering contrast or adding fine Noise may leave the same bars. |
| Fine lines disappear or shimmer | Check their physical size and pixels per feature at delivery resolution. A node's Scale is not a documented universal cycles-per-metre control; calibrate on a dimensioned sample instead of inventing a period formula. |
| Pattern disappears after regrouping; scale/contrast edits change only a flat color | Check the [coordinate signal across the group boundary](../api-diagnostics.md#constant-procedural-pattern-after-grouping) before more tuning. A created Mapping node is not a connected coordinate source. |
| Flat front, strongly striped side | Inspect coordinates on both planes before changing roughness/light. One successful face cannot validate a 3D part. |
| Looks carved, fuzzy or ribbed | Hold color/light and bypass bump; compare the actual highlight. Restore only relief supported by the finish and scale. |
| Calm but featureless after an adjustment | Revisit the defining grain/cut cue; removal of an artifact is not completion. |

The reference decides whether growth bands, fine pores, cathedral figures, knots or end grain
are relevant. Do not put every feature into every board. An existing licensed scan/material
can be faster than inventing distinctive structure; procedural and hybrid routes remain valid
when they reproduce the cue. Keep texture sources separate from observation-only reference photos.

Separate wood color/structure from finish. A clear coat changes reflection; it cannot supply
missing grain. Compare a neutral/low-relief base and the chosen finish under a useful broad
highlight. For an unfamiliar node, validate its actual type/properties/sockets on one scratch
instance with the [API/node probe](../api-diagnostics.md) before wiring the complete material.

## Prove the sample and keep the diagnostic view useful

Use one connected corner/rail-stile sample before distributing the treatment. Show enough of
both faces, the joint and edge highlight. For the rigid-rotation check, compare the same visible
face/feature on an original and rotated copy; shared mesh/material and a nonzero angle alone
are structural facts, not visible proof. Preserve the evaluated surface needed for comparison:
a new Object pointing to the same Mesh does not inherit the source Object's Bevel or other
modifiers. Keep those relevant settings on the diagnostic copy, or label the geometric difference.
Choose a view that exposes that face, not just its edge.
The [camera probe](camera-framing.md) can flag out-of-frame bounds or an almost edge-on surface
before a render. Inspect pixels afterward. Keep diagnostic visibility and the final saved view
deliberate, and repeat the needed observation after reopening.

Use [bounded bevel checks](cut-bevel.md) for edge shape and [light isolation](light-role-ab.md)
for a changed reflection. Keep camera/exposure/light stable within a material A/B; a brighter
render is not evidence of better grain. Reuse only the part/material that passed the comparison.

[Coordinates](https://docs.blender.org/manual/en/latest/render/shader_nodes/input/texture_coordinate.html) ·
[Wave texture](https://docs.blender.org/manual/it/5.2/render/shader_nodes/textures/wave.html) ·
[Bump scale](https://docs.blender.org/manual/id/5.2/render/shader_nodes/displacement/bump.html) ·
[Broader surface families](../surface-families.md)
