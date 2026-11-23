# Rigid bodies: release, collide and settle

Use for shape-preserving bodies with dynamic contact. Designed motion can use constraints or
keyframes through [animation](animation-workflow.md); rig constraints and rigid-body constraints
are different systems. Apply the scale/time/cache decisions in [simulation](simulation-workflow.md).

For a known local operation, use [Hinge axis/limits](techniques/rigid-hinge-axis.md) or
[evaluated cache replay](techniques/rigid-cache-replay.md). Choose broader contact geometry
and solver behavior below.

## Reusable starting patterns

| Pattern | Setup decisions | Useful controls and proof |
| --- | --- | --- |
| Drop or small debris pile | Active bodies, passive support, simple convex/primitive shapes and separated starts | Release height/orientation, mass, friction/restitution; inspect impact and settling |
| Rolling/sliding prop | Shape appropriate to contact, slope/support and plausible center of mass | Support angle, friction, restitution; check rolling versus sliding and final support gap |
| Animated handoff | Kinematic/Animated control until release, then physics ownership | Release frame and incoming motion; inspect frames immediately before/after transfer |
| Hinge, pendulum or constrained mechanism | Connected bodies, constraint pivot/orientation, limits and disabled mutual collision where appropriate | Swing/drive/limits; inspect full travel, constraint drift and forbidden intersections |

Do not start with hundreds of fragments. Prove one body/support and a small interacting set.
Keep render detail outside contact geometry when possible; expose the small set of meaningful
controls in the objects or project conventions rather than rebuilding the scene per variant.

## Model contact deliberately

Verify Active/Passive membership in the actual Rigid Body World collections, including
constraints. Choose a collision shape by occupied volume: primitives or convex hulls suit many
moving objects; a hull closes cavities. A vessel or concave support may need compound convex
pieces or an appropriate static mesh. Dynamic triangle meshes are a costly/fragile default.
Check the evaluated proxy and the expected center of mass, not only the rendered origin.

Avoid initial overlaps and trapped constraints. Apply scale where appropriate before tuning
a new setup; preserve existing animated transforms intentionally. Match collision margin to
object/contact scale and inspect support gaps. Zero margin or a large margin is not a universal
repair. Small/fast bodies and thin triangle surfaces need special attention to missed contacts.

If bodies tunnel, compare displacement per step with the thinnest relevant contact feature.
Inspect start state, collision representation and scale before increasing substeps. If stacks
or constraints drift, inspect mass ratios, constraint frames and solver iterations. Friction,
damping and deactivation cannot repair an intersecting initial assembly. Test the chosen rest
thresholds so objects do not freeze before visible motion should end or jitter indefinitely.

For animated colliders, verify that the physics engine sees their movement. Keying the visible
object alone can leave a passive collider at its starting state if its Animated mode is wrong.
At a kinematic-to-dynamic handoff, compare position and velocity through the switch. Activating
a constraint between badly separated bodies can inject a large corrective impulse.

For a hinge, align the constraint object's **local Z** with the intended pivot axis; do not
inherit another constraint type's axis convention. Inspect its anchor position through the
full swing as well as angle limits. For rolling, review rotation together with translation:
a sphere moving down a slope does not by itself prove rolling contact. A stripe or measured
travel versus rotation helps separate rolling from sliding without prescribing one friction.
See the [Hinge axis contract](https://docs.blender.org/manual/pt/5.2/physics/rigid_body/constraints/types/hinge.html).

## Bake and compare the right result

Bake the world range using its actual point cache; save and reopen before claiming cached
random access. Evaluate body world transforms from the dependency graph, since original
location channels can remain at the authored start while physics moves the evaluated body.
Review contact/settling visually as well as finite positions and plausible bounds.

For a receiver requiring transform keys, use a delivery copy and bake the evaluated motion.
Compare several times, especially release/impact, then disable the original simulation on that
copy to prove the keys carry the result. This is different from preserving a physics cache;
keep the editable simulation source. Do not promise that the target receives Bullet settings.

If an interactive bake operator lacks its required editor/keying context in automation, use
a supported evaluated-transform sampling route on a delivery copy. Capture the source motion
before removing physics, account for parenting/local space and rotation continuity, then
compare keys after reopening. [Rig handoff](rigging-workflow.md) also explains sampling and
subframe limits. A successful integer-frame match does not certify motion-blur interpolation.

[Rigid Body World](https://docs.blender.org/manual/sr/5.2/physics/rigid_body/world.html) documents
membership, substeps, solver iterations and cache scope. [Rigid-body tips](https://docs.blender.org/manual/sv/5.2/physics/rigid_body/tips.html)
cover animated handoffs, scaling and cross-system use. The [collision shape guide](https://docs.blender.org/manual/en/5.2/physics/rigid_body/properties/collisions.html)
describes proxy options; confirm their live enums and behavior in the intended build.
