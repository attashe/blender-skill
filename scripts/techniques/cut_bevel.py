"""A minimal editable Boolean → Bevel example extracted from the drilled motor flange."""
import math


def cut_and_bevel(host, cutter, radius, *, segments=3, angle=math.radians(30)):
    """Append two modifiers; return them. Inputs are owned meshes with suitable transforms.

    No geometry construction, transform application, material/normal edits or file IO.
    Radius is in the host's local units. Call once on the intended working copy;
    the function does not infer which existing stack stages it should replace.
    """
    if host == cutter or host.type != 'MESH' or cutter.type != 'MESH':
        raise ValueError('Two distinct mesh objects required')
    if not math.isfinite(radius) or radius <= 0 or segments < 1:
        raise ValueError('Positive local radius and segment count required')
    boolean = host.modifiers.new('Technique: through cut', 'BOOLEAN')
    boolean.operation = 'DIFFERENCE'
    boolean.solver = 'EXACT'
    boolean.object = cutter
    bevel = host.modifiers.new('Technique: bounded edge radius', 'BEVEL')
    bevel.width = radius
    bevel.segments = segments
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = angle
    bevel.use_clamp_overlap = True
    return boolean, bevel
