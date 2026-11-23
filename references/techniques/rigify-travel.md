# Walk from one mark to another on a Rigify human

Use this for a straight walk on level ground with a generated, upright Rigify human. The block starts from the character's current stance and ends at rest with both feet at the destination. Choose the step count, cadence and final pose from the brief. For a supplied walk, start with [Review the saved walk](#review-the-saved-walk). For turns and slopes, use the [walk guide](../character-walk.md).

### Make a playable pass

Once you have the names of the generated rig and its skinned body, run the first snippet in Blender. Fill in the skill folder, names, absolute output path and requested distance. The [blockout helper](../../scripts/techniques/rigify_walk.py) checks the standing IK controls, measures facing and footprints, saves an editable walk to disk, opens it and returns the contact measurements. An incompatibility identifies the control to inspect.

```python
from pathlib import Path
from runpy import run_path
import bpy

walk = run_path(str(Path(skill_dir) / "scripts/techniques/rigify_walk.py"))
fps = bpy.context.scene.render.fps / bpy.context.scene.render.fps_base
stage = walk["save_walk_blockout"](rig_name, mesh_name, output_path, distance=distance,
                                  hold_frames=max(8, round(0.75 * fps)))
print(stage["path"], stage["plan"], stage["report"])
```

A distance is measured straight ahead in Blender world units. For two world markers, confirm the feet start at A and pass `displacement_world=B-A` in place of `distance`. The default step count scales with distance and leg length. Set `steps`, `step_frames`, `lead` or `hold_frames` for a choreographed rhythm. The created Action carries its start reference, destination offset and footfall plan across calls and file reloads. If the report lists a failing contact or endpoint, fix the walk before adding the gesture.

### Review the saved walk

Inspect the supplied scene before changing keys. This example checks a walk that starts with both hands near the hips and ends with one hand rising to its own shoulder after the stop. Set `side` from the brief. The Action records its original start reference, displacement and footfall plan. If the brief has a new destination, measure against that destination.

```python
from pathlib import Path
from runpy import run_path
import bpy

scripts = Path(skill_dir) / "scripts"
walk = run_path(str(scripts / "techniques/rigify_walk.py"))
review = run_path(str(scripts / "techniques/travel_review.py"))["review_travel"]
ctx = walk["read_walk_plan"](rig_name)
ref, delta, plan = ctx["ref"], ctx["delta"], ctx["plan"]
checks = dict(start_hands={"L": "hip", "R": "hip"},
              end_hands={side: "shoulder_height"}, face_world=delta,
              min_steps=len(plan["footfalls"]),
              hold_frames=4, raise_after_arrival=side)
result = review(ref, delta, **checks)
print(result)
```

For a clip without a stored plan, use the [review helper](../../scripts/techniques/travel_review.py) to capture the starting stance with `capture_travel(rig, mesh)` and pass the requested displacement. Use scene marks or the clean source for absolute destinations. Set the step count from the brief. If the existing timing must be preserved, compare the landing frames and sides with the source. Include `raise_after_arrival` only if the gesture should follow the stop. Its check also detects a lift concentrated into one frame. Use `smooth_raise=False` for an intentionally stepped pose change.

### Repair only the reported movement

Use the failing measurement and frame interval to select a control. For a missing, early or abrupt lift on a stopped character, keep the wrist at its walking pose through the last landing, give it time to reach the shoulder, then hold. A high key marks the instant the wrist has already reached its target. This example replaces the selected hand's location keys inside the settling interval and preserves the earlier walk.

If you need to inspect existing keys, import `anim_utils` from `bpy_extras`, set `ad = rig.animation_data`, and read `anim_utils.action_get_channelbag_for_slot(ad.action, ad.action_slot).fcurves`. Each curve has a `data_path` and `array_index`. [Action slot example](../animation-workflow.md#use-the-current-animation-data-model)

```python
rig = bpy.data.objects[rig_name]
start, end = plan["arrival"], plan["last"]
walk["settle_hand"](rig, side, start, end - 4, end, "shoulder", outward=0.14, forward=0.16)
bpy.context.scene.frame_set(plan["first"])
result = review(ref, delta, **checks)
if result["ok"]:
    save = run_path(str(scripts / "blend_file.py"))["save_and_reopen"]
    save(output_path)
    result = review(ref, delta, **checks)
print(result)
```

If a foot ends short of its destination, correct its last swing and landing. When the planted sole drifts while its IK control stays still, check whether the knee has straightened fully. Try lowering the pelvis during that transfer or, if the cadence is free, taking shorter steps from the clean source. For a sideways lurch, inspect the reported pelvis frame and its neighbours against the line of travel. Set `max_lateral_drift` in world units when the brief deliberately calls for a wider sway.

Compare each repair with the saved pass using the same reference. If a sound contact or endpoint gets worse, reopen that pass. Keep the improvement, reopen the output and check it again. Watch the whole figure at playback speed to judge weight, balance and timing.
