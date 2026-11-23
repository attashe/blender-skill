# Build and review an animation in stages

Choose the stages, poses and timing from the brief. Carry them through to a saved, playable result in the current request.

## Choose your next task

1. **Find the dependencies.** Describe the start, the decisive change and the exit. Pick the smallest visible change on which another part depends. Travel, contact, a new pose or a timing change can each be a first task.
2. **Give yourself a testable assignment.** Keep the next task in your working notes as `Change [one relationship] during [interval]. Pass if [observable result]. Preserve [accepted check].` For example, close a gripper until it touches the load while the load stays on the bench. Then lift the load and keep its contact with the gripper fixed. Choose tolerances that suit the shot's scale and playback rate.
3. **Keep a reference you can test again.** Before editing, record the landmark, reference frame, frame interval and expected value, direction or event order. After a pass succeeds, keep its measured value and tolerance alongside the check. The target comes from the brief, the source or a scene marker. Comparing two drafts alone can preserve a mistake.
4. **Accept or repair.** Test the change and the previously accepted checks on the candidate. Keep the last accepted file recoverable until the candidate has been saved, reopened and checked. If a check fails, the next assignment is to fix the earliest bad interval or restore the working pass. Keep the original targets and tolerances. After it passes, choose the next unmet requirement yourself.

Once the whole action reads, review its spacing and secondary motion at speed. Finish by opening the requested output and repeating the checks across the full clip, including intermediate frames and the exit.

## Choose observations that distinguish the intended motion

- If something must keep moving at the cut, check its direction and speed in the last interval.
- Work out what initiates the action. What carries the rest? What stays in contact, and until when? Which part can follow through after its parent changes direction? Rigid attachments keep their relationship. Give flexible or independently driven parts the timing their job requires.
- Choose a reference for each observation. Measure travel against fixed scenery, contact against the supporting surface, and articulation against the part carrying it. For example, to see whether a latch opens after a case stops, compare the case with the floor and the latch with the case. Both can travel the full distance while the latch stays shut.
- Test the measurement itself on a plausible wrong pose before accepting the change. For a requested reorientation, track an attachment and a free end in the chosen reference frame. For example, to measure a tilt away from a surface, project the unit vector from attachment to tip onto the surface normal. Turning in the plane must leave that score unchanged. If a wrong pose passes, change what you measure and retest the saved pass.

## Protect direction and contact

**Travel.** Before keying, establish the direction from A to B or from two landmarks defining forward in the source pose. Sample an identifiable point on the evaluated moving body. Check signed progress, plus distance to the destination if one was specified. A correct finish can hide an unintended reversal, so also check consecutive samples during each intended forward section. On a curved path or a deliberate recoil, use that section's intended direction.

**Planted contact.** Identify the material point that should stick, the surface and the interval before release. If a whole patch must stay flat, sample several points. At first contact, verify the initial gap and record the anchor on the surface in the support's coordinates. At each contact frame, use the current support transform and world-space surface normal. Record peak tangential drift, signed normal gap and the first frame outside tolerance. Peak drift catches a slide that returns to its starting point. A moving support can carry a planted point a long way in world space.

```python
def signed_travel(point_world, start_world, direction_world):
    return (point_world - start_world).dot(direction_world.normalized())

def contact_error(point_world, support_world, anchor_local, normal_world):
    error = point_world - (support_world @ anchor_local)
    normal = normal_world.normalized()
    gap = error.dot(normal)
    return (error - normal * gap).length, gap
```

These calculations take Blender vectors, a nonzero direction and an outward normal. With a rigid support, capture `anchor_local = support_world.inverted() @ surface_point_world` at contact. For a deforming support, follow the same surface triangle and its material coordinates. End the check at release, start a new anchor at the next plant, and follow the current contact patch during a deliberate roll. For an intentional slide, compare with its planned path.

## Make one complete pass

Start with the main visible change you can already control. Key its starting and changed poses, then save and reopen the requested output in that same editing call. Continue from that file, keeping each animated owner's assigned Action and slot. If a control is unfamiliar, try its axes on the same original pose in one call. Track a surface point away from the **axis** and compare its signed displacement with the intended direction. Restore each trial. Once one achieves the intended direction and preserves the required contact, use it for the blockout. Check both surfaces when a pair should move together.

On a free quaternion control with uniform scale, you can apply a turn about an axis chosen in the scene without guessing Euler order. At the desired frame, read `basis = (rig.matrix_world @ control.matrix).to_quaternion()`, then `axis_local = basis.inverted() @ axis_world.normalized()`. The new local value is `control.rotation_quaternion.copy() @ mathutils.Quaternion(axis_local, angle_radians)`. Recompute the basis after the parent changes pose.

Choose the event times in seconds and convert them to frames at the scene's playback rate. Put a pose on either side of each change in support or direction. Widen the spacing as something accelerates and narrow it as it slows. If motion should continue through a transition, carry that speed across it. Block gross travel and the major articulations together so the action reads from start to finish. Refine contacts and secondary motion on the saved pass.

For standard pose controls, assemble an event table from your poses. Each row below is `(frame, {bone_name: {RNA_property: whole_value}})`. Use local values in the control's current rotation mode. Euler angles are radians and quaternions use `(w, x, y, z)`. For an absolute world-space target, [key_control_world](../../scripts/techniques/motion.py) converts it through the parent evaluated at that frame.

```python
import bpy
from runpy import run_path
from pathlib import Path

scene = bpy.context.scene
rig = scene.objects[rig_name]
scene.frame_start, scene.frame_end = first, last
for frame, changes in poses:
    scene.frame_set(frame)
    for name, channels in changes.items():
        control = rig.pose.bones[name]
        for prop, value in channels.items():
            setattr(control, prop, value)
            control.keyframe_insert(data_path=prop, frame=frame, group=name)
scene.frame_set(scene.frame_start)
save = run_path(str(Path(skill_dir) / "scripts/blend_file.py"))["save_and_reopen"]
print(save(output_path))
```

Seek **before** assigning a value. Seeking between assigning and inserting a key can restore the old animated value. Let Blender create the Action and slot on the first key of a clean rig. On an animated rig, keep the assigned Action and edit the intended controls. For BlenderMCP, send a self-contained script in the tool's `code` argument. Python variables are fresh on each call. The scene, including changes made before an exception, persists.

## Diagnose the first visible mismatch

Play the reopened pass at the intended rate. Check the start, a transition and the exit in a view that shows both the moving part and its reference. Around the first wrong frame, sample the evaluated surface on consecutive frames. For a mesh with stable vertex order, measure a point's world position as `mesh_eval.matrix_world @ mesh_eval.data.vertices[i].co`. To remove inherited travel, express that point in the evaluated parent or support matrix with `reference_world.inverted() @ point_world`. Reacquire the evaluated data at each frame.

- **The pass reads as stationary.** Compare the keyed control's evaluated transform at two distinct poses, then compare the surface it should drive. These two observations locate a keying, space, constraint or skinning issue before you adjust the timing.
- **The poses read, but the motion looks wrong.** Follow the spacing between poses. Look for the first slip, change of direction, abrupt jump, or missing response. Change the owning control in that interval and replay it alongside a feature that was already right.
- **A script fails mid-pass.** Inspect the actual pose or reopen the last saved pass. Clearing its Action can leave old pose values in the scene and remove useful keys. Reduce the failing operation to one control and two frames, then extend the successful edit. Curve handles and modifiers can wait until the blockout plays.

Save the revision, reopen that exact path and repeat the same measurements. Report what changed on disk and any remaining visual defect. The [animation workflow](../animation-workflow.md) covers curve editing and further polish when the blockout warrants it.
