"""Review a straight, level, rest-to-rest Rigify walk in Blender world units."""
import hashlib
import json
from collections import deque

import bpy
import numpy as np
from mathutils import Quaternion, Vector


SIDES = ("L", "R")


def _object(value):
    return bpy.context.scene.objects[value] if isinstance(value, str) else value


def _skin(mesh, deps):
    evaluated = mesh.evaluated_get(deps)
    vertices = evaluated.data.vertices
    if len(vertices) != len(mesh.data.vertices):
        raise ValueError("Use a skinned mesh whose evaluated vertices retain their original indices")
    xyz = np.empty(len(vertices) * 3, dtype=np.float32)
    vertices.foreach_get("co", xyz)
    matrix = np.array(evaluated.matrix_world)
    return xyz.reshape(-1, 3) @ matrix[:3, :3].T + matrix[:3, 3]


def _driver_signature(rig):
    curves = rig.animation_data.drivers if rig.animation_data else ()
    signatures = []
    for curve in curves:
        drv = curve.driver
        variables = [(v.name, v.type, [(t.id.name_full if t.id else None, t.data_path,
                      t.bone_target, t.transform_space, t.transform_type, t.rotation_mode)
                     for t in v.targets]) for v in drv.variables]
        signatures.append((curve.data_path, curve.array_index, curve.mute, drv.type,
                           drv.expression, drv.use_self, variables))
    return [len(curves), hashlib.sha256(json.dumps(sorted(signatures)).encode()).hexdigest()]


def _landmarks(rig, deps):
    obj = rig.evaluated_get(deps)
    matrix = obj.matrix_world
    bones = obj.pose.bones
    def point(name):
        return np.asarray(matrix @ bones["DEF-" + name].head)
    return dict(pelvis=point("spine"),
                chest_rotation=(matrix @ bones["DEF-spine.003"].matrix).to_quaternion(),
                hips={s: point("thigh." + s) for s in SIDES},
                shoulders={s: point("upper_arm." + s) for s in SIDES},
                wrists={s: point("hand." + s) for s in SIDES},
                ankles={s: point("foot." + s) for s in SIDES})


def _sole_centers(xyz, soles):
    return np.array([np.median(xyz[soles[s]], axis=0) for s in SIDES])


def capture_travel(rig, mesh, *, floor_z=None):
    """Capture the standing input at scene.frame_start. Persist the returned dict as JSON.

    Standard upright Rigify human, Z-up, level ground and a weight-painted body mesh.
    A is the midpoint of the two sole contact patches. Set floor_z for an explicit floor.
    """
    rig, mesh = _object(rig), _object(mesh)
    if not any(m.type == 'ARMATURE' and m.object == rig for m in mesh.modifiers):
        raise ValueError("Pass the visible character mesh deformed by the specified rig")
    scene = bpy.context.scene
    previous = scene.frame_current, scene.frame_subframe
    try:
        scene.frame_set(scene.frame_start)
        deps = bpy.context.evaluated_depsgraph_get()
        xyz = _skin(mesh, deps)
        pose = _landmarks(rig, deps)
        leg = float(np.mean([np.linalg.norm(pose['hips'][s] - pose['ankles'][s]) for s in SIDES]))
        feet, soles = {}, {}
        for s in SIDES:
            groups = {g.index for g in mesh.vertex_groups if g.name in ("DEF-foot." + s, "DEF-toe." + s)}
            ids = [v.index for v in mesh.data.vertices if sum(g.weight for g in v.groups if g.group in groups) > .25]
            if not ids:
                raise ValueError(f"No weighted toe/foot geometry on {mesh.name} for side {s}")
            z = xyz[ids, 2]
            feet[s] = ids
            soles[s] = np.asarray(ids)[z <= z.min() + .012 * leg].tolist()
        left = pose['hips']['L'] - pose['hips']['R']
        forward = np.cross(left, [0, 0, 1])
        if leg <= 0 or np.linalg.norm(forward) < 1e-6:
            raise ValueError("Capture an upright character with left and right hips apart")
        centers = _sole_centers(xyz, soles)
        return dict(rig=rig.name, mesh=mesh.name, vertices=len(xyz), drivers=_driver_signature(rig),
                    feet=feet, soles=soles, leg=leg, forward_world=(forward / np.linalg.norm(forward)).tolist(),
                    start_midfeet_world=centers.mean(axis=0).tolist(), sole_span_world=(centers[0] - centers[1]).tolist(),
                    pelvis=pose['pelvis'].tolist(),
                    chest_rotation=list(pose['chest_rotation']), floor_z=float(floor_z if floor_z is not None
                        else min(xyz[ids, 2].min() for ids in feet.values())))
    finally:
        scene.frame_set(previous[0], subframe=previous[1])


def _runs(mask):
    changes = np.flatnonzero(np.diff(np.r_[False, mask, False].astype(int)))
    return zip(changes[::2], changes[1::2] - 1)


def _hand_error(pose, side, goal, leg):
    if side not in SIDES:
        raise ValueError("Hand goals use anatomical side 'L' or 'R'")
    wrist = pose['wrists'][side]
    if not isinstance(goal, str):
        target = np.asarray(goal, dtype=float)
        if target.shape != (3,) or not np.isfinite(target).all():
            raise ValueError("A world hand goal must contain three finite coordinates")
        return float(np.linalg.norm(wrist - target)), .06 * leg
    if goal == 'shoulder_height':
        return abs(float(wrist[2] - pose['shoulders'][side][2])), .14 * leg
    if goal == 'hip':
        offset = wrist - pose['hips'][side]
        return max(float(np.linalg.norm(offset[:2])), abs(float(offset[2]))), .29 * leg
    raise ValueError("A hand goal is 'hip', 'shoulder_height', or a world XYZ position")


def review_travel(ref, displacement_world, *, start_hands=None, end_hands=None, hold_frames=3,
                  min_steps=2, face_world=None, raise_after_arrival=None, smooth_raise=True,
                  max_lateral_drift=None):
    """Review the current scene range against capture_travel. Does not change any keys.

    Units are Blender world units. Hand goals are {'L' or 'R': landmark or world XYZ}.
    min_steps counts completed forward swings, including the closing foot. For a deliberate
    hand lift after stopping, set raise_after_arrival to its anatomical side, 'L' or 'R'.
    Use smooth_raise=False for a deliberately stepped lift; timing is still checked.
    max_lateral_drift sets the allowed pelvis excursion across the route, in world units.
    """
    delta = np.asarray(displacement_world, dtype=float)
    if delta.shape != (3,) or not np.isfinite(delta).all() or abs(delta[2]) > 1e-5 or np.linalg.norm(delta) < 1e-6:
        raise ValueError("Choose a nonzero finite displacement on the level XY plane")
    if type(hold_frames) != int or hold_frames < 1 or type(min_steps) != int or min_steps < 1:
        raise ValueError("hold_frames and min_steps must be positive integers")
    if raise_after_arrival is not None and raise_after_arrival not in SIDES:
        raise ValueError("raise_after_arrival must be anatomical side 'L' or 'R'")
    if max_lateral_drift is not None:
        max_lateral_drift = np.asarray(max_lateral_drift, dtype=float)
        if max_lateral_drift.shape != () or not np.isfinite(max_lateral_drift) or max_lateral_drift < 0:
            raise ValueError("max_lateral_drift must be a finite nonnegative distance")
    if face_world is not None:
        facing_goal = np.asarray(face_world, dtype=float)
        if (facing_goal.shape != (3,) or not np.isfinite(facing_goal).all()
                or np.linalg.norm(facing_goal[:2]) < 1e-6):
            raise ValueError("face_world must be a finite 3D heading with a horizontal component")
    direction = delta / np.linalg.norm(delta)
    lateral = np.array([-direction[1], direction[0]])
    pelvis_start = np.asarray(ref["pelvis"])[:2]
    span = ref.get("sole_span_world")  # Older saved Actions carry only the sole vertex IDs.
    scene = bpy.context.scene
    rig, mesh = _object(ref['rig']), _object(ref['mesh'])
    if len(mesh.data.vertices) != ref['vertices']:
        raise ValueError("Mesh topology changed; the captured sole indices are no longer valid")
    first, last = scene.frame_start, scene.frame_end
    previous = scene.frame_current, scene.frame_subframe
    ends, soles, foot_skin = {}, [], {s: [] for s in SIDES}
    held = deque(maxlen=hold_frames)
    wrist_heights, pelvis_offsets = [], []
    try:
        for f in range(first, last + 1):
            scene.frame_set(f)
            deps = bpy.context.evaluated_depsgraph_get()
            xyz = _skin(mesh, deps)
            centers = _sole_centers(xyz, ref['soles'])
            soles.append(centers.mean(axis=0))
            if span is None:
                span = centers[0] - centers[1]
            evaluated = rig.evaluated_get(deps)
            bones = evaluated.pose.bones
            pelvis = np.asarray(evaluated.matrix_world @ bones["DEF-spine"].head)
            pelvis_offsets.append(float((pelvis[:2] - pelvis_start) @ lateral))
            for s in SIDES:
                foot_skin[s].append(xyz[ref['feet'][s]])
            if f >= last - hold_frames + 1:
                held.append(xyz)
            if f in (first, last):
                ends[f] = _landmarks(rig, deps)
            if raise_after_arrival is not None:
                offset = (bones["DEF-hand." + raise_after_arrival].head
                          - bones["DEF-upper_arm." + raise_after_arrival].head)
                wrist_heights.append((evaluated.matrix_world.to_3x3() @ offset).z)
    finally:
        scene.frame_set(previous[0], subframe=previous[1])

    leg, floor = ref['leg'], ref['floor_z']
    repair = []
    def check(ok, advice):
        if not ok:
            repair.append(advice)
    origin = np.array(ref['start_midfeet_world'])
    start_error = float(np.linalg.norm((soles[0] - origin)[:2]))
    error = float(np.linalg.norm((soles[-1] - origin - delta)[:2]))
    pelvis_error = float(np.linalg.norm((ends[last]['pelvis'] - ref['pelvis'] - delta)[:2]))
    check(start_error <= .06 * leg, f"Frame {first}: restore the two start footprints at A.")
    check(error <= .06 * leg, f"Frame {last}: place both soles around B; check their midpoint in world space.")
    check(pelvis_error <= .15 * leg, f"Frame {last}: carry the pelvis to B with the feet; inspect the body travel control.")
    width = abs(float(np.asarray(span)[:2] @ lateral))
    limit = max(.15 * leg, .5 * width + .05 * leg) if max_lateral_drift is None else float(max_lateral_drift)
    peak = int(np.argmax(np.abs(pelvis_offsets)))
    lateral_report = dict(frame=first + peak, distance=round(abs(pelvis_offsets[peak]), 5), limit=round(limit, 5))
    check(abs(pelvis_offsets[peak]) <= limit,
          f"Frame {first + peak}: the pelvis drifts {abs(pelvis_offsets[peak]):.3g} sideways from its route "
          f"(allowed {limit:.3g}); correct the body key while retaining the support transfer.")
    check(bool(rig.animation_data and rig.animation_data.action), "Restore the assigned, editable Action on the rig.")
    drivers = _driver_signature(rig)
    check(drivers == ref['drivers'], "Restore the source rig drivers; work on the assigned Action without clearing animation_data.")
    landings, slip, clear = [], {}, {}
    for s in SIDES:
        pts = np.asarray(foot_skin[s])
        z = pts[:, :, 2] - floor
        clear[s] = np.min(z, axis=1)
        planted = clear[s] <= .005 * leg
        check(planted[0] and planted[-1], f"{s} foot: ground the starting and stopping poses.")
        low = int(np.argmin(clear[s]))
        check(clear[s][low] >= -.006 * leg, f"Frame {first + low}: raise the {s} sole out of the floor.")
        middle = np.median(pts[:, :, :2], axis=1)
        for a, b in _runs(~planted):
            if a > 0 and b + 1 < len(pts) and max(clear[s][a:b + 1]) > .012 * leg:
                advance = float(np.dot(middle[b + 1] - middle[a - 1], direction[:2]))
                if advance > .025 * leg:
                    landings.append((int(first + b + 1), s))
        max_slip, interval = 0., None
        for a, b in _runs(planted):
            travel = 0.
            for j in range(a, b):
                touching = (z[j] <= .005 * leg) & (z[j+1] <= .005 * leg)
                if touching.any():
                    travel += float(np.median(np.linalg.norm(pts[j+1, touching, :2] - pts[j, touching, :2], axis=1)))
            if travel > max_slip:
                max_slip, interval = travel, [int(a+first), int(b+first)]
        slip[s] = dict(distance=round(max_slip, 5), frames=interval)
        check(max_slip <= .025 * leg, f"{s} sole slides during {interval}: hold the planted foot in world space.")
    landings.sort()
    check(len(landings) >= min_steps and len({s for _, s in landings}) == 2
          and all(a[1] != b[1] for a, b in zip(landings, landings[1:])),
          "Repair step order: lift, advance and land each foot while the opposite foot supports the body.")
    raise_timing = None
    if raise_after_arrival is not None:
        rise = wrist_heights[-1] - wrist_heights[0]
        arrival = landings[-1][0] if landings else None
        onset = None
        peak_frames, peak_rise, peak_fraction = None, None, None
        if rise < .08 * leg:
            repair.append(f"Frame {last}: the {raise_after_arrival} wrist needs a distinct rise from its starting height.")
        else:
            # Require two successive samples above one quarter of the final shoulder-relative rise.
            high = np.asarray(wrist_heights) >= wrist_heights[0] + .25 * rise
            sustained = np.flatnonzero(high[:-1] & high[1:])
            onset = first + int(sustained[0]) if len(sustained) else None
            if onset is None:
                repair.append(f"Hold the raised {raise_after_arrival} wrist for more than one frame.")
            elif arrival is not None and onset <= arrival:
                repair.append(f"The {raise_after_arrival} wrist rises at frame {onset}; "
                              f"delay its lift until after the last landing at frame {arrival}.")
            if arrival is not None and arrival < last:
                # At normal playback rates a single interval containing most of the lift
                # leaves no readable intermediate pose. Sparse timing samples cannot test this.
                changes = np.diff(wrist_heights[arrival - first:])
                i = int(np.argmax(changes))
                peak_frames = [arrival + i, arrival + i + 1]
                peak_rise = max(0., float(changes[i]))
                peak_fraction = peak_rise / rise
                dt = scene.render.fps_base / scene.render.fps
                if smooth_raise and onset is not None and onset > arrival and dt <= .05 and peak_fraction >= 2/3:
                    repair.append(f"Frames {peak_frames}: {peak_fraction:.0%} of the {raise_after_arrival} "
                                  f"wrist lift happens in one frame. Keep the low wrist at the last landing "
                                  f"({arrival}), move early high keys later, then allow intermediate heights "
                                  "before holding the final pose.")
        raise_timing = dict(side=raise_after_arrival, last_landing_frame=arrival,
                            sustained_quarter_rise_frame=onset, shoulder_relative_rise=round(rise, 5),
                            peak_post_landing_frames=peak_frames, peak_post_landing_rise=peak_rise,
                            peak_fraction_of_lift=peak_fraction)
    flight = [[first + int(a), first + int(b)] for a,b in _runs(np.minimum(clear['L'], clear['R']) > .005 * leg)]
    check(not flight, f"Both feet are airborne at {flight}: keep one sole on the ground during the transfer.")
    hand_errors = {}
    for phase, frame, goals in (('start', first, start_hands), ('end', last, end_hands)):
        for side, goal in (goals or {}).items():
            diff, tolerance = _hand_error(ends[frame], side, goal, leg)
            hand_errors[f'{phase}.{side}'] = round(diff, 5)
            check(diff <= tolerance, f"Frame {frame}: adjust the {side} wrist to {goal} in the {phase} pose.")
    held_delta = float(max(np.linalg.norm(sample - held[-1], axis=1).max() for sample in held))
    check(len(held) == hold_frames and held_delta <= .006 * leg,
          f"Hold the complete final pose for {hold_frames} frames, including feet, body and wrists.")
    facing = None
    if face_world is not None:
        target = Vector(facing_goal).to_2d()
        current = ends[last]['chest_rotation'] @ Quaternion(ref['chest_rotation']).inverted()
        front = (current @ Vector(ref['forward_world'])).to_2d()
        facing = float(np.degrees(front.angle(target)))
        check(facing <= 20, f"Frame {last}: turn the chest toward the requested final heading.")
    return dict(ok=not repair, repairs=repair, frames=[first,last], start_error=round(start_error,5),
                destination_error=round(error,5), pelvis_error=round(pelvis_error,5),
                midpoint_end=np.round(soles[-1],5).tolist(), landings=landings, airborne_frames=flight,
                support_slip=slip, hand_errors=hand_errors, hold_max_motion=round(held_delta,5),
                chest_heading_error_deg=facing, driver_count=drivers[0], raise_timing=raise_timing,
                lateral_pelvis=lateral_report)
