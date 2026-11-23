# Turn and tilt a Rigify head

Use the generated rig’s native `head` control when the character should look to one side
and tip an ear toward a shoulder. Start from a neutral head relative to the torso. Identify
forward from the face and up from neck to crown. Anatomical left is **up × forward**.
Check it points toward the character’s left shoulder. Keep these reference directions fixed.

**Set the pose.** Supply the rig, world-space `forward_world` and `up_world`, and signed
angles `yaw` and `tilt` in radians. Positive yaw turns the nose toward character-left;
positive tilt lowers the left ear. This example assumes a rigid or uniformly scaled rig.

```python
import bpy
from math import atan2, degrees
from mathutils import Quaternion

ctrl = rig.pose.bones["head"]
saved_basis = ctrl.matrix_basis.copy()
base = ctrl.matrix.copy()
world_to_rig = rig.matrix_world.to_quaternion().inverted()
F = (world_to_rig @ forward_world).normalized()
up = world_to_rig @ up_world
U = (up - F * up.dot(F)).normalized()
L = U.cross(F).normalized()

turn = Quaternion(U, yaw)
lean = Quaternion(-F, tilt)
goal = (turn @ lean).to_matrix().to_4x4() @ base
goal.translation = base.translation
ctrl.matrix = goal
bpy.context.view_layer.update()
```

`ctrl.bone.matrix_local` contains the rolled rest axes in armature space. The current
`ctrl.matrix` carries those axes through the posed parent. Pre-multiplying this matrix
applies the anatomical rotation in rig space while keeping the head pivot. Reuse the
captured neutral `base` for revisions. `turn @ lean` tilts around the facing direction
after the turn.

**Read back the result.** Measure the face and crown directions again from corresponding
points on the **evaluated** head. For example, use back-to-nose and neck-to-crown landmarks
or fit a rigid rotation to a sample of the upper head vertices before and after the pose.
Express both measured rays in the same armature space as the neutral references. For a
near-horizontal gaze, these formulas return positive values for a left turn and left tilt.

```python
face = measured_forward.normalized()
side = U.cross(face).normalized()
vertical = face.cross(side).normalized()
yaw_deg = degrees(atan2(face.dot(L), face.dot(F)))
tilt_deg = degrees(atan2(measured_up.dot(side), measured_up.dot(vertical)))
```

Compare signs and magnitudes to the request, then inspect the camera view and measure
displacement of a chest and opposite-shoulder sample. For a control-response check, keep
the accepted channels, restore `saved_basis`, update and verify that the head returns to
neutral, then restore the accepted channels and update. A vertical gaze needs a different
up reference because its projected horizontal heading vanishes.
