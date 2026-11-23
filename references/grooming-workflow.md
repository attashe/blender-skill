# Grooming: shape guides, attach roots, then add density or dynamics

Use for hair, fur, brows and related strand assets. A groom is a designed arrangement of
curves, not a particle count. Refer to [curves](curves-workflow.md), [GN](geometry-nodes-workflow.md)
and [simulation](simulation-workflow.md) only for the decisions the current groom needs.

## Reusable grooming patterns

| Pattern | Efficient starting route | Characteristic proof |
| --- | --- | --- |
| Short fur or fuzzy patch | Density/length regions, directional guides, modest interpolation, tapered radius and restrained clumping | Silhouette and growth direction at seams/thin regions; no bald gaps, detached roots or uniform spikes |
| Long hair/locks | Scalp regions, parting and silhouette guides before children; length, clump hierarchy and designed flyaways | Lock separation, contact with head/shoulders and view changes; children follow the intended guide regions |
| Brows, lashes or localized stylized strands | Small explicit or groomed curve set with deliberate roots, direction and taper | Attachment, spacing and silhouette without unnecessary dense children |
| Hair responding to movement | Valid attached groom plus a proven dynamics route, pinned roots and simple surface/other colliders | Animated support, root stability, bend/length behavior and a short cached interaction |

Inspect actual references for parting, direction changes, clump sizes, silhouette gaps, length
distribution, curl and regional density. Groom large masses before frizz and tiny flyaways.
A random normal-aligned field can suggest fuzz but does not establish a haircut or animal coat.
Keep density/length/parting masks, guide shape, child generation, radius and material separately
editable. Test a guide region with its neighboring region before covering the whole surface.

## Attach to the intended surface and rest state

Choose the existing project's Curves hair, supported legacy Particle Hair or tested external
system deliberately. Modern hair Curves/GN are useful for guide editing and procedural child
generation; do not convert a working legacy groom just to follow a newer feature list.

For surface-bound Curves, inspect the surface object, coordinate relationship, named UV map
and curve attachment attributes. Use the installed Empty Hair/attachment workflow where it
sets up these dependencies. Hair's lengthwise UV/parameter is not the same as scalp attachment
UV. Root coordinates must address the intended surface region; invalid/overlapping UV regions
or changed topology can produce jumps or ambiguous mapping. Surface UVs need consistency and
coverage for this use, not necessarily a texture-paint layout with unique space for every task.

When using Interpolate Hair Curves followed by Deform Curves on Surface, align interpolation's
rest-surface choice with the deformation's expected rest state. Check rest and deformed surface
data, modifier order and coordinate spaces. Test translation/rotation and a non-rigid surface
deformation: attached roots should follow the skin without double transforms or sliding to
another region. Hair that looks attached in the rest frame has not passed this test.

## Build controllable density and optical scale

Prove sparse guides and a small child region. Use relevant installed assets such as Generate/
Interpolate Hair Curves, Clump, Set Hair Curve Profile or restrained noise; inspect actual
interfaces, guide selection and attribute domains before wiring. Preserve distinct parting
regions so interpolation does not bridge an intended gap. Noise can break up a groom, but
independent random displacement is not a substitute for designed flow or physical dynamics.

Budget guides, children per region, total curves, points per curve, render density and radius.
Control curvature through enough samples, not uniform maximum resampling. Review the expanded
result and bounds; mesh tubes multiply topology and are usually unnecessary when the renderer
supports native strands. Choose strand radius/taper in scene units and inspect its apparent
width at delivery resolution. Increased density must not silently change overall hair mass.

Check the intended engine's hair shading, highlights, shadows and transparency. A native hair
BSDF, a generic surface material and opaque mesh tubes have different support and costs. Use
a neutral light plus the scene view, inspect against a contrasting background, and check a few
neighboring frames for thin-strand flicker. Geometry alone does not prove realistic hair.

## Keep guides reusable

The [Blender Studio procedural-hair case](https://studio.blender.org/blog/procedural-hair-nodes/)
describes editable parent guides followed by procedural children/effects. Use that split to
try density, clumping and silhouette variants without destroying the authored flow. Applying
generated modifiers can be a deliberate final manual-edit branch; keep the reusable guide
source first. The 2023 article's then-missing dynamics are historical, not a current capability
claim; use current runtime checks for motion.

## Add dynamics only to a working groom

Distinguish surface-following deformation from inertia, strand collisions and wind response.
For an existing legacy Hair Dynamics setup, verify its actual solver, pinning, collision and
point cache. A new Curves object does not inherit that system automatically.

Blender 5.2's experimental **Hair Dynamics** asset uses XPBD and rest/surface data; the updated
Empty Hair route can establish Capture Rest Geometry dependencies. Prefer the packaged asset
for a first test, then inspect its bundle/effectors contract and GN cache. Maintain the proper
rest capture before the surface deformation it describes. Classic Collision flags are not a
guarantee of GN Collider participation. Verify the installed asset, not just the node class.

The tested asset exposes **Animation** for surface-following transfer and **Physics
(Experimental)** for stateful dynamics. Inspect the actual mode enum and demonstrate the
chosen behavior: the name Hair Dynamics alone does not prove that physics ran.

Separate hair-to-object contact from strand-to-strand contact. The tested 5.2 XPBD route has
external mesh colliders but no self-collision; more guides, thicker strands or stronger root
stiffness do not create mutual contact. Inspect the installed capability before promising a
dense interacting groom. A clumped guide can stand for a lock, but that approximation needs
to fit the shot. Choose a proven alternative when mutual strand contact is essential.

Start with few guides/children, fixed roots, simple moving skin and one collider; prove length/
bending behavior and finite points before increasing density. Too much stiffness, overlapping
starts, fast support motion and oversized contact radii can all create instability or floating
locks. Custom XPBD graphs require explicit world geometry, constraints, effects, spaces and time;
an empty Simulation Zone supplies none of these. If an experimental route fails a bounded
probe, retain a working static/surface-following groom or use a supported dynamics/baked route
appropriate to the brief, and state the behavior still missing.

At the denser proof, inspect per-strand length ratios and worst segments through the entire
range, including late frames; root stability and a convincing contact frame can hide large
elongation elsewhere. Compare a changed force and a disabled collider on separate clean-source
variants. Increase constraint/substep accuracy only when those errors justify the cost, then
measure again. Prefer simulating a controlled guide set before generating render children
when interpolation preserves the required silhouette and contact. Recheck generated strands
too: guide clearance alone does not guarantee that interpolated children avoid the surface.

Reopen and directly seek baked adjacent frames, checking root error and curve topology/length
where those should be stable. Preserve the groom source even if delivering baked strands or
another representation. Do not label a static or skin-following groom as collision dynamics.

Sources: [attachment inputs](https://docs.blender.org/manual/id/4.0/modeling/geometry_nodes/hair/utility/attach_hair_curves_to_surface.html),
[interpolation/rest-surface guidance](https://docs.blender.org/manual/ru/5.2/modeling/geometry_nodes/hair/generation/interpolate_hair_curves.html),
[5.2 Hair Dynamics and rest capture](https://developer.blender.org/docs/release_notes/5.2/physics/),
and [XPBD's world and time contract](https://developer.blender.org/docs/features/nodes/xpbd_solver/).
Attachment concepts from older documentation still need current interface inspection.
