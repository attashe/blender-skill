# Animate an action on a humanoid

For successive steps, a loop, or a character crossing a shot, use [character walking](character-walk.md) for the path of the whole body, rhythm, acting and playback review.

**Read the two poses first.** In an existing Action, keep its slot, frame range and playback rate. Fit preparation, swing, landing and settle inside that range. Read the support change from the front and the path of the foot from the side. A new body channel needs keys for the original values at both boundaries or its first intermediate value can change the starting pose.

**For a step between supplied poses**, capture the body and both feet before keying. Give the [step review](../scripts/techniques/step_review.py) the generated rig and the names of its body, supporting foot and moving foot controls. For a staggered starting stance, supply the character’s world `forward` to isolate sideways motion. Across separate MCP calls, store `json.dumps(original)` in your task’s scratch directory and reload it with `json.loads` after reopening the result.

```python
from pathlib import Path
from runpy import run_path
from mathutils import Vector

review = run_path(str(Path(skill_dir) / 'scripts/techniques/step_review.py'))
original = review['capture_step'](rig, body, stance_foot, foot)
first, last = original['range']
```

**Block changes of support.** For a step from rest, keep both soles planted as the pelvis travels toward the supporting leg. Release the free foot once the body is moving onto its support. Let the knee fold, carry the foot forward on an arc with clearance under the whole sole, then lower it onto the recorded target. Give the body time to accept weight on the new foot. Let the pelvis and chest settle while the contact holds. Choose timing, lateral travel and clearance to suit the subject's proportions, pace and stance. For a single step ending at rest, reserve part of the shot for the landing and settle.

The same ordering works with other contacts. For a reach, establish the body's support before extension and keep the hand on its target during contact. For a turn, choose the pivot foot and release the other before changing its heading. For a rise from a chair, bring the trunk over the feet as the seat releases, then extend the legs. Add chest rotation, an arm counter-swing or head stabilization when it clarifies the action in the shot.

### Add breakdowns to an existing Rigify Action

Use a body control that moves the pelvis independently of the feet (often `torso` on a generated Rigify human). Try one small shift and inspect the sole and pelvis on the mesh. The master root normally carries the feet with it. Key one body control for that translation. Use the existing IK foot control for the swing. [Rigify controls](techniques/rigify-ik-animation.md)

The bundled [key_control_world](../scripts/techniques/motion.py) takes an **absolute world position** and inserts or updates the location at one frame in the active Action. It handles the Action slot and existing keys. `pose_bone.location` holds a local offset. Pass the captured world position through the same helper on the final hold.

```python
key = run_path(str(Path(skill_dir) / 'scripts/techniques/motion.py'))['key_control_world']
assert first < release < passing < touchdown < acceptance < settled < last  # step from rest to rest
foot_start, foot_goal = (Vector(original[p]['swing']) for p in ('start', 'end'))
stance_point = Vector(original['start']['stance'])
body_start, body_end = (Vector(original[p]['body']) for p in ('start', 'end'))
up = Vector(original['up'])

def on_floor(vector):
    return vector - up * vector.dot(up)

to_stance = on_floor(stance_point - body_start)
key(rig, body, first, body_start)
key(rig, body, last, body_end)
key(rig, body, release, body_start + to_stance * preparation_fraction)
key(rig, body, passing, body_start + to_stance * support_fraction)
key(rig, foot, release, foot_start)
key(rig, foot, passing, foot_start.lerp(foot_goal, travel_fraction) + up * clearance)
key(rig, foot, touchdown, foot_goal)
key(rig, foot, settled, foot_goal)
```

At `release` the moving sole is still planted. Place any low takeoff key strictly between `release` and the high passing pose. At passing, sight the belt line against the stance footprint from the front. Choose `travel_fraction` between zero and one. For a rolling or pivoting foot, track the heel or ball actually in contact.

### Receive weight after contact and keep the end pose

At touchdown the new sole is already in place while the belt line is still toward the old support. In the next pose, the pelvis travels toward the planted lead foot and dips as the knee yields. Pick the timing from playback and the distance from the stance. Here `remaining` and `received` are fractions of the corresponding distance to each foot, and `dip` is a small distance in world units.

```python
at_contact = body_end + on_floor(stance_point - body_end) * remaining
loaded = body_end + on_floor(foot_goal - body_end) * received - up * dip
key(rig, body, touchdown, at_contact)
key(rig, body, acceptance, loaded)       # after touchdown, with the foot planted
for frame in (settled, last):            # touchdown < acceptance < settled < last
    key(rig, body, frame, body_end)      # world position copied from the input
```

For a step ending at rest, use clamped Bézier handles on the settling body keys. Save and reopen with a moving sole vertex and a lift frame in `motion_sample`. Find the last planted frame before lift (`release`), first contact on landing (`touchdown`) and the subsequent loaded pose (`acceptance`) from the evaluated sole and body. Review that interval against the original data, using the same function after any repair.

```python
print(review['review_step'](original, release=release, touchdown=touchdown, acceptance=acceptance))
```

`swing_max_drift_before_release` should be near zero for a flat planted foot. `swing_extra_vertical_travel` measures how much vertical travel an extra dip and lift add to a single arc. For a simple step, a value comparable to the lift height is a cue to inspect the order and handles of the foot keys. Fix the early motion, then judge preparation at the last actually planted frame.

`toward_stance_at_release` and `toward_swing_after_touchdown` should both show a visible positive distance on a deliberate side-to-side transfer. Compare their size with the stance width. If they are negligible, move the body toward the measured foot positions and replay from the front. If the range changed or the endpoint errors grew, put the hold inside the original range and restore the captured boundary values. The report measures control points in world units. On the mesh, check clearance under the whole sole, landing at the target, contact drift and the final held pose. [Blender Studio walking study](https://studio.blender.org/training/animation-fundamentals/5d70e4e31ec1bc5f7c3d4e24/)
