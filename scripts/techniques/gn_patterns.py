"""Small editable row/grid/ring groups and a GN-to-shader attribute bridge.

No scene edits on import. create_pattern creates one node-group datablock, not an
object/modifier/material. Source object != consuming host; source-local +X is the
forward axis for RADIAL/TANGENT rings. Tested with Blender 5.2.1, see cards.
"""
import bpy


def _input(node, name):
    matches = [s for s in node.inputs if s.name == name and s.enabled and not s.is_unavailable]
    if len(matches) != 1:
        raise ValueError(f'{node.bl_idname}: expected one active {name!r}, got {len(matches)}')
    return matches[0]


def _wire(tree, value, socket):
    if isinstance(value, bpy.types.NodeSocket):
        tree.links.new(value, socket)
    else:
        socket.default_value = value


def _math(tree, operation, a, b, x, y):
    node = tree.nodes.new('ShaderNodeMath')
    node.operation = operation
    node.location = (x, y)
    _wire(tree, a, node.inputs[0])
    _wire(tree, b, node.inputs[1])
    return node.outputs[0]


def create_pattern(source, layout, *, name=None, max_count=256, max_axis=32, orientation='FIXED'):
    """Return a new GN group: Source plus layout controls -> unrealized Instances.

    ROW: Count 0..max_count, Step vector, starts at origin.
    GRID: Count X/Y 2..max_axis, Spacing X/Y >0, centered XY.
    RING: Count 3..max_count, Radius >0, centered XY, +X forward.
    Counts are graph-clamped before generation; spacing/radius >=1e-6.
    FIXED keeps source axes; RADIAL/TANGENT are ring-only, +Z up.
    """
    if source is None or source.type != 'MESH':
        raise ValueError('Provide a mesh source object, distinct from the future host')
    if layout not in {'ROW', 'GRID', 'RING'}:
        raise ValueError('layout must be ROW, GRID or RING')
    if orientation not in {'FIXED', 'RADIAL', 'TANGENT'} or (layout != 'RING' and orientation != 'FIXED'):
        raise ValueError('RADIAL/TANGENT require a RING with local +X forward')
    if not isinstance(max_count, int) or max_count < 3 or not isinstance(max_axis, int) or max_axis < 2:
        raise ValueError('max_count >=3 and max_axis >=2 must be integers')
    g = bpy.data.node_groups.new(name or f'{layout.title()} Instances', 'GeometryNodeTree')

    def interface(label, typ, default, minimum=None, maximum=None):
        s = g.interface.new_socket(name=label, in_out='INPUT', socket_type=typ)
        s.default_value = default
        if minimum is not None:
            s.min_value = minimum
        if maximum is not None:
            s.max_value = maximum
        return s

    interface('Source', 'NodeSocketObject', source)
    if layout == 'GRID':
        for axis in 'XY':
            interface(f'Count {axis}', 'NodeSocketInt', 3, 2, max_axis)
            interface(f'Spacing {axis}', 'NodeSocketFloat', .6, 1e-6)
    else:
        interface('Count', 'NodeSocketInt', min(8, max_count), 0 if layout == 'ROW' else 3, max_count)
        if layout == 'ROW':
            interface('Step', 'NodeSocketVector', (.6, 0, 0))
        else:
            interface('Radius', 'NodeSocketFloat', 1., 1e-6)
    g.interface.new_socket(name='Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')
    inp = g.nodes.new('NodeGroupInput'); inp.location = (-1000, 0)
    out = g.nodes.new('NodeGroupOutput'); out.location = (650, 0)

    def bounded(label, minimum, maximum, y):
        low = _math(g, 'MAXIMUM', inp.outputs[label], minimum, -800, y)
        return _math(g, 'MINIMUM', low, maximum, -600, y)

    if layout == 'GRID':
        primitive = g.nodes.new('GeometryNodeMeshGrid')
        for i, axis in enumerate('XY'):
            count = bounded(f'Count {axis}', 2, max_axis, -i*300)
            span = _math(g, 'SUBTRACT', count, 1, -400, -i*300)
            spacing = _math(g, 'MAXIMUM', inp.outputs[f'Spacing {axis}'], 1e-6, -600, -i*300-150)
            size = _math(g, 'MULTIPLY', span, spacing, -200, -i*300)
            g.links.new(count, primitive.inputs[f'Vertices {axis}'])
            g.links.new(size, primitive.inputs[f'Size {axis}'])
    else:
        count = bounded('Count', 0 if layout == 'ROW' else 3, max_count, 0)
        primitive = g.nodes.new('GeometryNodeMeshLine' if layout == 'ROW' else 'GeometryNodeMeshCircle')
        if layout == 'ROW':
            primitive.mode = 'OFFSET'
            g.links.new(count, _input(primitive, 'Count'))
            g.links.new(inp.outputs['Step'], _input(primitive, 'Offset'))
        else:
            primitive.fill_type = 'NONE'
            g.links.new(count, primitive.inputs['Vertices'])
            radius = _math(g, 'MAXIMUM', inp.outputs['Radius'], 1e-6, -600, -200)
            g.links.new(radius, primitive.inputs['Radius'])
    primitive.location = (0, 0)
    points = primitive.outputs['Mesh']
    if layout == 'ROW':
        # Mesh Line clamps its own count; explicitly represent the empty case.
        switch = g.nodes.new('GeometryNodeSwitch'); switch.input_type = 'GEOMETRY'
        switch.location = (180, 0)
        positive = _math(g, 'GREATER_THAN', count, 0, -200, -250)
        g.links.new(positive, _input(switch, 'Switch'))
        g.links.new(points, _input(switch, 'True'))
        points = switch.outputs['Output']
    info = g.nodes.new('GeometryNodeObjectInfo'); info.location = (0, 300)
    info.transform_space = 'ORIGINAL'
    info.inputs['As Instance'].default_value = True
    g.links.new(inp.outputs['Source'], info.inputs['Object'])
    inst = g.nodes.new('GeometryNodeInstanceOnPoints'); inst.location = (420, 0)
    g.links.new(points, inst.inputs['Points'])
    g.links.new(info.outputs['Geometry'], inst.inputs['Instance'])
    if layout == 'RING' and orientation != 'FIXED':
        pos = g.nodes.new('GeometryNodeInputPosition'); pos.location = (0, -350)
        vector = pos.outputs['Position']
        if orientation == 'TANGENT':
            cross = g.nodes.new('ShaderNodeVectorMath'); cross.operation = 'CROSS_PRODUCT'
            cross.location = (170, -350); cross.inputs[0].default_value = (0, 0, 1)
            g.links.new(vector, cross.inputs[1]); vector = cross.outputs['Vector']
        align = g.nodes.new('FunctionNodeAlignRotationToVector'); align.location = (230, -150)
        align.axis = 'X'; align.pivot_axis = 'Z'
        g.links.new(vector, align.inputs['Vector'])
        g.links.new(align.outputs['Rotation'], inst.inputs['Rotation'])
    g.links.new(inst.outputs['Instances'], out.inputs['Geometry'])
    return g


def set_inputs(modifier, **values):
    """Set existing named group inputs by identifier, then tag the owner for evaluation."""
    if modifier.type != 'NODES' or modifier.node_group is None:
        raise ValueError('Expected a Geometry Nodes modifier with an assigned group')
    sockets = {s.name: s for s in modifier.node_group.interface.items_tree
               if s.item_type == 'SOCKET' and s.in_out == 'INPUT'}
    unknown = values.keys() - sockets.keys()
    if unknown:
        raise ValueError(f'Unknown group input(s): {sorted(unknown)}')
    if values.get('Source') == modifier.id_data:
        raise ValueError('Source must differ from consuming host')
    for name in values:
        ident = sockets[name].identifier
        if bpy.app.version >= (5, 2, 0):
            entry = getattr(modifier.properties.inputs, ident)
            if getattr(entry, 'type', 'VALUE') != 'VALUE':
                raise ValueError(f'{name}: attribute mode is active; this helper sets constants only')
        elif modifier.get(ident + '_use_attribute', False):
            raise ValueError(f'{name}: attribute mode is active; this helper sets constants only')
    for name, value in values.items():
        ident = sockets[name].identifier
        if bpy.app.version >= (5, 2, 0):
            getattr(modifier.properties.inputs, ident).value = value
        else:
            modifier[ident] = value
    modifier.id_data.update_tag()


def store_instance_value(tree, geometry, name, value):
    """Return geometry with a FLOAT named value stored on INSTANCE domain.

    Pass a number or field output socket. Replaces a same-named attribute on this
    branch; the caller owns that name and must route the returned geometry onward.
    """
    if not name:
        raise ValueError('Use an explicit, task-owned attribute name')
    node = tree.nodes.new('GeometryNodeStoreNamedAttribute')
    node.domain = 'INSTANCE'; node.data_type = 'FLOAT'
    node.inputs['Name'].default_value = name
    tree.links.new(geometry, node.inputs['Geometry'])
    _wire(tree, value, _input(node, 'Value'))
    return node.outputs['Geometry']


def shader_instance_value(tree, name):
    """Return the scalar shader field for the matching unrealized instance attribute."""
    if not name:
        raise ValueError('Use the same explicit name as the geometry writer')
    node = tree.nodes.new('ShaderNodeAttribute')
    node.attribute_type = 'INSTANCER'; node.attribute_name = name
    return node.outputs['Fac']
