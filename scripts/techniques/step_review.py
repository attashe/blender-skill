"""Read a single step from evaluated pose-bone heads in Blender world units."""
import math

import bpy
from mathutils import Vector


def _poses(rig, controls, frames):
    scene = bpy.context.scene
    current, subframe = scene.frame_current, scene.frame_subframe
    poses = {}
    try:
        for frame in frames:
            scene.frame_set(frame)
            evaluated = rig.evaluated_get(bpy.context.evaluated_depsgraph_get())
            poses[frame] = {role: evaluated.matrix_world @ evaluated.pose.bones[name].head
                            for role, name in controls.items()}
    finally:
        scene.frame_set(current, subframe=subframe)
    return poses


def _unit(vector, label):
    value = Vector(vector)
    if len(value) != 3 or not all(math.isfinite(v) for v in value) or value.length == 0:
        raise ValueError(f"{label} must be a finite non-zero 3D direction")
    return value.normalized()


def capture_step(rig, body, stance, swing, *, up=(0, 0, 1), forward=None):
    """Capture both input endpoints and the stance-ward axis as JSON-safe values.

    The three names identify a body landmark and the two foot landmarks.
    For staggered feet, supply world forward to exclude travel along the floor.
    """
    scene = bpy.context.scene
    rig = scene.objects[rig] if isinstance(rig, str) else rig
    controls = dict(body=body, stance=stance, swing=swing)
    if rig.type != 'ARMATURE' or len(set(controls.values())) != 3:
        raise ValueError("Choose three distinct pose bones on the character's armature")
    first, last = scene.frame_start, scene.frame_end
    if first >= last:
        raise ValueError("The source playback range must contain at least two frames")
    poses = _poses(rig, controls, (first, last))
    normal = _unit(up, "up")
    separation = poses[first]['stance'] - poses[first]['swing']
    side = separation - normal * separation.dot(normal)
    if forward is not None:
        front = _unit(forward, "forward")
        front -= normal * front.dot(normal)
        if front.length < 1e-6:
            raise ValueError("Choose a forward direction along the support plane")
        front.normalize()
        side -= front * side.dot(front)
    if side.length <= separation.length * 1e-6:
        raise ValueError("The two input foot landmarks need visible lateral separation")
    return dict(rig=rig.name, controls=controls, range=[first, last],
                fps=scene.render.fps / scene.render.fps_base, up=list(normal),
                toward_stance=list(side.normalized()), stance_width=side.length,
                start={role: list(point) for role, point in poses[first].items()},
                end={role: list(point) for role, point in poses[last].items()})


def review_step(reference, *, release, touchdown, acceptance):
    """Sample the original interval, one integer frame at a time, in the open scene.

    Positive projections mean travel toward the named support or down for dip.
    Error and drift are 3D distances. All measurements describe control heads.
    """
    scene = bpy.context.scene
    first, last = reference['range']
    if (not all(type(f) is int for f in (release, touchdown, acceptance))
            or not first <= release < touchdown < acceptance <= last):
        raise ValueError("Choose release < touchdown < acceptance inside the input playback range")
    controls = reference['controls']
    poses = _poses(scene.objects[reference['rig']], controls, range(first, last + 1))
    start, end = poses[first], poses[last]
    side, up = Vector(reference['toward_stance']), Vector(reference['up'])
    received = poses[acceptance]['body'] - poses[touchdown]['body']
    goal = Vector(reference['end']['swing'])
    heights = [(pose['swing'] - start['swing']).dot(up) for pose in poses.values()]
    vertical_travel = sum(abs(b - a) for a, b in zip(heights, heights[1:]))
    single_arc_travel = (max(heights) - heights[0]) + (max(heights) - heights[-1])
    playback_range = [scene.frame_start, scene.frame_end]
    fps = scene.render.fps / scene.render.fps_base
    return dict(
        playback_range=playback_range, range_unchanged=playback_range == reference['range'],
        fps=fps, fps_unchanged=math.isclose(fps, reference['fps']),
        start_error={role: (start[role] - Vector(reference['start'][role])).length for role in controls},
        end_error={role: (end[role] - Vector(reference['end'][role])).length for role in controls},
        toward_stance_at_release=(poses[release]['body'] - start['body']).dot(side),
        toward_swing_after_touchdown=-received.dot(side),
        body_dip_after_touchdown=-received.dot(up),
        swing_max_drift_before_release=max((poses[f]['swing'] - start['swing']).length
                                           for f in range(first, release + 1)),
        swing_extra_vertical_travel=max(0.0, vertical_travel - single_arc_travel),
        swing_error_at_touchdown=(poses[touchdown]['swing'] - goal).length,
        swing_max_error_after_touchdown=max((poses[f]['swing'] - goal).length for f in range(touchdown, last + 1)),
        stance_max_drift=max((pose['stance'] - start['stance']).length for pose in poses.values()),
        last_interval_motion={role: (end[role] - poses[last - 1][role]).length for role in controls},
    )
