"""Block a straight, level walk on an upright generated Rigify human in standing IK."""
import json
import math
from pathlib import Path
from runpy import run_path

import bpy
from bpy_extras import anim_utils
from mathutils import Vector


_motion = run_path(str(Path(__file__).with_name("motion.py")))
key_control_world = _motion["key_control_world"]
UP = Vector((0, 0, 1))
SIDES = ("L", "R")


def _world(rig, name):
    return rig.matrix_world @ rig.pose.bones[name].head


def forward_world(rig):
    """Read the standing heading from ankle-to-toe vectors (world XY)."""
    forward = sum((_world(rig, "toe_ik." + s) - _world(rig, "foot_ik." + s)
                   for s in SIDES), Vector((0, 0, 0)))
    forward.z = 0
    if forward.length < 1e-7:
        raise ValueError("Cannot identify heading from these foot and toe controls")
    return forward.normalized()


def _hand_target(rig, side, landmark, outward, forward, up):
    if side not in SIDES or landmark not in ("hip", "shoulder"):
        raise ValueError("Use side 'L' or 'R' and landmark 'hip' or 'shoulder'")
    if not all(math.isfinite(value) for value in (outward, forward, up)):
        raise ValueError("Hand offsets must be finite Blender world distances")
    left = _world(rig, "DEF-upper_arm.L") - _world(rig, "DEF-upper_arm.R")
    left.z = 0
    if left.length < 1e-7:
        raise ValueError("Cannot resolve the shoulder axis")
    left.normalize()
    bone = "DEF-thigh." if landmark == "hip" else "DEF-upper_arm."
    target = _world(rig, bone + side) + left * (outward if side == "L" else -outward)
    return target + left.cross(UP) * forward + UP * up


def key_hand_offset(rig, side, frame, landmark, *, outward=0., forward=0., up=0.):
    """Place a hand IK pivot relative to its shoulder or hip in Blender units."""
    if isinstance(rig, str):
        rig = bpy.context.scene.objects[rig]
    bpy.context.scene.frame_set(frame)
    key_control_world(rig, "hand_ik." + side, frame, _hand_target(rig, side, landmark, outward, forward, up))


def settle_hand(rig, side, start, reached, end, landmark, *, outward=0., forward=0., up=0.):
    """Replace one stopped character's wrist motion from its current pose to a held pose.

    Ease from start to reached, then hold through end. Landmark offsets use the same
    anatomical axes and world units as key_hand_offset. Requires keyed IK location.
    """
    scene = bpy.context.scene
    if (not all(type(f) is int for f in (start, reached, end))
            or not scene.frame_start <= start < reached < end <= scene.frame_end or reached - start < 2):
        raise ValueError("Choose start, reached and end inside the clip with room for an in-between and a hold")
    if isinstance(rig, str):
        rig = scene.objects[rig]
    if side not in SIDES:
        raise ValueError("Choose anatomical side 'L' or 'R'")
    control_name = "hand_ik." + side
    scene.frame_set(start)
    control = _motion["_location_control"](rig, control_name, allow_keyed=True)
    ad = rig.animation_data
    if not ad or not ad.action or not ad.action_slot:
        raise ValueError("Use the active walk Action and its Rigify slot")
    bag = anim_utils.action_get_channelbag_for_slot(ad.action, ad.action_slot)
    path = control.path_from_id("location")
    curves = [bag.fcurves.find(path, index=i) for i in range(3)] if bag else []
    if not curves or any(fc is None or fc.lock or fc.mute or fc.modifiers for fc in curves):
        raise ValueError("The active Action needs three editable hand IK location curves")
    # Capture every target before replacing any keys. The original start pose matters
    # even when the existing clip jumps to the shoulder on the very next frame.
    targets = {start: _world(rig, control_name)}
    for frame in (start, reached, end):
        scene.frame_set(frame)
        if abs(rig.pose.bones["upper_arm_parent." + side]["IK_FK"]) > 1e-5:
            raise ValueError("Keep this arm in IK during the gesture")
        if frame != start:
            targets[frame] = _hand_target(rig, side, landmark, outward, forward, up)
    for fc in curves:
        keys = fc.keyframe_points
        # Auto smoothing can propagate a new wrist height backwards into the walk.
        # Keep the incoming tangent of the boundary at its authored value.
        boundary = next((key for key in keys if key.co.x == start), None)
        if boundary is None:
            boundary = keys.insert(start, fc.evaluate(start))
        incoming = boundary.handle_left.copy()
        boundary.handle_left_type = "FREE"
        boundary.handle_left = incoming
        for i in reversed(range(len(keys))):
            if start < keys[i].co.x <= end:
                keys.remove(keys[i], fast=True)
        fc.update()
    for frame, target in targets.items():
        key_control_world(rig, control_name, frame, target)
    for fc in curves:
        for key in fc.keyframe_points:
            if key.co.x == start:
                key.interpolation = "SINE"
                key.easing = "EASE_IN_OUT"
            elif key.co.x == reached:
                key.interpolation = "LINEAR"
        fc.update()
    scene.frame_set(start)


def block_walk(rig, displacement_world, *, first=1, steps=None, step_frames=None,
               hold_frames=None, lead="L"):
    """Key a rest-to-rest forward walk on an unanimated rig in standing IK.

    displacement_world is the world-space change of the midpoint of the feet
    in Blender units. Turn the clean character to face the route before keying.
    Both feet finish at their own starting positions plus that displacement.
    steps includes the closing footfall. The output is a small editable set
    of torso, foot and hand keys. Returns frame numbers for later acting edits.
    """
    scene = bpy.context.scene
    delta = Vector(displacement_world)
    if len(delta) != 3 or not all(math.isfinite(v) for v in delta) or delta.length < 1e-6:
        raise ValueError("Supply a finite nonzero displacement in world coordinates")
    if abs(delta.z) > 1e-6 * delta.length or lead not in SIDES or type(first) is not int:
        raise ValueError("Use a level route, integer start frame and lead 'L' or 'R'")
    ad = rig.animation_data
    if ad and (ad.action or any(not t.mute and t.strips for t in ad.nla_tracks)):
        raise ValueError("Start this blockout from a clean rig with no active Action or NLA")
    scene.frame_set(first)
    for side in SIDES:
        for limb in ("upper_arm_parent.", "thigh_parent."):
            if abs(rig.pose.bones[limb + side]["IK_FK"]) > 1e-5:
                raise ValueError("The arm and leg controls must be in IK at the starting pose")
    for control in ("torso", "foot_ik.L", "foot_ik.R", "hand_ik.L", "hand_ik.R"):
        _motion["_location_control"](rig, control, allow_keyed=False)
    direction = delta.normalized()
    if direction.dot(forward_world(rig)) < .94:
        raise ValueError("Face the standing character along the route before calling block_walk")
    feet = {s: _world(rig, "foot_ik." + s) for s in SIDES}
    hips = {s: _world(rig, "DEF-thigh." + s) for s in SIDES}
    shoulders = {s: _world(rig, "DEF-upper_arm." + s) for s in SIDES}
    middle = (feet["L"] + feet["R"]) * .5
    torso = _world(rig, "torso")
    leg = sum(hips[s].z - feet[s].z for s in SIDES) * .5
    left = UP.cross(direction)
    stance_width = (feet["L"] - feet["R"]).dot(left)
    if leg <= 1e-6 or stance_width <= 1e-6:
        raise ValueError("Expected an upright standing pose, one foot on either side")
    fps = scene.render.fps / scene.render.fps_base
    if steps is None:
        steps = max(2, math.ceil(delta.length / (.52 * leg)) + 1)
    if step_frames is None:
        step_frames = max(6, round(.44 * fps))
    if hold_frames is None:
        hold_frames = max(3, round(.35 * fps))
    if not all(type(v) is int for v in (steps, step_frames, hold_frames)):
        raise ValueError("steps, step_frames and hold_frames must be integers")
    if steps < 2 or step_frames < 6 or hold_frames < 1:
        raise ValueError("Use at least two footfalls, six frames per footfall and one hold frame")

    # Relax each wrist near its hip, respecting the reach of this character.
    hands = {}
    for s in SIDES:
        elbow = _world(rig, "DEF-forearm." + s)
        arm = (shoulders[s] - elbow).length + (elbow - _world(rig, "DEF-hand." + s)).length
        outward = left if s == "L" else -left
        hand = hips[s] + outward * (.22 * arm) + direction * (.07 * arm)
        hand.z = max(hand.z, shoulders[s].z - .90 * arm)
        hands[s] = hand

    def key_pose(frame, footprint, weight_shift):
        travel = (footprint["L"] + footprint["R"]) * .5 - middle
        travel.z = 0
        body_offset = travel + weight_shift
        # A long split stance needs a lower pelvis to keep both ankles in reach.
        # Preserve each leg's standing hip-to-ankle length before loading the foot.
        for s in SIDES:
            offset = hips[s] + body_offset - footprint[s]
            reach_squared = (hips[s] - feet[s]).length_squared
            height = math.sqrt(max(0., reach_squared - offset.x ** 2 - offset.y ** 2))
            body_offset.z -= max(0., offset.z - height)
        key_control_world(rig, "torso", frame, torso + body_offset)
        for side, opposite in (("L", "R"), ("R", "L")):
            key_control_world(rig, "foot_ik." + side, frame, footprint[side])
            stride = (footprint[opposite] - feet[opposite] - footprint[side] + feet[side]).dot(direction)
            hand_target = hands[side] + body_offset + direction * (.28 * stride)
            key_control_world(rig, "hand_ik." + side, frame, hand_target)

    floor = {s: p.copy() for s, p in feet.items()}
    hold = Vector((0, 0, 0))
    key_pose(first, floor, hold)
    footfalls = []
    for step in range(steps):
        moving = lead if step % 2 == 0 else ("R" if lead == "L" else "L")
        support_sign = -1 if moving == "L" else 1
        start = first + step * step_frames
        target = feet[moving] + delta * min(1, (step + 1) / (steps - 1))
        support = left * (support_sign * .18 * stance_width)
        # Carry the belt over the stance foot while both feet still touch down.
        early_travel = (target - floor[moving]) * .075
        release = start + max(1, step_frames // 5)
        landing = start + step_frames
        key_pose(release, floor, support + early_travel - UP * (.025 * leg))
        passing = floor.copy()
        lift = min(.09 * leg, .22 * (target - floor[moving]).length)
        passing[moving] = floor[moving].lerp(target, .52) + UP * lift
        key_pose(start + round(.59 * step_frames), passing, support - UP * (.012 * leg))
        # Clear the ground before travelling and brake horizontally before touchdown.
        edge = max(1, step_frames // 8)
        key_control_world(rig, "foot_ik." + moving, release + edge, floor[moving] + UP * (.25 * lift))
        key_control_world(rig, "foot_ik." + moving, landing - edge, target + UP * (.25 * lift))
        floor[moving] = target
        key_pose(landing, floor, hold)
        footfalls.append({"frame": landing, "side": moving})
    arrival = first + steps * step_frames
    last = arrival + hold_frames
    key_pose(last, floor, hold)
    action = rig.animation_data
    bag = anim_utils.action_get_channelbag_for_slot(action.action, action.action_slot)
    for curve in bag.fcurves:
        for key in curve.keyframe_points:
            key.interpolation = "BEZIER"
            key.handle_left_type = key.handle_right_type = "AUTO_CLAMPED"
    scene.frame_start, scene.frame_end = first, last
    scene.frame_set(first)
    return {"first": first, "arrival": arrival, "last": last, "footfalls": footfalls}


def read_walk_plan(rig):
    """Read the original reference, displacement and timing from the active walk Action."""
    if isinstance(rig, str):
        rig = bpy.context.scene.objects[rig]
    action = rig.animation_data.action if rig.animation_data else None
    record = action.get("rigify_walk_plan_v1") if action else None
    if not record:
        raise ValueError("This Action has no saved walk plan. Call capture_travel on the original scene.")
    return json.loads(record)


def save_walk_blockout(rig, mesh, output_path, *, distance=None, displacement_world=None,
                      hold_frames=None, steps=None, step_frames=None, lead="L"):
    """Create the walk on a clean rig, save, reopen and measure it. Rig/mesh may be names.

    Supply one of distance (forward along the character's heading) or displacement_world.
    Both use Blender world units. Return path, plan and the reopened blockout's report.
    """
    path = Path(output_path)
    if not path.is_absolute() or path.suffix.lower() != ".blend" or path.is_dir():
        raise ValueError("Provide an absolute .blend file path for the blockout")
    if (distance is None) == (displacement_world is None):
        raise ValueError("Supply either distance or displacement_world")
    if distance is not None and (not math.isfinite(distance) or distance <= 0):
        raise ValueError("distance must be a positive finite forward length in Blender units")
    path.parent.mkdir(parents=True, exist_ok=True)
    techniques = Path(__file__).resolve().parent
    review = run_path(str(techniques / "travel_review.py"))
    save = run_path(str(techniques.parent / "blend_file.py"))["save_and_reopen"]
    if isinstance(rig, str):
        rig = bpy.context.scene.objects[rig]
    rig_name = rig.name
    ref = review["capture_travel"](rig, mesh)
    delta = list(Vector(ref["forward_world"]) * distance if distance is not None else Vector(displacement_world))
    plan = block_walk(rig, delta, first=bpy.context.scene.frame_start, steps=steps,
                      step_frames=step_frames, hold_frames=hold_frames, lead=lead)
    rig.animation_data.action["rigify_walk_plan_v1"] = json.dumps(
        {"ref": ref, "delta": delta, "plan": plan}, separators=(",", ":"))
    # Keep the editable checkpoint even when the full skin review suggests a repair.
    opened = save(path)
    data = read_walk_plan(rig_name)
    plan = data["plan"]
    hands_low = {"L": "hip", "R": "hip"}
    report = review["review_travel"](data["ref"], data["delta"], start_hands=hands_low,
                                     end_hands=hands_low, min_steps=len(plan["footfalls"]),
                                     face_world=data["ref"]["forward_world"],
                                     hold_frames=min(3, plan["last"] - plan["arrival"] + 1))
    return {"path": opened, "plan": plan, "report": report}
