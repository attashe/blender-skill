# Passes, mattes and reconstruction

Read with [compositing](compositing-workflow.md) when the task needs selective control,
layer assembly, AOVs or a reconstructed beauty. Plan useful inputs before a costly render,
then check what actually exists in the saved file. Renderer/version support differs.

Small implementations: [raw lobe reconstruction](techniques/pass-reconstruction.md), [alpha Over](techniques/alpha-over.md), [saved Cryptomatte grade](techniques/crypto-local-exposure.md). Read the relevant one once the operation is known.

## Choose information by the intended edit

| Required control | Candidate input | Boundary to verify |
| --- | --- | --- |
| Local object/material correction | Cryptomatte Object/Material; Asset grouping where appropriate | Names, coverage, manifest/metadata and layer survive saving and reopening |
| Custom material region, wear or effect intensity | Named Shader AOV, Color or Value, produced in the material | Pass declaration and AOV Output name/type agree; actual pixels contain the intended signal |
| Separate foreground, background or effects | View Layers and collection controls; holdouts/shadow catcher where appropriate | Exclusion, indirect-only and holdout change transport/alpha differently; shadows/reflections must still integrate |
| Adjust light families | Light Groups supported by the renderer | What lights/world belong to each group, whether all contributions are accounted for, and reconstruction against the source |
| Adjust a lighting lobe | Diffuse/glossy/transmission direct, indirect and color plus other relevant contributions | Lobe formula and engine semantics, emission/environment/volume terms, no duplicated contribution |
| Depth-aware atmosphere or post blur | Z/Mist/Vector as needed | Meaning, units, range, camera and frame alignment; raw depth and categorical indices are not smooth coverage mattes |

A Shader AOV exports a signal; it does not change the material's beauty by itself. Create the
View Layer AOV and connect the intended shader value to the matching AOV Output. Names and
types are a data interface, not labels to guess later. When a GN attribute feeds this signal,
verify that the material sees it in the renderer. Keep scalar masks independent of display
color transforms. A new AOV declaration cannot recover information from an older saved render.

View Layers retain combinations of scene contributions. A second render with a collection
excluded can change indirect light, reflections and shadows; assembling such images is not
guaranteed to match the original scene. Decide what must remain visible to camera, indirect
rays or shadows. Test overlaps and contacts before rendering the full sequence.

## Use Cryptomatte as encoded data

Enable the required Cryptomatte type and sufficient levels before rendering. Select the
correct source scene/image, View Layer and crypto layer in the Cryptomatte node, then select
IDs by actual names/picker information. View the resulting matte: a connected node or a
colorful Pick preview does not establish that the intended object was selected. Verify a
target interior, a non-target region, and a partially covered edge.

Save the original ID/coverage channels with their metadata/manifest. Cryptomatte hashes need
32-bit float preservation and lossless storage; half precision, lossy compression, color
conversion, filtering or denoising can corrupt their meaning. Extract mattes before image
resampling and ordinary color operations. A file called multilayer EXR is not proof that
the required channels and metadata were written: inspect and reopen it with the actual
consumer. A flattened File Output beauty is not a substitute for the original crypto source.
For multipart EXR, inspect all parts/layers; a reader showing only the first part can hide
passes that are present elsewhere in the same file.

Inspect the extracted matte's actual range and edges before using it as a mix factor. Do not
assume its values are confined to [0,1]; an unclamped mix extrapolates outside that range.
Choose the consumer's factor range deliberately and compare the edge. If clamping is needed,
apply it to the derived factor, not to encoded crypto IDs, original pass data or HDR beauty.

Cryptomatte supports multiple coverage contributions per pixel, but it is not deep image
data and does not give the unobscured beauty of each selected object. A selection through
transparent/refractive materials depends on renderer behavior and pass settings; inspect
the difficult pixels. Motion blur, DOF and overlapping objects need enough ID levels and
their own checks. Do not claim that a mask removes background contamination already mixed
into a beauty. Separate render elements or scene changes may be needed for an exact edit.

## Reconstruct only when the task benefits

For EEVEE Shader to RGB, prefer the verified Combined result: ordinary lighting-pass
reconstruction does not preserve that shader evaluation. See [cel shading](cel-shading-workflow.md)
for the renderer and palette contract.

Start from Combined for ordinary finishing. Reconstruction adds control and more ways to
lose or double-count light. For Cycles' conventional lobe passes, a representative expression
is `DiffuseColor * (DiffuseDirect + DiffuseIndirect)`, with corresponding glossy and
transmission terms. Add the separately stored emission, environment and volume contributions
that actually participate in this render, following its pass definitions. Do not multiply
Emission by a surface color or add an entire Light Group beauty on top of Combined.
With Film Transparent, the Environment pass can still contain the camera-visible world for
optional background assembly; do not add it when matching the transparent Combined. World
illumination/reflections already present in the lighting lobes are a separate contribution.

Prove a neutral reconstruction before grading: compare raw source Combined and reconstructed
RGB with matching frame, view, resolution and denoising state. Use an absolute-difference
image and an error metric appropriate to precision/noise. A small example with only diffuse
and glossy objects cannot certify glass, volumes, shadow catcher or every EEVEE pass.
Pass antialiasing, coverage filtering and nonlinear operations can also affect edge agreement;
inspect interior and fractional-coverage regions separately and report residuals rather
than hiding them with a tolerance chosen after seeing the result.

Carry alpha deliberately from the correct source when recombining RGB. Adding pass RGBA
values can inadvertently add alpha repeatedly; restoring alpha does not undo RGB damage.
Do not compare a sum of raw passes to denoised Combined as if they should match exactly.
AO and data passes are diagnostic/artistic controls, not automatically missing beauty terms.

## Diagnose by looking at the signal

| Symptom | Inspect next |
| --- | --- |
| Empty or wrong matte | Correct file/frame/layer, pass enabled at render time, selection ID/name and saved metadata |
| Jagged depth-driven edge | Z versus coverage/Mist, non-antialiased data semantics, foreground/background discontinuity; blurring Z invents depths |
| AOV looks constant or disappears | View Layer declaration, name/type, shader connection, object material, render support and saved channels |
| Pass sum too bright/dark | Missing/doubled terms, color multiplication, denoise mismatch, alpha and transparent/background handling |
| Local grade makes a dark outline | Premultiplication, nonlinear grade on associated color, selection applied twice, mixed object coverage |
| Looks correct until file reopen | In-memory Render Result dependency, layer/frame selection, omitted passes/manifest, wrong alpha/color-space interpretation |

For post DOF or motion blur, a single Z or vector sample cannot reveal surfaces hidden behind
the foreground. Use camera/rendered effects when their occlusion/optical quality is needed.
Mist is a mapped depth-related control with render-time settings; it is not interchangeable
with a distance-valued Z pass. Preview a data pass with a temporary remapping for inspection,
while preserving the original values for its actual consumer.

Primary references: Blender [render passes](https://docs.blender.org/manual/en/latest/render/layers/passes.html),
[View Layers](https://docs.blender.org/manual/en/latest/render/layers/introduction.html),
[AOV Output](https://docs.blender.org/manual/id/5.0/render/shader_nodes/output/aov.html),
and the original [Cryptomatte specification and implementations](https://github.com/Psyop/Cryptomatte)
([EXR handoff guidance](https://github.com/Psyop/Cryptomatte/blob/master/docs/nuke.md)).
Use current runtime evidence for API and renderer details; source provenance and the actual
test scope are recorded in [provenance](provenance.md).
