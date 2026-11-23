# Interchange profiles: choose only the needed route

Read the selected profile with [the export workflow](export-workflow.md). Use actual installed
exporter and receiver versions; these are decision patterns, not frozen operator presets.

| Required handoff | Candidate | First discriminating test |
| --- | --- | --- |
| PBR asset, scene hierarchy and supported runtime animation | glTF/GLB | Textured asymmetric asset, shared mesh and required clip in the receiver |
| Engine/DCC mesh or skeleton through an established importer | FBX | Units/pivot, smoothing/tangents, skeleton rest pose and material conversion |
| Scene assembly, references, richer interchange and sampled data | USD/USDZ | Supported schema, composition/instancing, materials and resolved dependencies |
| Baked evaluated geometry/motion | Alembic | Timing, topology, normals/UVs and nonsequential cache replay |
| Simple static surface or fabrication boundary | OBJ/PLY/STL as specified | Units, winding, attributes and the actual downstream requirement |

## glTF / GLB

Use glTF 2.0's declared PBR/geometry/animation model and only extensions the receiver supports.
GLB is a binary container; `.gltf` commonly uses JSON with companion buffers/images. Inspect
actual resource URIs/buffer views rather than assuming the suffix makes a package self-contained.

Confirm supported Principled/image wiring in Blender's exporter. Base color, metallic and
roughness have explicit meanings; metallic/roughness image data uses the format's B/G channel
mapping. Do not repack by guessing another engine's convention. Shader Noise, arbitrary mixed
closures and GN graphs are not portable executable Blender graphs. Bake or reconstruct only
the unsupported behavior required by the chosen look; verify color, roughness, normals and alpha.

Check mesh reuse across nodes separately from GPU-instancing extensions. A receiver can share
geometry without issuing one draw call for all occurrences. Named LOD/collision/lightmap data
does not acquire standardized runtime behavior merely by being present in a core glTF asset;
use the receiver's conventions/extensions or a sidecar and verify the consumer.

Inspect `extensionsUsed`/`extensionsRequired` and decoder availability before enabling mesh
or texture compression. Establish an uncompressed baseline, then compare decoded shape, normal
maps, animation, load cost and bytes. An exporter setting's presence is not proof of receiver
support. Run an available [Khronos validator](https://github.com/KhronosGroup/glTF-Validator)
for format diagnostics, plus real import/view tests; report when only focused checks were run.

Select the intended actions/scene range and sample constraints where necessary. glTF animation
uses time in seconds; compare duration and intermediate poses after import. Inspect skin and
morph data only if used. Blender-import success does not guarantee the same extensions in a
web engine. Sources: [Blender glTF guide](https://docs.blender.org/manual/id/5.0/addons/import_export/scene_gltf2.html)
for stable concepts, current runtime for flags, and the [glTF 2.0 specification](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)
for the interchange contract.

## FBX through an engine or DCC importer

Match the project's supported FBX/exporter/importer combination. Define units, forward/up,
pivots and root transforms once. Inspect smoothing/tangents and any triangulation or export-only
modifier application. For skeletal delivery test rest pose, bone axes, influence limits,
root motion and clips; do not apply transforms indiscriminately to the authoring rig.

FBX material transfer is a restricted translation, not preservation of arbitrary Blender nodes.
Rebuild the target shader or provide tested maps. For engine collision/LODs/sockets, use that
importer's naming/selection rules rather than a universal Blender convention. For example,
Unreal's FBX static-mesh route recognizes named collision meshes; check association and importer
limitations on multiple meshes, then test the actual opening/contact in the engine.
See [Epic's FBX static-mesh pipeline](https://dev.epicgames.com/documentation/unreal-engine/fbx-static-mesh-pipeline-in-unreal-engine)
and [Unity handoff](unity-handoff.md); their behavior is not interchangeable.

## USD / USDZ

Choose supported schemas for hierarchy, transforms, mesh/curve/point/volume data, instancing,
materials and time samples. USD's broader capabilities do not imply that a particular Blender
export preserves every composition arc, rig or shader. Check Preview Surface/MaterialX and
receiver support explicitly; material conversion may approximate the source.

Verify stage units/up axis, reference/texture/cache resolution, instance treatment, topology
and animated material/subset behavior. Distinguish reusable referenced scene structure from
an evaluated flattened export. Test a clean location and a source update if composition is
part of the deliverable. A USDZ package also needs a dependency check. Consult the matching
Blender/receiver docs; [Blender's USD guide](https://docs.blender.org/manual/id/5.0/files/import_export/usd.html)
describes supported-data and conversion boundaries, not a guarantee for future versions.

## Alembic and simple static formats

Alembic is useful for evaluated transforms and geometry caches. Decide frame range, time scale,
sampling/subframe motion and supported attributes. Check animated topology, normals, UVs and
instancing in the actual receiver. Preserve material resources and the editable rig/solver
separately when requested: a cached result is not its procedural authoring system. See
[Blender's Alembic guide](https://docs.blender.org/manual/pt/latest/files/import_export/alembic.html).

For OBJ/PLY/STL, confirm the required attributes and downstream interpretation before choosing
the route. Verify physical dimensions explicitly where units are not reliably carried or
interpreted. Static mesh exchange does not provide a general rig/animation/material pipeline;
fabrication may additionally require a valid closed oriented solid. Apply those requirements
to the declared consumer rather than making every Blender surface watertight.
