"""Sweep a closed XY profile along an open Bézier path. Run inside Blender 4.3+."""

import math

import bpy


ROUND_PROFILE = ((1, 0), (0, 1), (-1, 0), (0, -1))


def _coordinates(values, size, minimum, label):
    coords = [tuple(float(v) for v in point) for point in values]
    if len(coords) < minimum or any(len(p) != size or not all(map(math.isfinite, p)) for p in coords):
        raise ValueError(f"{label} needs at least {minimum} finite {size}D points")
    if any(a == b for a, b in zip(coords, coords[1:])):
        raise ValueError(f"{label} has coincident consecutive controls")
    return coords


def _point_values(values, count, default, label):
    result = [default] * count if values is None else [float(v) for v in values]
    if len(result) != count or not all(map(math.isfinite, result)):
        raise ValueError(f"Supply one finite {label} per path point")
    return result


def create_sweep(name, points, *, profile=ROUND_PROFILE, radii=None, tilts=None,
                 path_resolution=12, profile_resolution=6, caps=True, twist="MINIMUM",
                 path_handles="AUTO", profile_handles="AUTO"):
    """Create (path_object, profile_object) in the current collection. Import has no scene effects.

    points: local XYZ. profile: one simple local XY loop, without repeating the first point.
    radii scale the profile per knot; tilts are roll in radians. Resolution is per segment.
    Handles can be AUTO for flowing sections or VECTOR for straight segments.
    To revise the result, edit the returned objects' native Bézier points.
    """
    path_xyz = _coordinates(points, 3, 2, "path")
    section_xy = _coordinates(profile, 2, 3, "profile")
    if section_xy[0] == section_xy[-1]:
        raise ValueError("Pass the first profile point only once; the spline closes itself")
    ring = list(zip(section_xy, section_xy[1:] + section_xy[:1]))
    area2 = sum(x * v - y * u for (x, y), (u, v) in ring)
    if not area2:
        raise ValueError("The profile needs a simple loop with nonzero area")
    if area2 < 0:
        section_xy = section_xy[:1] + section_xy[:0:-1]
    factors = _point_values(radii, len(path_xyz), 1.0, "radius")
    rolls = _point_values(tilts, len(path_xyz), 0.0, "tilt")
    if min(factors) <= 0:
        raise ValueError("Use positive radii; a zero radius collapses an entire ring")
    if twist not in {"MINIMUM", "Z_UP"} or {path_handles, profile_handles} - {"AUTO", "VECTOR"}:
        raise ValueError("Use MINIMUM or Z_UP twist and AUTO or VECTOR handles")
    if any(type(n) is not int or not 1 <= n <= 64 for n in (path_resolution, profile_resolution)):
        raise ValueError("Resolution must be 1..64 samples per segment")
    if ((len(path_xyz) - 1) * path_resolution + 1) * len(section_xy) * profile_resolution > 250_000:
        raise ValueError("Over 250,000 sweep vertices; reduce controls or resolution")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Give the path a nonempty object name")
    section_name = f"{name} Profile"
    if name in bpy.data.objects or section_name in bpy.data.objects:
        raise ValueError(f"{name!r} or its profile already exists; edit its curve points")

    created = []

    def curve_object(label, coords, dimensions, resolution, handles, cyclic):
        data = bpy.data.curves.new(label, "CURVE")
        created.append(data)
        data.dimensions = dimensions
        data.resolution_u = resolution
        spline = data.splines.new("BEZIER")
        spline.bezier_points.add(len(coords) - 1)
        for point, xyz in zip(spline.bezier_points, coords):
            point.co = xyz
            point.handle_left_type = point.handle_right_type = handles
        spline.use_cyclic_u = cyclic
        spline.use_smooth = True
        obj = bpy.data.objects.new(label, data)
        created.append(obj)
        if obj.name != label:
            raise ValueError(f"Blender shortened or changed {label!r}; use a shorter unique name")
        bpy.context.collection.objects.link(obj)
        return obj, spline

    try:
        path, spline = curve_object(name, path_xyz, "3D", path_resolution, path_handles, False)
        path.data.twist_mode = twist
        spline.radius_interpolation = spline.tilt_interpolation = "LINEAR"
        for knot, radius, roll in zip(spline.bezier_points, factors, rolls):
            knot.radius, knot.tilt = radius, roll
        section, _ = curve_object(section_name, [(x, y, 0) for x, y in section_xy],
                                  "2D", profile_resolution, profile_handles, True)
        section.data.fill_mode = "NONE"
        section.hide_render = True
        section.hide_set(True)

        tree = bpy.data.node_groups.new(f"{name} Sweep", "GeometryNodeTree")
        created.append(tree)
        interface = tree.interface
        interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
        interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
        profile_socket = interface.new_socket(name="Profile", in_out="INPUT", socket_type="NodeSocketObject")
        profile_socket.default_value = section
        cap_socket = interface.new_socket(name="Fill Caps", in_out="INPUT", socket_type="NodeSocketBool")
        cap_socket.default_value = caps

        def node(kind, x, y):
            item = tree.nodes.new(kind)
            item.location = (x, y)
            return item

        inputs = node("NodeGroupInput", -480, 100)
        info = node("GeometryNodeObjectInfo", -240, 0)
        info.transform_space = "ORIGINAL"
        sweep = node("GeometryNodeCurveToMesh", 20, 100)
        output = node("NodeGroupOutput", 260, 100)
        link = tree.links.new
        link(inputs.outputs["Profile"], info.inputs["Object"])
        link(inputs.outputs["Geometry"], sweep.inputs["Curve"])
        link(info.outputs["Geometry"], sweep.inputs["Profile Curve"])
        link(inputs.outputs["Fill Caps"], sweep.inputs["Fill Caps"])
        # Older versions use path radius implicitly. Newer versions expose Scale.
        scale = sweep.inputs.get("Scale")
        if scale is not None:
            radius = node("GeometryNodeInputRadius", -240, -240)
            link(radius.outputs["Radius"], scale)
        link(sweep.outputs["Mesh"], output.inputs["Geometry"])
        modifier = path.modifiers.new("Editable Sweep", "NODES")
        modifier.node_group = tree
        path.update_tag()
        return path, section
    except Exception:
        bpy.data.batch_remove(ids=created)
        raise
