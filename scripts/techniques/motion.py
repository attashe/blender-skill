"""Small animation probes and keying examples. Import has no scene/file effects.

Call on an owned working copy. No reset, file IO, rendering or object-name lookup.
The keying examples cover Euler rotation, control translation and properties.
key_control_world edits one frame of the active clip. The other keying examples expect free channels.
"""
import math
import bpy
from bpy_extras import anim_utils
from mathutils import Vector


def control_sides(rig, center, front, control_names, *, up=(0, 0, 1)):
    """Group pose controls by anatomical side at the current frame. Read-only.

    center and front accept a pose bone name (its head) or a world-space point.
    Place center on the midline, with front ahead of it. up is a world direction.
    """
    evaluated = rig.evaluated_get(bpy.context.evaluated_depsgraph_get())

    def world_point(point):
        if isinstance(point, str):
            return evaluated.matrix_world @ evaluated.pose.bones[point].head
        return Vector(point)

    origin = world_point(center)
    forward = world_point(front) - origin
    left = Vector(up).normalized().cross(forward)
    if left.length <= max(1e-9, forward.length * 1e-4):
        raise ValueError("Choose a front landmark ahead of the center along the facing direction")
    left.normalize()
    sides = {"left": [], "right": [], "midline": []}
    for name in control_names:
        offset = (world_point(name) - origin).dot(left)
        if abs(offset) <= max(1e-8, forward.length * 1e-5):
            side = "midline"
        else:
            side = "left" if offset > 0 else "right"
        sides[side].append(name)
    return sides


def _direct_channel(target, path, index, *, allow_keyed):
    owner = target.id_data
    full_path = target.path_from_id(path)
    ad = owner.animation_data
    if ad:
        if any(not track.mute and len(track.strips) for track in ad.nla_tracks):
            raise ValueError('Isolate active NLA on a working copy before using this example')
        if any(fc.data_path == full_path and fc.array_index == index for fc in ad.drivers):
            raise ValueError('Requested channel already has a driver')
        if ad.action:
            if not ad.action_slot:
                raise ValueError('Existing Action has no assigned slot')
            bag = anim_utils.action_get_channelbag_for_slot(ad.action, ad.action_slot)
            if not allow_keyed and bag and bag.fcurves.find(full_path, index=index):
                raise ValueError('Requested channel already has keys')
    return owner, full_path


def _free_channel(target, path, index):
    return _direct_channel(target, path, index, allow_keyed=False)


def _finish(owner, path, index, interpolation, cycle):
    ad = owner.animation_data
    bag = anim_utils.action_get_channelbag_for_slot(ad.action, ad.action_slot)
    fc = bag.fcurves.find(path, index=index)
    if fc is None:
        raise RuntimeError('Key insertion did not produce the intended channel')
    for key in fc.keyframe_points:
        key.interpolation = interpolation
        if interpolation == 'BEZIER':
            key.handle_left_type = key.handle_right_type = 'AUTO_CLAMPED'
    if cycle:
        mod = fc.modifiers.new('CYCLES')
        mod.mode_before = mod.mode_after = cycle
    return fc


def _location_control(rig, control_name, *, allow_keyed):
    control = rig.pose.bones[control_name]
    if control.bone.use_connect or any(control.lock_location) or any(
        not constraint.mute and constraint.influence for constraint in control.constraints
    ):
        raise ValueError("Choose an unconnected control with free location channels")
    for axis in range(3):
        _direct_channel(control, "location", axis, allow_keyed=allow_keyed)
    return control


def key_control_world(rig, control_name, frame, target_world):
    """Insert or update a control's location at one frame of the current Action.

    target_world is an absolute position in Blender world units. Conversion uses
    its parent at this frame. Only local location channels are keyed.
    """
    target = Vector(target_world)
    if type(frame) is not int or len(target) != 3 or not all(math.isfinite(v) for v in target):
        raise ValueError("Expected an integer frame and a finite 3D world position")
    bpy.context.scene.frame_set(frame)
    control = _location_control(rig, control_name, allow_keyed=True)
    matrix = rig.matrix_world @ control.matrix
    matrix.translation = target
    local = rig.convert_space(pose_bone=control, matrix=matrix, from_space='WORLD', to_space='LOCAL')
    control.location = local.translation
    if not control.keyframe_insert(data_path="location", frame=frame):
        raise RuntimeError(f"Could not key {control_name!r} at frame {frame}")
    bpy.context.view_layer.update()


def key_ik_world_offset(rig, control_name, first, last, world_delta):
    """Key a world-space translation on a free IK control with a stationary parent.

    Use an active IK limb. Keep the starting orientation and scale. The control's
    three local location channels must be available for this new animation.
    """
    if type(first) is not int or type(last) is not int or first >= last:
        raise ValueError("Choose two increasing integer frames")
    delta = Vector(world_delta)
    if len(delta) != 3 or not all(math.isfinite(v) for v in delta):
        raise ValueError("Expected a finite 3D world offset")
    scene = bpy.context.scene
    scene.frame_set(first)
    control = _location_control(rig, control_name, allow_keyed=False)
    initial = control.location.copy()
    target_world = rig.matrix_world @ control.matrix
    target_world.translation += delta
    scene.frame_set(last)
    target_local = rig.convert_space(
        pose_bone=control, matrix=target_world, from_space='WORLD', to_space='LOCAL'
    )
    control.location = target_local.translation
    control.keyframe_insert(data_path='location', frame=last)
    control.location = initial
    control.keyframe_insert(data_path='location', frame=first)
    scene.frame_set(first)


def _points(points, interpolation, cycle):
    points = list(points)
    if interpolation not in {'LINEAR', 'BEZIER', 'CONSTANT'}:
        raise ValueError('Unsupported interpolation for this small example')
    if cycle not in {None, 'REPEAT', 'REPEAT_OFFSET'}:
        raise ValueError('Unsupported cycle mode')
    if len(points) < 2 or any(not all(math.isfinite(v) for v in pair) for pair in points):
        raise ValueError('At least two finite (frame, value) pairs are required')
    if any(b[0] <= a[0] for a, b in zip(points, points[1:])):
        raise ValueError('Frames must increase strictly')
    return points


def rotation_keys(target, axis, frame_radians, *, interpolation='BEZIER', cycle=None):
    """Object or PoseBone, Euler axis 0/1/2, radians. Returns only the new F-Curve."""
    points = _points(frame_radians, interpolation, cycle)
    if axis not in (0, 1, 2) or target.rotation_mode not in {'XYZ','XZY','YXZ','YZX','ZXY','ZYX'}:
        raise ValueError('Choose an Euler target and a valid local axis')
    owner, path = _free_channel(target, 'rotation_euler', axis)
    for frame, value in points:
        target.rotation_euler[axis] = value
        target.keyframe_insert('rotation_euler', index=axis, frame=frame)
    return _finish(owner, path, axis, interpolation, cycle)


def property_keys(control, name, frame_values, *, interpolation='BEZIER', cycle=None):
    """Animate an existing numeric Object property, retaining unrelated channels."""
    points = _points(frame_values, interpolation, cycle)
    if not isinstance(control, bpy.types.Object) or name not in control:
        raise ValueError('Supply an Object with an existing numeric property')
    if not isinstance(control[name], (int, float)):
        raise ValueError('Control property must be numeric')
    path = '["' + bpy.utils.escape_identifier(name) + '"]'
    owner, full_path = _free_channel(control, path, 0)
    for frame, value in points:
        control[name] = float(value)
        control.keyframe_insert(path, frame=frame)
    return _finish(owner, full_path, 0, interpolation, cycle)


def drive_from_property(target, path, control, name, *, factor=1.0, offset=0.0, index=None):
    """Linear relation on a free transform channel or ShapeKey.value.

    A numeric Object property is the source. Caller chooses axis, units and sign;
    offset is the assembled value. No target geometry or parenting is changed.
    """
    if not isinstance(control, bpy.types.Object) or not isinstance(control.get(name), (int, float)):
        raise ValueError('Source must be an existing numeric Object property')
    if not all(math.isfinite(v) for v in (factor, offset)):
        raise ValueError('Finite factor and offset required')
    target.path_resolve(path)
    _free_channel(target, path, 0 if index is None else index)
    fc = target.driver_add(path) if index is None else target.driver_add(path, index)
    driver = fc.driver
    driver.type = 'SCRIPTED'
    driver.expression = f'{float(offset)!r} + {float(factor)!r} * value'
    var = driver.variables.new()
    var.name = 'value'
    var.type = 'SINGLE_PROP'
    var.targets[0].id = control
    var.targets[0].data_path = '["' + bpy.utils.escape_identifier(name) + '"]'
    return fc


def constant_spin(pivot, axis, rpm, fps, start, endpoint, *, initial_radians=0.0):
    """Unwrapped Euler rotation with linear keys and Repeat Offset.

    endpoint is a boundary sample, normally just after the last delivered loop frame.
    A visible loop additionally requires matching geometry/other channels at the seam.
    """
    if fps <= 0 or endpoint <= start:
        raise ValueError('Positive fps and increasing frame boundaries required')
    final = initial_radians + math.tau * rpm / 60 * (endpoint-start) / fps
    return rotation_keys(pivot, axis, [(start, initial_radians), (endpoint, final)],
                         interpolation='LINEAR', cycle='REPEAT_OFFSET')
