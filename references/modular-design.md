# Design modular assets within production

Read when planning reuse, source ownership, a kit, or a scene refactor. The aim is to make
useful change propagate predictably while preserving visual quality. More files, more nested
collections, or a more elaborate generator are not inherently better modularity.

## Separate three decisions

1. **Visual/construction decomposition:** which masses, repeated structures and unique features
   explain the reference and scene? This informs modeling and kit design.
2. **Reusable asset boundaries:** what needs independent reuse, replacement, variation, motion,
   surfacing or delivery? This defines identity, ownership and interfaces.
3. **Storage and assembly:** should those sources be collections/datablocks in one file, linked
   library files, procedural groups, or a combination? Choose for the project's actual needs.

Do not equate a physical component, a mesh object, an asset, and a `.blend` file. One asset can
contain several meshes, materials and helper objects. A simple prop can remain one source.
An environment can combine a modular architectural kit with unique terrain and hero objects.

| Boundary signal | Useful consequence |
| --- | --- |
| Repeated in several places | Share a source and instance it; changes propagate consistently |
| Replaced or varied independently | Define a stable pivot/socket, fit envelope and variant interface |
| Animated/deformed separately | Separate the appropriate motion/rig responsibility; preserve clearance |
| Shared material or procedural logic | Reuse the material/node group with an intentional interface and durable asset identity |
| Different publishing/editing lifecycle | Consider a separate source file and explicit dependency |
| Unique detail with no independent use | Keep it inside its owning asset; split only if a concrete benefit emerges |

Avoid a file per screw or per visible surface. Avoid a monolithic generator that prevents a
single meaningful part from being edited/replaced. Use the simplest representation that
supports the expected change and current scale.

## Define the contract before replication

Specify only the fields that affect consumers:

- Identity and authoritative source/root; dependencies and who owns shared data.
- Units, local axes, pivot and placement convention; dimensions or fit envelope/tolerance.
- Attachment sockets or grid/step rules where placement depends on them.
- Material slots, surface/UV scale and seam expectations where assets meet.
- Allowed shape/material variants and motion/clearance requirements.
- Budgets derived from target views/device, including expected occurrence count.

Use one coherent grid for a snapping kit when appropriate; not every organic or artistic
assembly needs a grid. Define whether a socket represents a surface, centerline or mating
plane so its meaning survives a model revision. Keep inspection lights/cameras out of the
public asset root. A library's dependencies include textures, materials, node groups and
required caches as well as other geometry.

## Prove the kit in context

Use the blockout and reference breakdown to select a small representative sample. Check a
straight/repeated run plus the transitions actually needed: a corner, opening, end cap,
height change or a different-size neighbor. For mechanical assemblies, test the mating
interfaces and motion envelope instead. Test useful combinations, not a universal checklist.

Inspect scale, snapping, seams, normals, UV/material continuity, intended intersections and
viewing-distance readability. Place enough occurrences to expose repetitive patterns and
aggregate cost. Test one useful parameter or variant change. Discovering a seam or pivot error
here is cheaper than correcting every placement later.

Keep a stable set of core shapes. Add variation through purposeful variants, materials,
decals or set dressing when the brief benefits. Randomness does not automatically improve
composition, and tiny modules can multiply placement and rendering overhead. Shared mesh data
does not by itself prove fewer draw calls; measure in the actual target.

## Keep authoring, exploration, and release distinct

`part → assembly → module → scene` names useful responsibility levels, not compulsory stages.
Skip levels and nest coherent assemblies where useful. Keep dependencies acyclic; a reusable
part must not depend on the scene that places it. Scene-specific connecting geometry still
needs an owner, but need not become a reusable catalog item without a reason.

Build exploratory layouts from proxies immediately. Replace them progressively with reviewed
assets. Treat consumer-ready releases separately from in-progress variants, so an experiment
does not silently alter a finished scene. Source names/IDs and interfaces should survive
routine edits; record intentional interface changes and update affected consumers.

For linked libraries, prefer relative paths and stable root collections. Modify source
geometry in its own source, then reload consumers. Use overrides for a deliberate per-instance
need; append when creating an intentionally independent owned variant. Document that choice
instead of accidentally forking a reusable source. Where scripts help, organize them by asset
or production responsibility; no particular folder tree or builder API is required.

For a refactor, checkpoint first, inventory current dependencies and compare representative
before/after views, bounds, transforms and materials. Extract incrementally and verify each
replacement. Avoid repeatedly clearing the user's live scene. Test a controlled source update
through its consumers and restore a test-only change before delivery.

For Asset Browser catalogs, import ownership and shared-source updates, use
[asset libraries](asset-library-workflow.md). For saved resources and portable native packages,
use [project handoff](project-handoff.md).

## Choose the tracking implementation

For a small local asset, named collections plus concise project notes may be enough. For
cross-file reusable assets, keep an explicit inventory of source identities, dependencies,
contracts and readiness. Use the existing project's format where available.

The bundled [manifest profile](manifest-contract.md) provides a stricter implementation:
one `.blend` per node, one public collection, typed dependency levels, budgets and evidence
freshness checks. Use it when that file structure fits, and retain it where already adopted.
It does not support several separately tracked nodes in one `.blend`, arbitrary dependency
types, or artistic production stages. Do not claim those capabilities or falsify entries to
make a different organization pass. A needed profile migration must preserve checks and be
handled explicitly; a failed gate is a problem to fix, not a reason to discard the contract.

Source ownership, bounded procedural work and visual review still apply outside that profile.
The technical tools are described in the profile so the main production guidance remains
independent of a particular command sequence.
