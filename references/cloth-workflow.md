# Cloth: establish support, folds and stable contact

Use for drape, hanging fabric, garments and pressure-driven cloth forms. Read the relevant
pattern plus [shared simulation decisions](simulation-workflow.md), not every physics branch.
Keep woven appearance in [materials](surface-families.md); shading does not create folds.

## Choose the physical question

| Pattern | Starting structure | Characteristic test |
| --- | --- | --- |
| Tablecloth or cloth dropped over a form | Modest even sheet, separated from a supported collider, gravity and sufficient settle time | Edge drape and one sharp/rounded contact; no floating cushion or deep penetration |
| Flag or curtain | Pinned edge/points, deliberate rest shape and gravity/wind | Attachment stays fixed or follows its animated support; waves and folds evolve coherently |
| Garment/cape over an animated body | Suitable rest fit, pin/weight zones and simple animated body collision | Body bends through a difficult pose without trapped fabric, stretching or underarm failure |
| Cushion/soft bag | Closed coherent mesh, pressure only when the intended form requires it | Expansion, seams/support and contact under loading; no leaking/open pressure shell |

Presets can initialize a material class, but resolution, scale and construction still affect
the result. Tune mass, stretch/shear/bending response and damping by observed fabric behavior.
Expose pin regions, wind and meaningful stiffness/shape controls; do not assign one set of
numbers to every fabric or infer real material calibration from a convincing short shot.

## Resolve the simulation mesh and stack

Use enough regular geometry for the required folds, with sensible aspect ratios and no
accidental duplicates or self-intersections. More vertices can increase instability and cost
without fixing fit. Keep thin sheets for ordinary cloth; a thick modeled shell creates a
different collision problem. Add visible thickness and finishing subdivision after simulation
when that is the intended construction. If subdivision occurs before the solver, it changes
simulated topology and needs its own budget and cache. Check viewport/render levels consistently.

For a garment, decide which deformation produces the start/rest or moving pinned input and
which deformation happens after simulation. Armature-before-cloth is not interchangeable with
armature-after-cloth. Use Dynamic Mesh/rest-shape options only when the chosen behavior needs
them; inspect rest lengths, pin weights and actual moving anchors. A vertex group existing by
name does not prove its membership or that the solver uses it. Review an extreme pose early.

In classic Cloth, the obstacle needs Collision physics and the cloth needs the intended
object-collision collection/settings. Set collision distances against edge lengths and physical
scale. Excessive distance creates rounded folds and visible hovering; very small distance
with fast/thin contact can miss collisions. Check both sides of a sheet and first impact.
Enable self-collision where folded regions need it, with appropriate exclusions for intended
seams/attachments. It adds work and can fight incompatible pinning or an overlapping start.

Diagnose an explosion in order of evidence: initial penetration/duplicate geometry, moving
collider or pin discontinuity, scale/rest state, mesh sampling, then time/collision quality.
Test a smaller segment or simpler collider before turning every quality setting up. Change
one consequential factor at a time and rebake its dependent state.

## Pattern-based garments

For a pattern-based garment, establish body measurements/ease, panel shape and seam pairing
before tuning cloth parameters. Sew and settle a fitting state before testing shot motion;
do not use stronger forces to pull an incorrectly sized pattern into place. The author's
[tailoring course outline](https://blenderartists.org/t/a-tailors-approach-to-cloth-sewing-in-blender-full-course/1408223)
separates measurement, drafting/cutting, assembly and finishing. Its public outline is a
case-study route, not a claim that the full video course was inspected. In classic Cloth,
sewing uses loose edges between intended pairs; bound sewing force and inspect seam closure
before delivery. See [Shape](https://docs.blender.org/manual/zh-hant/5.2/physics/cloth/settings/shape.html).

Measure paired seam separation after settling, then exercise the fitted garment against a
moving body. Closed seams alone do not prove fit or collision. Inspect surface triangles as
well as vertices around narrow contact: a triangle can cross a collider with its corners
outside. For pressure forms, review the inflation ramp, supported volume and deformation
under loading. Even sampling across the shell matters; tiny side edges can stretch severely
while a whole-object average looks acceptable. Pressure is a shell model, not a simulated
interior liquid; see [pressure behavior](https://docs.blender.org/manual/ko/5.2/physics/cloth/settings/physical_properties.html).

## Current GN dynamics are a separate route

Blender 5.2 introduced experimental **Cloth Dynamics** assets backed by XPBD. Resolve the
installed asset and interface; a GN asset label is not an ordinary modifier enum. These assets
support constraints/effectors through their own data contract and use their own GN state/bake
route. Classic Cloth settings or classic Collision modifiers cannot simply be assumed to drive
them. Start with the packaged asset before attempting a custom XPBD world/typed-bundle graph.

Choose it when an isolated test proves the needed behavior and the project accepts its version
dependency. Preserve source/rest geometry and inspect actual collider/force inputs, pinning,
substeps and constraint residuals when available. A Simulation Zone or XPBD node alone does
not establish cloth structure. Keep a supported classic or baked delivery route where needed.

Check capability before choosing this route for folded/layered cloth: the tested 5.2 XPBD
solver supports external mesh contact but **no self-collision**, and its cross-edge bending
has documented limitations. Classic Cloth self-collision settings do not add that feature to
GN Cloth. See the [current solver limits](https://developer.blender.org/docs/features/nodes/xpbd_solver/).
Where an installed asset exposes tearing, compare an untorn control and inspect actual
topology changes, fragment motion and downstream material/attribute/cache handling. A label
or an extreme threshold causing an immediate explosion of disconnected faces does not prove
a useful progressive tear. Keep tearing unvalidated if a bounded probe cannot establish it.
If animated input geometry is meant to stretch the cloth, inspect the constraint rest lengths
over time: updating the rest state alongside that animation can remove the intended strain.

## Review folds over time and after reopening

Inspect a side/low contact view and the delivery view at first contact, maximum deformation,
settled state and adjacent frames. Check anchors, stretch, fold quality, self-penetration,
support gaps and finite bounded geometry. Cache with the chosen solver, save and test direct
seeking after reopening. Changing upstream topology/rest pose/pins/colliders invalidates the
result even if the old cache still draws. A single drape test does not validate garments,
tearing, pressure, extreme motion or every fabric class.

Sources: [classic settings](https://docs.blender.org/manual/ru/5.2/physics/cloth/settings/index.html),
[collision behavior](https://docs.blender.org/manual/id/5.0/physics/cloth/settings/collisions.html),
[cache/mesh-level cautions](https://docs.blender.org/manual/nl/5.2/physics/cloth/settings/cache.html),
[5.2 experimental physics](https://developer.blender.org/docs/release_notes/5.2/physics/), and
[XPBD inputs and results](https://docs.blender.org/manual/sv/5.2/modeling/geometry_nodes/simulation/xpbd_solver.html).
Older collision documentation supports the classic concepts; inspect current properties.
