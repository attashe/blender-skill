# Animate a Rigify IK foot or hand

**Already have both endpoint poses?** Keep the assigned Action, its slot and its playback range. Use `key_control_world` to insert intermediate keys on existing channels. For a step, [capture the original poses and measure the transfer](../humanoid-animation.md) before using the examples below. The two-pose setup below is for a new motion on free location channels.

Use the generated armature targeted by the body mesh's Armature modifier. On stock Rigify limbs, full IK is `IK_FK == 0` on the limb settings bone (often `thigh_parent.L` or `upper_arm_parent.L`). If a limb starts in FK, match its IK controls to the current pose with Rigify's snap before switching. Keep the existing parent setting, pole, heel roll and toe orientation for a flat translation. [Rigify limb controls](https://docs.blender.org/manual/ru/5.2/addons/rigify/rig_features.html)

### Place one foot, keep the other planted

Work on the supplied starting pose. Choose the two frames and the distance from the brief. Use the current IK control transform as the origin of a relative move. Moving an ankle control to the absolute height of a sole point would discard the ankle-to-sole offset.

Pass in the body object `mesh`, skill folder `skill_dir`, absolute `output_path`, integer frames `first` and `last`, and the desired forward displacement `distance_in_blender_units`. With metric scene units, divide the requested distance in metres by `scene.unit_settings.scale_length`.

```python
from pathlib import Path
from runpy import run_path
from mathutils import Vector
import bpy

# mesh is the skinned body object. skill_dir is the actual folder containing SKILL.md.
rig = next(m.object for m in mesh.modifiers if m.type == 'ARMATURE' and m.object)
motion = run_path(str(Path(skill_dir) / 'scripts/techniques/motion.py'))
scene = bpy.context.scene
scene.frame_set(first)
def head_world(name):
    return rig.matrix_world @ rig.pose.bones[name].head

# Use the generated control names present on this rig.
feet = ['foot_ik.L', 'foot_ik.R']
toe_for = {'foot_ik.L': 'toe_ik.L', 'foot_ik.R': 'toe_ik.R'}
ankles = (head_world(feet[0]) + head_world(feet[1])) / 2
toes = (head_world(toe_for[feet[0]]) + head_world(toe_for[feet[1]])) / 2
up = Vector((0, 0, 1))   # World normal to this support surface
forward = (toes - ankles) - up * (toes - ankles).dot(up)
forward.normalize()
moving, = motion['control_sides'](rig, ankles, toes, feet, up=up)['left']

# Pick a moving surface vertex in the starting pose for the save check.
live = mesh.evaluated_get(bpy.context.evaluated_depsgraph_get())
toe = head_world(toe_for[moving])
toe_index = min(live.data.vertices, key=lambda v: (live.matrix_world @ v.co - toe).length_squared).index
motion['key_ik_world_offset'](rig, moving, first, last, forward * distance_in_blender_units)
scene.frame_start, scene.frame_end = first, last  # For a new clip with this range
scene.frame_set(first)
save = run_path(str(Path(skill_dir) / 'scripts/blend_file.py'))['save_and_reopen']
print(save(output_path, motion_sample=(mesh.name, toe_index, first, last)))
```

The helper keys only the moving control's location, on free channels with unchanged parent space. Keep the support control and its parents in their original pose during this placement. If the torso or root will also move, check the IK parent space before animating them. Reacquire objects after opening the saved file. Compare the heel, ball and sides of each sole in world space. At the destination measure the chosen contact point, lowest surface height and sole tilt. Skin near the heel can follow the shin even when the IK control lands exactly. Inspect that residual before adjusting the target. On the planted side check the same points throughout the transition.

### Reach a target with a hand

For a fingertip or palm target, measure the current position of that surface landmark at the first frame. Move the hand IK control by the difference between the target and that landmark. This retains the offset from the wrist pivot to the contact point.

```python
delta = Vector(target_world) - Vector(palm_landmark_world)
motion['key_ik_world_offset'](rig, hand_ik_name, first, last, delta)
```

Use an attainable target while keeping the same hand orientation. Sample the palm after posing and check the elbow silhouette. For a pickup that switches parents at contact, use [matched pickup and release](../technique-index.md#rig-and-deformation).
