# Carry the hierarchy into Unity

Keep the same ownership graph: Blender source part → imported mesh/model → assembly prefab →
module prefab → scene. This is a workflow mapping; use the project's Unity version, exporter,
import pipeline, and render pipeline documentation before implementing it. Start with the
[export contract](export-workflow.md) and [performance checks](performance-workflow.md);
choose the actual supported [format](export-formats.md), not a filename convention alone.

| Blender authoring unit | Unity responsibility |
| --- | --- |
| Part source `.blend` | Owned exported model and its import settings; materials/textures |
| Assembly root collection | Prefab nesting verified part prefabs/models |
| Module collection with sockets | Module prefab containing assemblies, colliders, controls |
| Final scene with linked modules | Scene placing module prefab instances and scene services |

- Prefer an explicit export folder and a declared interchange format supported by the actual
  project. Avoid silently making Unity depend on a developer's local Blender installation.
- Preserve `.blend` sources; realize instances, apply export-only modifiers, and triangulate in
  controlled export copies only when the chosen format/importer requires it.
- Define one unit/axis conversion contract. Blender authoring uses meters/Z-up in the example.
  Validate imported dimensions and orientation in Unity; do not add an unexplained manual
  90-degree rotation in several different stages.
- Preserve stable asset identity and existing Unity `.meta` GUIDs. Update files in place;
  rebuild only dependent prefabs/exports. Do not replace scene references with duplicate meshes.
- Export node materials to supported shaders or bake them. Geometry Nodes graphs and Blender
  simulations do not automatically become executable Unity systems. Export geometry, animation,
  caches supported by the project, or implement the intended behavior in Unity.
- Keep colliders, LODs, bounds, material count, lightmap UVs, and prefab behavior explicit in the
  target-side acceptance checks. Measure actual runtime draw calls, frame time, and memory.
- Test replacing one part and reimporting: existing prefab references should remain valid and
  module placement should remain correct. Inspect the scene and play-test requested behavior.

The supplied Blender audit/checker does not inspect Unity prefabs or `.unity` YAML and is not a
Unity test runner. Connect equivalent target-side checks before claiming a Unity deliverable passed.
