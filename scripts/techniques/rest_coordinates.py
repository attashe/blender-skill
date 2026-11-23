"""Capture undeformed mesh-local coordinates. No file or scene reset side effects."""


def capture_rest_positions(mesh_object, name='rest_position'):
    """Call before deformation on an owned mesh. Refuse to overwrite existing data.

    Writes a POINT/FLOAT_VECTOR attribute on the source mesh. Shared mesh users share it.
    This is not a UV unwrap, dynamic-topology paint solution or world-space coordinate map.
    """
    if mesh_object.type != 'MESH':
        raise TypeError('Mesh object required')
    mesh = mesh_object.data
    if name in mesh.attributes:
        raise ValueError('Attribute exists; verify/reuse it instead of recapturing a deformed pose')
    attribute = mesh.attributes.new(name, 'FLOAT_VECTOR', 'POINT')
    for datum, vertex in zip(attribute.data, mesh.vertices):
        datum.vector = vertex.co
    return attribute


def connect_rest_coordinates(material, coordinate_input, name='rest_position'):
    """Replace the explicitly selected shader vector input with an Attribute output.

    The caller chooses the actual mapping input; this does not search/rewire a whole material.
    Attribute existence on each rendered mesh and evaluated shading remain caller checks.
    """
    if not material.use_nodes or coordinate_input.is_output or coordinate_input.type != 'VECTOR':
        raise ValueError('An input Vector socket in a node material is required')
    tree = material.node_tree
    if coordinate_input.id_data != tree:
        raise ValueError('Socket must belong to the supplied material')
    node = tree.nodes.new('ShaderNodeAttribute')
    node.attribute_name = name
    node.label = 'Coordinates captured before deformation'
    tree.links.new(node.outputs['Vector'], coordinate_input)
    return node
