# Sources and validation limits

This skill combines Blender production workflows with small, independently authored Python helpers. The [technique notes](techniques/provenance.md) describe measurements from the original tests, their conditions and limits. The [bundled examples](implementation-examples.md) include editable geometry and animation for repeating selected checks in another project. Compare evaluated geometry, motion and the intended view after reopening your own output. The manifest checker verifies declared relationships and freshness.

## Original implementation sources

The upstream access and compatibility notes below are retained from the original package;
those repositories were not re-audited during the production-workflow refactor.

- [vinhelysia/blender-mcp](https://github.com/vinhelysia/blender-mcp), MIT: its README documents
  inspecting the scene, making a scoped change, and validating numerical results. That documented
  loop informs this workflow. The individual upstream SKILL.md could not be fetched in this run;
  do not describe this package as a patched copy of that file or its MCP bridge.
- [NodeCue geometry-nodes SKILL.md](https://github.com/nodecue/blender-node-skills/blob/main/skills/geometry-nodes/SKILL.md),
  MIT: the skill was read directly. It informs the live identity/introspection and evaluated-output
  workflow. The repo is archived. Its reported paired test motivated keeping the entrypoint short
  instead of importing a broad static node catalog. No upstream scripts are copied here.
- [ahujasid/mcp-for-blender](https://github.com/ahujasid/mcp-for-blender): the user's established
  community connection is an execution option. It is distinct from Blender Lab MCP; do not
  exchange their tool names, ports, or installers based on similar names.
- Consult official Blender versioned manuals/release notes linked in `blender-methods.md`.
  Future agents must check the installed runtime; “latest” web documentation can move.

## Production workflow sources

Reviewed for the 2026-10-22 refactor. These are production accounts informing the decisions,
not a claim that all studios use one fixed pipeline or that their add-ons must be installed.

- [Blender Studio Asset Pipeline](https://studio.blender.org/tools/addons/asset_pipeline):
  configurable task layers, ownership and different publication states inform the separation
  between editable work and consumer-ready assets. Only indexed documentation was inspected
  for this source in the refactor session. This skill does not
  implement or require that add-on or its merge behavior.
- [Ask Epic: Art Production, response by Saga Alayyoubi](https://forums.unrealengine.com/t/ask-epic-art-production-january-25-2024-10-am-et/1626687?page=2):
  early layout and lighting, then reuse decisions based on the scene, inform the feedback loop.
- [Shira Eilan's Asha production breakdown](https://www.unrealengine.com/developer-interviews/exploring-asha-go-behind-the-scenes-of-a-rookie-award-winning-game-environment?lang=en-US):
  a concept establishes direction while additional material, foliage and pattern references
  answer details; this informs the distinction between reference roles.

The reference inspection loop, decision gates and modularity guidance are this package's
synthesis for an agent. They are not verbatim studio procedures. Detailed branches cover
scoped blockout delivery, modeling, modifiers, Geometry Nodes, shaders/material composition,
UV layout, texture authoring/baking, placement, curves, animation, particle effects, production lighting and
rendering. Compositing remains a separate specialist branch; its render-input handoff is
present in the production map, which also lists other remaining specialist branches.

## Tool-workflow sources

The versioned sources and access/verification distinctions are listed in
[recent Blender features](recent-blender-features.md). Feature claims were checked against
official indexed release documentation on 2026-10-22; direct developer-document page retrieval
was unavailable. The curve, scatter and animation guides also link the specific manuals/API
notes used. Older versioned manual pages support conceptual guidance only; the installed
runtime and corresponding current documentation remain authoritative for implementation.
