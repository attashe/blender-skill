# Find the next operation

Choose the smallest entry matching the task. A **technique** gives an input contract,
mechanism and check; a **guide section** helps choose or diagnose a method. A **recipe**
combines operations. None requires loading its source asset. Search terms below include
ordinary task words, not just Blender feature names.
When the helper already covers the operation, prefer calling it with the task's parameters
for the first sample. Rewrite its internals when the required mechanism differs; reading a
working helper then retyping its API plumbing can reintroduce errors it already resolves.
Stop reading when inputs, effect and verification are clear; open a dependency only to
answer the next unresolved question.

## Hard surface

| Need / search terms | Smallest useful entry | Boundary |
| --- | --- | --- |
| Hole, cutout, recess, rounded edge, bevel | [Cut → Bevel](techniques/cut-bevel.md), small helper | Coherent operands and measured radius/clearance |
| Sheet, panel, roof, wall thickness, support contact | [Anchored shell](techniques/anchored-shell.md), small stack | Flat source with intentional normal and contact side |
| Extrude, inset, mirror, subdivision, fit to surface | [Modeling choices](modeling-workflow.md#practical-tool-choices), guide section | Choose construction for the reference and target use |
| Stack order, clamping, pinching, apply modifiers | [Modifier diagnosis](modifiers-workflow.md#debug-the-stack-before-applying-it), guide section | Inspect evaluated geometry; retain editable source |
| Normals, reversed faces, zero thickness, new mesh helper | [Shell orientation](techniques/mesh-orientation.md), read-only probe | Per-component winding/topology; thickness and intended cavities need their own checks |
| Seam, gap, mating parts, assembly fit, blocked opening | [Assembly fit](techniques/assembly-fit.md), read-only spatial probe | Ordered extent gap or first actual occluder; not a universal collision test |

## Curves and profiles

For an editable horn, root, hose or rail with taper, roll and a custom section, use the [editable sweep](techniques/editable-sweep.md).

## Architectural surfaces

| Need / search terms | Smallest useful entry | Boundary |
| --- | --- | --- |
| Tile size, grout seam, backsplash, border cuts, layout phase | [Tile field and junction](techniques/tile-field-junction.md), small layout helper | Rectangular planar field; preserves tile size, returns actual edge cuts |

## Animation

| Need / search terms | Technique | Boundary |
| --- | --- | --- |
| Spin, motor, wheel, constant signed rpm | [Unwrapped rotation](techniques/constant-rotation.md) | Known Euler pivot; not physics or automatically a visible loop |
| Rigify foot placement, planted support, hand reach, two keyed IK targets | [Rigify IK animation](techniques/rigify-ik-animation.md) | Generated rig, active IK, unchanged parent space |
| Screw, nut, thread pitch, rotation plus travel | [Thread pitch](techniques/pitch-coupling.md) | Known axis, units, handedness and assembled offset |
| Nod, gesture, lead/follow, delayed tail, FK keys | [FK pose/phase](techniques/fk-phase.md) | Existing rig and supported pose range |
| Blink, property-driven shape, facial control | [Graphical blink](techniques/driven-blink.md) | Existing shape; not eyelid construction |

Combine through [mechanical motion](recipes/mechanical-motion.md) or
[character gesture](recipes/character-gesture.md). For broader timing/camera/clip choices,
use [animation](animation-workflow.md). For constructing a rig or repairing skinning, use
[rigging](rigging-workflow.md) or [deformation](deformation-workflow.md).

## Rig and deformation

| Need / search terms | Smallest useful entry | Boundary |
| --- | --- | --- |
| Local lift, rock shoulder, change proportions with an editable cage | [Fitted lattice and region lift](techniques/lattice-region.md) | World-space falloff on rest controls, check surface displacement and contact |
| Locate a skinning defect on a posed limb, find affected vertices, compare mirrored weights | [Find a skin-weight defect by vertex](techniques/mirrored-skin-weights.md) | Match rest-space pairs and check the candidates on the posed surface |
| Rigify Basic Human, metarig fit, automatic weights, hand IK, diagnose an elbow crease or fold | [Fit, bind and pose with hand IK](techniques/rigify-basic-human.md) · [Measure elbow bend](techniques/arm-front-of-chest.md) | For a crease, confirm the shoulder–elbow–wrist angle changes before inspecting the skin |
| Look left or right, head turn, ear toward shoulder, head tilt | [Turn and tilt a Rigify head](techniques/rigify-head-direction.md) | Anatomical axes, signed angles and evaluated skin |
| Elbow/knee twists out of plane, pole, endpoint right but joint wrong | [IK bend plane](techniques/ik-bend-plane.md) | Known two-bone chain/roll; singular poses need a stable convention |
| Pick up, attach, release, change parent space, prop jumps | [Child Of handoff](techniques/child-of-handoff.md) | Unparented rigid object, full axes, matched discrete events |
| Switch IK to FK without a pop, snap incoming controls | [IK → FK match](techniques/ik-to-fk-match.md) | Same rig/rest axes; not reverse matching or continuous blending |
| Bake constrained bones to keys, preserve pose, interpolation error | [Native visual pose bake](techniques/visual-pose-bake.md) | Delivery copy; selected bones/Action slot, integers and subframes |
| Bend transition, twist distribution, rigid cuff, stale zero weights | [Skin weight partition](techniques/skin-weight-partition.md) | Declared rest coordinates and owned influences; not anatomical autoweights |
| Candy-wrapper collapse, Preserve Volume, cross-section area | [Same-pose skinning A/B](techniques/preserve-volume-ab.md) | Area, inner folds and intersections are separate checks |
| Joint shape driven by angle, corrective double-deforms | [Shape before skin](techniques/pose-shape-before-skin.md) | Rest-space delta and bounded local-angle driver; effect ≠ anatomical improvement |

For a different rig architecture, return to [rigging](rigging-workflow.md); for organic topology,
sculpted correctives, cages or a different skinning method, use [deformation](deformation-workflow.md).
Read only the row relevant to the current operation; the source asset is optional evidence.

## Geometry Nodes and repeated placement

| Need / search terms | Smallest useful entry | Boundary |
| --- | --- | --- |
| Row, grid, ring, bolt circle, seats, spacing, radial/tangent orientation | [Bounded GN patterns](techniques/gn-patterns.md), editable group helper | Source-local mesh, defined degenerate counts, host-local layout |
| Per-copy color, roughness or mask; shader variation without Realize | [Instance → shader attribute](techniques/instance-shader-attribute.md), two small functions | Named scalar on INSTANCE domain and matching shader reader |
| Surface scatter, slope, exclusion, path placement or persistent IDs | [Scatter](scatter-workflow.md), guide | Composition/eligibility and source footprint need their own checks |

## Shading coordinates

| Need / search terms | Entry | Boundary |
| --- | --- | --- |
| Pigment sticks to bending mesh, texture swimming | [Rest coordinates](techniques/rest-coordinates.md), technique | Stable point correspondence |
| Repeated objects need different material responses | [Instance attribute bridge](techniques/instance-shader-attribute.md), technique | Shared source material; unrealized instances |
| Directional image maps, board grain size, metric flat-patch UVs | [Metric image patch](techniques/metric-image-patch.md), helper + map contract | Coplanar faces, known physical image dimensions; no inferred end grain |
| Timber grain, rails/stiles, periodic stripes, exposed cuts | [Board grain and finish](techniques/wood-grain-frame.md), diagnostic route | Two visible faces/cut and feature scale; no universal oak preset |
| Roughness, wear, multiple surface responses | [Surface families](surface-families.md) / [material composition](material-composition.md), guides | Choose response for the view |

## Material responses

| Need / search terms | Smallest useful entry | Boundary |
| --- | --- | --- |
| Exposed metal, chipped paint, wet/dry regions, mix two surfaces | [Spatial shader mix](techniques/spatial-shader-mix.md), short wiring example | A spatial mask is distinct from a transparent coating; verify both endpoints |
| Resin, colored glass, liquid tint changes with thickness | [Interior absorption](techniques/volume-absorption.md), short wiring example | Closed boundary, known scale, separate Surface and Volume paths |
| Faux leather, leatherette, PU/PVC upholstery, shallow embossed grain | [Embossed upholstery](techniques/embossed-upholstery.md), small height helper | Cellular approximation; relief, pigment and finish remain independent |
| Molded plastic, satin housing, matte shell, fine mold texture | [Molded plastic finish](techniques/molded-plastic-finish.md) | Reflection first; optional microrelief and no automatic color noise |
| Frosted/etched glass, blurred background, privacy pane | [Frosted pane](techniques/frosted-pane.md) | Etched boundary versus thickness; near/far background test |
| Sheer curtain, thin cloth, backlight, visible weave openings | [Sheer fabric](techniques/sheer-fabric.md) | Thin-sheet scattering versus clear openings; mean coverage at architectural distance |
| Velvet edge, cloth sheen, soft fiber/dust reflection | [Sheen response](techniques/sheen-response.md), short parameter example | Reflection layer; does not build weave or silhouette fibers |

Use [material composition](material-composition.md) to choose between mechanisms or combine
them; full reference scenes are optional. These cards expose the optical operation, not a
universal finished-material preset.

## Bake and UV

| Need / search terms | Smallest useful entry | Boundary |
| --- | --- | --- |
| Black bake, wrong image, missing material region, active image | [Bake image target](techniques/bake-image-target.md) | Every receiving material; selected and active node |
| High to low, tangent normal, ray misses, cage reach | [Selected-to-active projection](techniques/bake-projection.md) | Isolated pair first; stable receiver and consumer tangents |
| Bake roughness/mask/base color, raw data, wrong gamma after reload | [Field → Emit → image](techniques/bake-field-transfer.md) | Field is not a BSDF; preserve source and declare encoding |
| Cylinder, pipe, canister, UV side strip and caps | [Seam-defined strip](techniques/uv-seam-strip.md) | Shape-specific cuts; actual corner coordinates and checker |
| Checker size, px/m, packing, gutter, bleeding, directional stretch | [Density and padding](techniques/uv-density-padding.md) | Relative vs absolute allocation; measured boundaries, not centers |

Use [baking](baking-workflow.md) or [UV layout](uv-workflow.md) for a different consumer,
complex cage, UDIM, trims or existing painted dependencies.

## Light and image

| Need / search terms | Smallest useful entry | Boundary |
| --- | --- | --- |
| Saved overview differs, cutaway, section, camera/layer visibility, wrong framing | [Saved review views](techniques/saved-review-views.md), short scene setup | Static view state; complete model retained, capped snapshots need refresh |
| Key/fill role, source size, soft shadow, light contribution | [Light A/B](techniques/light-role-ab.md) | Hold material/camera/view; World and emissive geometry remain separate |
| EXR vs PNG, exposure stops, wrong saved brightness | [Linear/display output](techniques/linear-output-exposure.md) | Same Render Result vs a newly lit render; beauty, not a pass archive |
| Rebuild beauty, missing contribution, sum lighting passes | [Lobe reconstruction](techniques/pass-reconstruction.md) | Raw conventional Cycles lobes, transparent film, separate alpha |
| Fringe, dark edge, foreground over plate, premultiplied/straight | [Alpha Over](techniques/alpha-over.md) | Known encoding/canvas; do not multiply coverage twice |
| Select one object in saved EXR, local exposure, protected region | [Cryptomatte grade](techniques/crypto-local-exposure.md) | Persisted metadata; mixed-object pixels remain approximate |

Use [lighting](lighting-workflow.md), [rendering](render-workflow.md) or
[compositing](compositing-workflow.md) to choose a broader method. These operations do not
require rebuilding an asset or opening the full historical scene.

## Cel shading and contours

| Need / search terms | Smallest useful entry | Boundary |
| --- | --- | --- |
| Toon, three tones, color bands, palette independent of lighting | [Neutral signal → palette](techniques/cel-palette-bands.md) | EEVEE Combined; thresholds need actual light/pose checks |
| Outline off/thin/thick, silhouette, pixel weight | [Independent contours](techniques/freestyle-contours.md) | Owned Freestyle style; engine/output-size check |

For style choice, cast shadows, different contour methods or temporal problems, use
[cel shading](cel-shading-workflow.md). Character form design remains a separate task.

## State and motion

| Need / search terms | Smallest useful entry | Boundary |
| --- | --- | --- |
| Low emission rate, missing births, reused ID, live particle cap | [Birth budget and IDs](techniques/gn-emission-budget.md) | Fixed capacity; excess drops; no queued bursts |
| Moving emitter, world-space trail, age/dt, gravity step | [Advance survivors, then births](techniques/gn-state-step.md) | Constant acceleration; explicit host space; no collision solver |
| GN packed bake, seek out of order, edit hidden by cache | [One GN bake and replay](techniques/gn-bake-replay.md) | Owned node/modifier; fresh-process state comparison |
| Settled particle hovers or intersects despite radius clamp | [Actual-shape support](techniques/particle-support-contact.md) | Known plane and fixed instant/orientation; geometric placement |
| Sparks cool/fade, heat changes but material does not | [Age → visible response](techniques/particle-age-response.md) | Designed response, attribute context and actual output |
| Pendulum, hinge axis, joint drift, angular limit | [Rigid Hinge frame](techniques/rigid-hinge-axis.md) | Two bodies; local Z, relative-angle convention |
| Rigid cache, random seek, original location does not move | [Evaluated world replay](techniques/rigid-cache-replay.md) | World-owned physics cache, not exported transform keys |

Use [particles](particles-workflow.md), [GN state](particle-simulation-nodes.md) or
[rigid bodies](rigid-body-workflow.md) when choosing a broader method or a different solver.
Cache equality, contact geometry and convincing motion are separate checks.

## Export and native delivery

| Need / search terms | Smallest useful entry | Boundary |
| --- | --- | --- |
| Export selected assembly, helpers leak, wrong duration, only one part animates | [Scoped GLB export](techniques/scoped-glb-export.md) | Tested timebase and merged clip; preserve authoring source |
| Vertex count changed, UV seams, mirrored transform, import differs | [Surface round-trip](techniques/glb-surface-roundtrip.md) | World shape plus corner attributes/images; receiver explicitly Blender |
| Embedded image missing, GLB bytes, duplicated mesh, GPU vertex/triangle estimate | [Payload audit](techniques/glb-payload-audit.md) | Targeted content/cost evidence; not a validator or runtime benchmark |
| Source revision should update two scenes but keep local animation | [Linked override update](techniques/linked-override-update.md) | Coherent root, stable identity, supported local edits |
| Independent editable copy versus frozen linked asset, Append/Pack | [Snapshot ownership](techniques/native-snapshot-ownership.md) | Fixed revision; resource packing is separate |
| Wrong relative image path, packed flag but no pixels, same basename | [Owner-relative resources](techniques/owner-relative-resources.md) | Resource owner and decoded content; not an exhaustive crawler |
| Deliver .blend project, relocate libraries/textures/cache, prove independence | [Clean project relocation](techniques/clean-project-relocation.md) | Fresh process; only disposable sources may be withheld |

Use [export](export-workflow.md) and [formats](export-formats.md) for a different receiver;
[asset libraries](asset-library-workflow.md) and [project handoff](project-handoff.md) for
broader ownership/dependency decisions. Blender interoperability and native portability are
separate guarantees. Read full assets only for integration or provenance.

## API and existing files

| Need / search terms | Entry | Boundary |
| --- | --- | --- |
| Missing rig, wrong scene, edit a ready asset | [Existing-file route](existing-file-workflow.md) | Verify loaded identity before diagnosing content |
| AttributeError, property/enum, Bone/PoseBone, Action slot, driver source | [Scoped API probe](api-diagnostics.md), direct CLI or import | Stored RNA/state; not an artistic or evaluated-motion validator |
| Unknown socket, linked control has no effect, graph operands | [One node/upstream branch](api-diagnostics.md#inspect-one-node-or-upstream-branch) | Exact input and bounded graph; then a one-control response test |
| Node socket, modifier input, stored value has no effect | [Active socket → evaluated effect](blender-methods.md#resolve-active-node-sockets-and-prove-their-effect), guide section | Confirm actual interface and consumer |

Other production areas remain in the [method selector](blender-methods.md#route-by-the-next-unresolved-question).
Use [whole assets](implementation-examples.md) for a specific integration or evidence question.
[Provenance](techniques/provenance.md) separates authored
checks from independent-agent results; [extraction](example-extraction.md) explains how new
mechanisms enter these modules.
