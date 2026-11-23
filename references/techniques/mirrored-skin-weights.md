# Locate a skin-weight defect on a posed limb

On a bilaterally skinned character, compare the posed fold with weights from its healthy opposite limb. Keep the requested pose. The [read-only vertex probe](../../scripts/vertex_probe.py) pairs original vertices across rig-local X = 0 in the rest mesh, even if the two limbs have different poses.

**Find the patch.** Supply the inspected mesh object `mesh` and the absolute skill folder `skill_dir` as a `Path`. On stock Rigify the forearm head is the elbow. Use a search radius that includes healthy loops on either side of the joint. The radius and optional matching tolerance use rig-local units.

```python
from runpy import run_path

probe = run_path(str(skill_dir / "scripts/vertex_probe.py"))["mirrored_weights"]
rig = next(m.object for m in mesh.modifiers if m.type == "ARMATURE" and m.show_viewport)
joint = rig.data.bones["ORG-forearm.L"]
result = probe(mesh, rig, joint.name, radius=joint.length / 2)
print(result["in_region"], result["matched"], result["unmatched"])
for row in result["candidates"][:3]:
    print(row["index"], row["weight_l1"], row["weights"], row["expected_weights"], row["posed_world"])
```

The probe uses unique mutual matches within tolerance. It ranks the sum of absolute differences between deform-bone weights after pairing names such as `forearm.L.001` and `forearm.R.001`. Look for connected outliers with an abrupt change relative to neighboring loops. Increase `limit` to see where the scores return to the local background. A narrow section also occurs on a healthy inner bend. For poor matches or intentional asymmetry, compare with adjacent loops or a trusted healthy version.

**Show the result.** Choose a vertex in the confirmed patch. Report its mesh, source index and `posed_world` point. Frame that point from the exposed side. If the marker is occluded, try a second angle. After moving the marker or camera, render again and open the saved image to check its framing and marker. The probe supplies posed points for an armature-only viewport stack. With other modifiers, identify the point on the source cage or establish a source-index mapping before reusing IDs on the evaluated mesh. Equal counts alone are insufficient.

For a local vertex search without a mirror reference, seed it with a visible face or joint landmark. Compare points in one space, keep those within the local radius and follow mesh edges to stay on the same surface. Review the resulting IDs and their neighbors before changing them.

**If asked to edit**, use the confirmed source IDs. In Object Mode, read memberships from `mesh.data.vertices[i].groups` and resolve each group by index on the object, `mesh.vertex_groups[g.group]`. For a binding repair, `mesh.vertex_groups[bone_name].add([i], weight, "REPLACE")` sets one influence. Preserve locked groups and masks, check the sum of deform weights, then test the same patch in a second bend. For a rest-shape edit, set `mesh.data.vertices[i].co = mesh.matrix_world.inverted() @ rest_world` in Object Mode and call `mesh.data.update()`, or edit the intended shape key. A posed point already includes skin deformation. In Edit Mode use the live `bmesh.from_edit_mesh(mesh.data)` and flush changes with `bmesh.update_edit_mesh`. Reacquire IDs after changing topology. [Skin-weight repair](skin-weight-partition.md) · [Blender BMesh API](https://docs.blender.org/api/current/bmesh.html)
