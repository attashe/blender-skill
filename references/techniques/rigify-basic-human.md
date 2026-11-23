# Fit and pose a Rigify Basic Human

Use the Basic Human metarig for a humanoid with recognizable limb and torso joints. Keep the fitted metarig for edits. The generated rig owns the controls and deforms the mesh. For a forearm across the chest, use [Elbow fit and forearm clearance](arm-front-of-chest.md) to locate the three joints and test contact along the sleeve.

Follow the [bind checkpoint, pose reset and reopened bend checks](../../SKILL.md#building-a-character-rig) when fitting and testing this rig.

**Fit.** With Rigify enabled and Blender in Object Mode, `bpy.ops.object.armature_basic_human_metarig_add()` creates the metarig and makes it active. For an unfamiliar installation, search the registered operators with `api_probe.find_ops("basic human metarig")` or `api_probe.find_ops("rigify generate")`. [Operator lookup](../api-diagnostics.md)

Choose shoulder, elbow, wrist and leg joints from the mesh in rest pose. Trace the spine through chest, neck and head, distributing intermediate joints in anatomical order. Leave a slight elbow and knee bend in the intended plane. In Edit Mode, convert world landmarks into **metarig space**. For example, `meta` is the active metarig and the two landmarks below are world-space vectors.

```python
to_meta = meta.matrix_world.inverted()
arm = meta.data.edit_bones["upper_arm.L"]
arm.head = to_meta @ shoulder_world
arm.tail = to_meta @ elbow_world
```

Plan both ends of each chain before moving shared joints. A connected child's head shares its parent's tail. Preserve the template's parent links, bone roll, Rigify types and original `use_connect` flags. Where the template has touching endpoints on an unconnected child, fit both endpoints explicitly. After leaving Edit Mode, check rest positions with `meta.matrix_world @ bone.head_local` and `tail_local` on `meta.data.bones`. Sight along the spine to catch a reversed neck segment.

**Generate and bind.** Activate the fitted metarig in Object Mode, run `bpy.ops.pose.rigify_generate()` and get `rig = meta.data.rigify_target_rig`. Confirm the generated arm has its hand IK control, original chain (`ORG-`) and deform bones (`DEF-`) before binding. On a fresh mesh, select the mesh and generated rig, with the rig active, then run `bpy.ops.object.parent_set(type='ARMATURE_AUTO')`. Check the mesh's Armature modifier target and per-vertex weights against bones with `use_deform`. Count uncovered vertices and inspect the strongest influences at the elbow, wrist and chest. Automatic weights can fail even when a modifier and named groups exist. [Skin weights](skin-weight-partition.md)

**Pose and verify.** On the stock left arm, `IK_FK = 0` selects IK. Use a reachable wrist target. This example changes the hand position while retaining its orientation. Choose `wrist_world` from the intended pose.

```python
from mathutils import Vector

rig.pose.bones["upper_arm_parent.L"]["IK_FK"] = 0.0
rig.update_tag()
bpy.context.view_layer.update()
hand = rig.pose.bones["hand_ik.L"]
pose = hand.matrix.copy()
pose.translation = rig.matrix_world.inverted() @ Vector(wrist_world)
hand.matrix = pose
bpy.context.view_layer.update()
```

Compare the generated `ORG-upper_arm.L`, `ORG-forearm.L` and `ORG-hand.L` heads in world space before and after the bend. Measure the wrist's distance to its target and the bend at the elbow. Compare evaluated mesh vertices at the elbow and hand, plus a stationary region such as the opposite hand. Inspect the elbow silhouette in the same view. Save the rig, mesh and fitted metarig together and repeat the decisive check after reopening. [Rigify workflow](https://docs.blender.org/manual/en/latest/addons/rigging/rigify/basics.html)
