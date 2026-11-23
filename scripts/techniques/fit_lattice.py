"""Fit a native lattice once; lift its controls inside a world-space ellipsoid."""
from math import isfinite

import bpy
from mathutils import Vector


_OWNER = "_blender_modular_scenes_fit_lattice"


def _is_fitted_cage(obj):
    # Recognise saved cages from the original rock example as well.
    return obj.type == "LATTICE" and (obj.get(_OWNER) or obj.get("_experiment_fit_lattice"))


def _bounds(points):
    axes = list(zip(*points))
    return Vector(min(axis) for axis in axes), Vector(max(axis) for axis in axes)


def fit_lattice(obj, *, resolution=(5, 4, 4), name=None):
    """Append an editable lattice fitted to the evaluated object's local bounding box.

    The cage follows the object's transforms. Repeating the same request returns its
    existing cage, preserving all edits. Resolution is ordered along object-local XYZ.
    """
    dims = tuple(resolution)
    if len(dims) != 3 or any(type(n) is not int or not 2 <= n <= 64 for n in dims):
        raise ValueError("resolution needs three integers from 2 to 64")
    for mod in obj.modifiers:
        existing = mod.object if mod.type == "LATTICE" else None
        if existing and _is_fitted_cage(existing) and existing.parent == obj:
            data = existing.data
            if (name is not None and name != existing.name) or dims != (data.points_u, data.points_v, data.points_w):
                raise ValueError(f"{obj.name} already has fitted cage {existing.name!r} with another name or resolution")
            return existing
    requested = name if name is not None else f"{obj.name} cage"
    if not isinstance(requested, str) or not requested.strip() or bpy.data.objects.get(requested):
        raise ValueError("Choose an unused, nonempty cage object name")
    if not obj.users_collection:
        raise ValueError("The target must belong to a collection")
    evaluated = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    low, high = _bounds(evaluated.bound_box)
    if any(high[i] <= low[i] for i in range(3)):
        raise ValueError("Fitting this volume lattice requires a nonzero object extent along all three local axes")
    try:
        evaluated.matrix_world.to_3x3().inverted()
    except ValueError as exc:
        raise ValueError("The target's world transform must be invertible") from exc

    data = bpy.data.lattices.new(requested)
    cage = modifier = None
    try:
        cage = bpy.data.objects.new(requested, data)
        if cage.name != requested:
            raise ValueError("Blender could not preserve the requested cage name")
        obj.users_collection[0].objects.link(cage)
        data.points_u, data.points_v, data.points_w = dims
        if (data.points_u, data.points_v, data.points_w) != dims:
            raise ValueError("Blender could not allocate this lattice resolution")
        data.interpolation_type_u = data.interpolation_type_v = data.interpolation_type_w = "KEY_LINEAR"
        rest_low, rest_high = _bounds(point.co for point in data.points)
        cage.parent = obj
        cage.scale = [(high[i] - low[i]) / (rest_high[i] - rest_low[i]) for i in range(3)]
        cage.location = [low[i] - rest_low[i] * cage.scale[i] for i in range(3)]
        cage[_OWNER] = True
        modifier = obj.modifiers.new(requested, "LATTICE")
        modifier.object = cage
        bpy.context.view_layer.update()
        return cage
    except Exception:
        if modifier is not None:
            obj.modifiers.remove(modifier)
        if cage is not None:
            bpy.data.objects.remove(cage, do_unlink=True)
        bpy.data.lattices.remove(data)
        raise


def lift_region(cage, center, radii, dz):
    """Set a world-Z lift from rest. center and positive XYZ radii use world coordinates.

    All distances are in Blender world units. dz specifies peak control travel.
    Interpolation and an optional modifier vertex group determine surface motion.
    Recalculates every control from rest, replacing previous and manual control edits.
    Returns the number of rest controls inside the region. Use dz=0 to restore neutral.
    """
    if not _is_fitted_cage(cage):
        raise ValueError("Pass a cage returned by fit_lattice")
    if cage.data.users - int(cage.data.use_fake_user) > 1:
        raise ValueError("Make the cage's lattice data single-user before changing its controls")
    center, radii = Vector(center), Vector(radii)
    if (len(center) != 3 or len(radii) != 3 or not all(map(isfinite, (*center, *radii, dz)))
            or min(radii) <= 0):
        raise ValueError("Use three finite world coordinates, three positive radii, and a finite dz")
    matrix = cage.evaluated_get(bpy.context.evaluated_depsgraph_get()).matrix_world.copy()
    local_lift = matrix.to_3x3().inverted() @ Vector((0, 0, dz))
    weights = []
    for point in cage.data.points:
        delta = matrix @ point.co - center
        t = min(1.0, sum((delta[i] / radii[i]) ** 2 for i in range(3)))
        weights.append((1 - t) ** 2 * (1 + 2 * t))
    count = sum(weight > 0 for weight in weights)
    if dz and not count:
        raise ValueError("The ellipsoid contains no rest controls; enlarge it or move its center")
    for point, weight in zip(cage.data.points, weights):
        point.co_deform = point.co + local_lift * weight
    cage.data.update_tag()
    bpy.context.view_layer.update()
    return count
