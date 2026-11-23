# Recipe: a restrained upper-body gesture

Compose for a ready character's readable limited gesture. Define intent, views, timing/contact;
skip rig/surface construction when the input already has them. Use only the relevant techniques:

1. Prove one [FK pose/direction](../techniques/fk-phase.md), then place leading/response poses.
2. Phase secondary motion where useful; protect contact and silhouette.
3. Tie [blink](../techniques/driven-blink.md) to the intended event.
4. If pigment slips, use suitable UV mapping or [rest coordinates](../techniques/rest-coordinates.md).
5. Review the saved pose/shape animation together, including in-betweens and clip boundaries.

The [Momo interface](../examples/character-gesture.md) is optional integration context.
Its names and original amplitudes are not required inputs to these techniques.

## Timing, deformation and image decisions

**Purpose:** make the existing character feel attentive and readable through a short gesture.
Block an initial pose, anticipation, wave extremes and settling pose before adding secondary
motion. Judge face visibility and negative space between hand, head and tail in the shot.
A clean joint deformation can still produce an unreadable overlapping silhouette.

Resolve surface defects and necessary topology changes before skinning or facial keys. Retain
the source and compare the new silhouette; remeshing is not automatic animation topology.
For a bounded upper-body gesture, FK arms and a small torso/head/tail hierarchy may be enough.
Use IK when the hand must maintain an external contact, not simply because it is available.
Keep planted feet stable while the torso shifts; test the supported joint range and root motion.

Offset head response and successive tail controls to make the gesture follow through rather
than moving every part in phase. Shape their timing with keys/curves; random noise does not
substitute for an intended arc. Review the resulting pose and speed at delivery frame rate.

Use facial shapes appropriate to the style. The Momo example uses a graphical closed-eye curve
and withdraws the highlights during a blink. This does not demonstrate anatomical eyelids,
eye tracking or a full facial rig. Test partial closure, full closure and combined head motion.
Carry procedural markings with the deforming surface using suitable UV/rest coordinates; an
object-space mask alone does not guarantee that painted regions stay attached to skin.

For a loop, match the visible state and its incoming/outgoing motion. A matching endpoint key
can sit immediately after the delivered range, avoiding a duplicate held frame. Check nearby
frames and subframes, not just equal endpoint matrices. Preserve every Action/slot needed by
the clip: pose channels and facial controls may have different owners.
