# Momo: adapt a bounded FK gesture

This is an asset-specific integration interface. For a reusable operation start with the
[technique index](../technique-index.md); for composition use the [recipe](../recipes/character-gesture.md).

Use for a short upper-body gesture with graphical blink and delayed tail on the prepared Momo.
This rig demonstrates a limited pose range, not locomotion, IK/FK switching or a full facial rig.
The optional example was exercised in Blender 5.2.1 LTS, build 9e2066aef7ef.

## Choose the right input and interface

The [editable gesture scene](../../assets/momo-example/gesture.blend) contains the 11-bone rig, skin, blink drivers and greeting Actions. Scrub the existing performance or save a copy for a new gesture.

| Interface in the rigged asset | Role / units | Preserve or verify |
| --- | --- | --- |
| `RIG_Momo` pose bones `Spine`, `Head` | Upper-body FK; bone-local Euler angles in radians | Bone axes and semantic direction of a new pose in the actual view |
| `Arm_L`, `Upper_R`, `Fore_R`, `Hand_R` | Arms/raised hand | Rest is the raised-arm pose; separate local hand gesture from inherited torso movement |
| `Tail_1` … `Tail_4` | Successive tail segments | Offset response along the chain; inspect the resulting shape |
| `CTRL_Momo["blink"]` | 0=open, 1=graphical closure; drives eye/highlight shape keys | Rig pose Action and root blink Action have distinct owners/slots |
| `Root`, lower-body weights; `rest_position` on Body/Head | Planted lower body and coordinates for painted regions | Foot contact and pigment staying attached during deformation |

## Relevant implementation, then one changed pose

Inspect the assigned pose Action on the rig and the blink Action on the root. The [FK phase example](../techniques/fk-phase.md) shows how to offset a follower, and the [blink example](../techniques/driven-blink.md) explains the shape drivers.

Choose the leading pose and the weaker following body/tail response for the new gesture.
Before filling the timeline, change one head/torso angle on a copy and inspect its evaluated
effect in the shot: the expected numeric peak alone does not distinguish nodding down from
lifting the chin. Isolate conflicting existing animation or key the diagnostic change.
Then add timing, secondary motion and blink at the intended event; original greeting values
are an example, not required amplitudes or timing.

## Verify the saved result

Reopen your output and inspect extremes, in-betweens and the loop; compare feet, face/hand
readability, painted regions and delayed tail response. Count blink **intervals/events**, not
closed frames; label radians/degrees correctly. Report a local hand change separately from
world travel inherited from the torso. Keep the images and checks tied to the delivered file,
including after a late source-code correction.
