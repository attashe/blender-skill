# Technique extraction: sources and verification

The initial six techniques were extracted from three local reference packages on 2026-10-23.
The source assets remain integration evidence, not a dependency for executing the extracted
Python examples. Actual runtime: Blender **5.2.1 LTS**, build **9e2066aef7ef**. Other versions,
arbitrary rigs/topologies and independent-agent effectiveness are not certified by these checks.

| Technique | Source decision / implementation | Extraction check |
| --- | --- | --- |
| Constant rotation | Motor `action()`, linear angle and Repeat Offset | Different named pivot, −37.5 rpm /30 fps; integer/subframe/next-cycle evaluation and carried marker; fresh reopen |
| Pitch coupling | Motor `driver()`, rotation/travel from turns | 12 mm pitch /0.75 turns in a rotated carrier; local/world relationship; then one original motor nut at 1 mm pitch |
| FK pose/phase | Momo `keys()` and staggered tail controls | Independent single-bone rig and owning Action/slot; occupied channel rejected; then integrated pose/tail on Momo |
| Graphical blink control | Momo root property → ShapeKey drivers | Independent shape/control with separate ownership, then original driven eye/highlight shapes |
| Rest pigment | Momo rest_position capture and Attribute routing | Independent panel deformed by >0.69 scene units; evaluated attribute unchanged; saved before/after shader images viewed |
| Cut/bevel | Drilled motor flange's Boolean → Bevel | Independent plate at two radii; actual hole/solid ray tests, closed positive-volume mesh, unchanged thickness and visible edge response |

Original snapshots (optional external archive):

Related assets in this distribution include the [motor](../examples/motor-motion.md) and [Momo rig](../examples/character-gesture.md). The test summaries below describe the original development fixtures. The editable scenes are indexed in [whole-asset examples](../implementation-examples.md).

Extraction changes: explicit caller-owned objects/units, no historical scene names or output
paths in helper execution, no construction on import, slotted-channel access and rejection of
already-occupied animation channels. These small helpers are optional implementations, not a
complete asset-building framework. Inputs such as geometry, actual bone axes, thread clearance
and the closure shape still belong to the task.

The first authored Momo transfer used the wrong sign for this rig's local head axis. An
independent signed-world-pitch check rejected it; the asset-specific pose parameters were
corrected, with the generic helper unchanged. This illustrates why successful key insertion is
distinct from the requested gesture. Original failures and the corrected check are retained.

Extraction report and artifacts
contain save/reopen measurements, images and limits. This is authored execution/visual review,
not a completed independent Pi trial of the new technique structure. The prior whole-asset and
short-card trials do not establish a causal improvement from this revision.

## Anchored shell extension

The seventh technique extracts the fixed support plane and Solidify → Bevel mechanism from
the thin-roof case.
That source has historical 20/40/80 mm thickness/contact checks and was completed with
supervision; it is not proof of independent-agent success.

A fresh authored fixture used a 1.4 × 0.8 panel, a differently sized support, a tilted basis,
30/70/110 mm thicknesses and a separate 6 mm bevel. Evaluated thickness error stayed below
1e-6 scene units, contact gap below 1e-6, with closed consistently wound positive-volume mesh.
The 70 mm saved fixture was reopened and remeasured on Blender 5.2.1 LTS.
Measurements
establish this flat-panel mechanism only. Curved/folded sheets, final appearance and autonomous
Pi discovery of this new card have not been validated by that fixture.

## Geometry Nodes extraction batch

[Bounded patterns](gn-patterns.md) and [instance shader attributes](instance-shader-attribute.md)
extract mechanisms from the GN source package.
The source verified fixed-orientation row/grid/ring and one scalar material attribute. Radial
and tangent orientations are an extension tested in the new small fixture, not inherited
evidence from the historical source.

Blender 5.2.1 authored checks: 14 count/spacing/radius/orientation cases, row zero/singleton,
graph-enforced generation caps, source with nonidentity transform and a parented tilted/scaled
host. Independent modifier values on a shared group, rejected attribute-mode constant write,
save/reopen and 28 unrealized instances were checked. EEVEE images show an asymmetric source
and two material classes; a deliberately missing attribute reader removes the variation.
Index parity produced stripes on this grid, so checkerboard behavior is not claimed.

The helper was also substituted for the row in a copy of the source scene: five changed
placements, with the original grid/ring preserved, then save/reopen. No historical source
files were edited. The first setter attempt used the pre-5.2 API and failed; the installed
implementation uses the probed RNA input owner. Older-version fallback is not runtime-tested.
Batch audit and artifacts.
The later independent Pi ring task found and used both cards. Its saved Cycles scene passed
separate count/orientation/color and changed-parameter checks, but Pi did not finish all of its
own checks within budget. See the trial audit.
Arbitrary nested-instance propagation, export and natural surface scatter remain unverified.

## Material-response extraction batch

[Spatial mix](spatial-shader-mix.md), [interior absorption](volume-absorption.md) and
[sheen](sheen-response.md) extract separately tested optical mechanisms from the
layered-materials package.
The new cards contain short wiring/parameter examples rather than a full material builder.
Those exact snippets were executed on different fixtures in Cycles / Blender 5.2.1 LTS.

New authored checks: spatial mask regions agree with their corresponding endpoint images;
one shared absorption material on 30/80/160 mm closed blocks, compared with density zero;
sheen 0/0.85 on a green sphere under unchanged illumination. All seven comparison images
were rendered again after fresh reopen with matching recorded metrics. The snippets were
also integrated into a copy of the source study, preserving geometry and live upstream group
controls, then saved/reopened. Images were inspected for the relevant response.

Batch report and evidence.
This certifies the bounded mechanisms, not convincing natural wear, measured absorption
coefficients, fine weave/grooming or EEVEE/export behavior. A later independent Pi task found
and applied all three cards but exhausted its budget before comparative renders/report. The
saved scene passed separate optical checks; a linked copper-roughness control had zero effect.
The trial audit separates discovery,
artifact behavior and incomplete autonomous delivery. Short socket/control examples were added
after those observations; their effect on a future Pi run has not yet been measured.

## Bake and UV extraction batch

Five cards extract mechanisms from bake maps
and UV density:
image targets, selected-to-active projection, field transfer, seam-defined strip, density/padding.
The source scripts/images were inspected; full builders stay in the external evidence archive.
The new card snippets are executed on changed fixtures in Blender 5.2.1 LTS, then saved/reopened.
Results, failed attempts and exact boundaries are in the
batch audit.
This is authored validation, not an independent Pi discovery trial of these five cards.
No complex custom cage, organic unwrap, UDIM, trim/lightmap or target-export certification is implied.

## Light and image extraction batch

Seven short cards extract mechanisms from four archived packages: lighting (light-role A/B,
linear/display output), compositor (lobe reconstruction, alpha Over, Cryptomatte exposure),
cel-shading (neutral light signal and palette) and cartoon-lowpoly-cel (independent contours).
The older character supplies a contour mechanism, not an approved artistic form reference.
Integration uses the later smooth Momo for an owned scarf material and contour style.

Actual Blender 5.2.1 LTS checks execute the card snippets on new inputs: differently placed
lights and +0.75 stop exposure, named diffuse/metal/glass/emission samples, a newly persisted
multilayer EXR, +0.5 stop local grade, different fractional-alpha swatches, a blue-green palette,
new thresholds and three keyed light directions. Pass reconstruction agrees within 6e-6;
zero/missing selections and deliberately wrong alpha, coverage and omitted emission are
checked. Three occupied palette regions, threshold/light response, a one-color negative
control and two contour widths are measured and viewed. This is Combined/EEVEE cel output.

Fresh-process reopening repeats the small fixtures. Light, comp and cel fixture results match
their saved baselines. In copies of the source studies, geometry and original material graphs
are preserved; the new scarf material/style is separately owned. Reopened Momo differs by at
most 1.31e-4 in RGB, with five pixels above 2e-5 and mean difference below 1e-9; it is not
bit-identical. Source light and comp integrations match their comparison renders.

The integration exposed premature relative image paths before Save As. The extracted route
now keeps the added dependency absolute through the first save and checks its resolved path
after relocation. Original failures, corrected metrics and actual images remain in the
batch audit.
The archived sources and previous independent-test inputs are unchanged.

These are authored mechanism/integration checks, not a new independent Pi discovery trial.
They do not certify an artistic lighting preset, full character motion/contour stability,
occluder-heavy cel shots, volumes, deep/refraction compositing, arbitrary pass sets, export
or other Blender versions. Mixed-object Cryptomatte grading remains approximate.

## Rig and deformation extraction batch

Seven cards extract bounded mechanisms from mechanical-rig (IK bend-plane diagnostics and
rigid Child Of handoff), rig-controls (IK → FK matching, native visual pose bake, shape-before-
skin data flow) and deformation (weight partition and Preserve Volume A/B). The source scripts,
subsequent pole/weight repairs, case limits and actual comparison images were inspected.
No whole source builder is required by the installed cards.

Blender 5.2.1 LTS authored checks execute the exact snippets on new names, bone lengths,
rest profiles, transformed roots, targets, attachment events and shape activation angles.
Matching/world mesh errors remain below 1e-6; a wrong pole angle preserves endpoint accuracy
while failing the plane check. Attach/release preserve same-time poses and hold offsets.
Native bake matches integer frames, but a half-frame mesh-coordinate error around 0.00191
scene units remains. No subframe-equivalence claim is made. The source/baked integer-frame
images were also compared, separately from the numeric interpolation check.

A 792-vertex sleeve with 100-degree twist retains about 42.2% of its minimum rest section
under linear skinning and essentially 100% with Preserve Volume. In tested bend/twist poses,
a narrow normalized weight transition has 43 nonadjacent triangle intersections; the wider
profile has none. Rigid-cuff distances, sums, replacement of now-zero weights, preservation of
an unrelated mask and detection of a nonexistent deform-bone group are checked independently.
These are sampled technical surfaces, not a guarantee for arbitrary skinning/anatomy.

A base-space shape delta with 75-degree local activation is compared with analytic linear
skinning; wrong post-skin delta application fails. Neutral, reverse bend, intermediate and
saturated values are tested. Its visible effect is not described as an anatomical improvement.
The mechanisms are also integrated in copies of the original manipulator, two-chain rig,
sleeve and shape fixture with changed controls/profiles. Fresh-process reopening repeats
nonsequential poses and compares evaluated results. Archived sources remain unchanged.

Batch audit and images
record values and scope. This is authored validation, not a new independent Pi discovery/apply
trial. FK → IK matching, wrist orientation, continuous switching, arbitrary parent/shear modes,
facial/anatomical correctives, retargeting and target export are not certified by these cards.

## State and motion extraction batch

Seven bounded cards were extracted from particle-state (fractional birth/ID, survivor step
and packed GN replay), sparks (actual settled support and age-driven appearance) and
rigid-hinge (local-Z constraint frame and evaluated world-cache replay). Relevant source
scripts, contact repair, saved metrics and images were inspected; whole builders stay outside
the routine discovery path. Small card snippets and corresponding GN mappings were exercised
on new fixtures, then composed in copies of all three source scenes.

Blender 5.2.1 LTS: 9.5 births/s with fps_base 1.25 gives 13 accepted births at effective
24/48 FPS before the emission stop; a capacity of three accepts seven while retaining unique
IDs. Constant-acceleration errors are below 1.3e-6; birth locations remain independent of
subsequent emitter motion. Zero-rate rebake empties the effect. A saved packed cache masks
an upstream rate edit until the owned bake is deleted. Fresh-process nonsequential seeks
match compact state exactly. API tests exposed the active-object poll requirement even for
addressed bake operations and the ineffective hidden Set ID default (implicit Index);
the cards use explicit context and linked ID fields.

New irregular grains use measured transformed support for multiple scales/orientations
and a tilted plane; nominal-radius contact leaves up to 0.0933 units of gap. Geometry support
error is below 1e-7. The source sparks are retested at count 61, lifetime 1.1 s and radius
0.02: 57 settled particle/frame groups have zero actual lower-vertex gap. An independent
age-driven rendered sample fades; a disconnected shader retains changing heat attributes
but constant pixels. This is designed appearance, not physical temperature or collision.

A new rotated hinge is compared with disabled, wrong-axis and asymmetric-limit variants.
Base pivot drift is 2.33e-5 units; a changed limit produces a distinct stop angle. Object order
and angle sign are checked instead of assuming world Euler limits. The original assembly
with a longer 1.45-unit rod has up to 0.00228 units of pivot error; it is not exact physics.
Rigid-body world caches and all three integrated scenes replay after reopening. Technical
images were viewed. No arbitrary colliders, motors/chains, subframe equivalence, cross-version
cache compatibility, large-scene performance or independent Pi discovery is certified.

Batch audit, logs and images.

## Delivery extraction batch

Seven cards extract GLB scope/clip/timebase, surface round-trip and payload inspection from
glb-roundtrip, plus linked override updates, native snapshots, owner-relative resources and
clean relocation from asset-handoff. Relevant source scripts, packed-resource repair evidence,
saved scenes/metrics and actual images were inspected. Full assets remain integration evidence,
not required builders. Python snippets execute from the actual candidate Markdown cards.

Blender 5.2.1 LTS checks use new hierarchy dimensions, asymmetric UV texture, mirrored shared
mesh, nonuniform parent scale, root and hinge animation, and fps_base=1.25. Source/import world
positions agree within 4.93e-7 scene units after the tested export representation is prepared;
UVs, normals and area are checked separately. Three unique meshes remain four mesh instances;
8 source vertices become 24 export vertices per mesh. Deliberate UV shifts leave the spatial
check passing but fail UV and image checks. A vertex displacement fails the spatial check.
GLB payload counts and embedded pixels are measured; no engine frame-time claim is made.

Two real export-boundary issues were found. Installed exporter/importer code multiplies fps
by fps_base: a 1.25-second source becomes 0.8 seconds, while same-setting reimport still matches
the tested frame. A delivery copy at equivalent integral 24/1 FPS restores correct duration;
the authoring source stays at 30/1.25. SCENE defaults to split-object clips, so root motion can
play while the separate hinge clip is inactive. The bounded profile explicitly merges the clip
and checks both members. Original failures, wrong outputs and targeted API evidence are kept.

Two new linked consumers retain different local positions/animation after source thickness
0.35→0.56 and a new hierarchy member. Append/Pack snapshots retain v001 and correct pixels.
An isolated negative packed-linked image has a packed flag but size 0×0. A same-basename decoy
in the shot folder proves the need to resolve against the library owner. External Alembic
motion replays out of order. Both new and historical-source packages are copied, opened fresh
while only their disposable source copies are temporarily unavailable, then sources restored.
Before/after images match exactly. Historical consumers also retain new local edits across a
0.6→0.69 source update; newly made snapshots remain at 0.6. Source archives remain unchanged.

Audit and images
record exact checks and limits. No independent Pi discovery/apply trial, Khronos validator,
external engine, skin/morph export, LOD/lightmaps/collision, complex override hierarchy,
cross-version cache compatibility or Asset Browser UI discovery was tested in this batch.
These authored mechanisms close extraction from the initial twenty packages, not every
possible mechanism or Blender production requirement.


## Window transmission extraction

Author study in Cycles 5.2.1, separate from Pi. A manufacturer glass photo was viewed in
the browser, and both pages of the Kvadrat Air 4 reference PDF were inspected. The extracted
mechanisms are an etched boundary on a closed pane, and thin-sheet scattering with separate
mean coverage. Reference images are not used as textures or copied into the installed skill.

Four fixed-view glass images compare clear/rough treatment with near/far backgrounds. Five
fabric images separate opaque, diffuse-transmitting and open-area branches, double layers
and front/back lighting. The assembled window includes an actual wall opening, separate
panes/frame, static folded sheet and doubled hem. Overlapping frame faces in the first
author render were corrected before delivery. Existing assembly-fit guidance covers this;
it did not justify a new scenario-specific diagnostic tool.

The exact Python snippets from both candidate cards were executed in a fresh process on the
saved fixtures, then rendered and compared. The final window was reopened and rendered.
No new full-asset builder or shader helper is required to use these short operations.
The textile uses averaged unresolved holes, not explicit yarn geometry or measured BSDF
data. Product-specific haze/transmittance, close-up weave, dynamic draping, EEVEE equivalence
and independent Pi discovery/application remain unverified.

Study, images and exact checks.


## Upholstery and plastic extraction

Author study, Cycles 5.2.1. The Brisa Natural polyurethane swatch was viewed at high
resolution; Vitra furniture photos supplied smooth shell/edge/reflection cues. Neither
source supplied calibrated optical values or verified grain dimensions. Manufacturer
pixels remain references, not textures or redistributed skill assets.

A small furniture sample established curvature and finish boundaries before adding relief.
Upholstery comparisons isolate embossed height, optional coat and doubled nominal spacing.
Plastic comparisons isolate fine relief and roughness. Its initial close view lacked a
useful highlight, so the camera moved to a rounded edge with a narrow reflected source.
The chosen satin finish suppresses much of the fine grain; the smoother diagnostic finish
reveals it more clearly. Numeric pixel differences alone do not certify resolved texture.

The helper extracts only normalized height; it supplies no full material or object builder.
Both candidate Markdown snippets run in a fresh Blender process, including a changed grain
spacing. The saved final scene is reopened and rendered. Exact measurements and comparison
results are in the audit.
No product-specific optical match, natural leather, deforming upholstery, physical coating
thickness, EEVEE/export equivalence or independent Pi discovery/application is certified.


## Apartment composition integration

The authored 5.2.1 study reuses cabinetry, metric veneer, tile, glazing, textile and chair
finishes in one existing room. It exposed a stale unlinked `matrix_world` and a mutated
name-list alias during `libraries.load`. The snapshot card now evaluates after linking;
a translated/rotated parent-child regression executes its exact snippet. Host lighting and
camera views are reviewed separately from the original material sample rigs. The wider
cabinet keeps 60 mm stiles and 0.5 metres per UV unit. Source geometry preservation, actual
sink opening, selected shell orientation, occupied clearances and fresh reopen are recorded
in the report.
This is not independent Pi evidence, a finished kitchen appliance layout, building-code
verification, animated clearance testing or a completed apartment.
