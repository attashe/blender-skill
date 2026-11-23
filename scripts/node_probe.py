"""Read-only, bounded inspection of one existing node tree or upstream branch.

Stored sockets and links are structural evidence, not evaluated shader/field values.
No creation, frame changes, rendering, saving or recursive group traversal.
"""
import bpy


def _bound(value, high, name):
    if not isinstance(value, int) or not 1 <= value <= high:
        raise ValueError(f'{name} must be an integer from 1 to {high}')
    return value


def _items(values, limit):
    return dict(items=values[:limit], total=len(values), truncated=len(values) > limit)


def resolve_tree(spec):
    """material:NAME, world:NAME or group:NAME; exact names, no fallback creation."""
    kind, sep, name = spec.partition(':')
    if not sep or not name or kind not in ('material', 'world', 'group'):
        raise ValueError('Tree selector must be material:NAME, world:NAME or group:NAME')
    collection = {'material': bpy.data.materials, 'world': bpy.data.worlds,
                  'group': bpy.data.node_groups}[kind]
    owner = collection.get(name)
    if owner is None:
        raise KeyError(f'{kind} {name!r} does not exist')
    tree = owner if kind == 'group' else owner.node_tree
    if tree is None:
        raise ValueError(f'{spec!r} has no node tree')
    return tree


def _header(node):
    result = dict(name=node.name, label=node.label, type=node.bl_idname, mute=node.mute)
    for key in ('operation', 'data_type', 'blend_type', 'is_active_output'):
        if key in node.bl_rna.properties:
            result[key] = getattr(node, key)
    if 'node_tree' in node.bl_rna.properties and node.node_tree is not None:
        result['group_boundary'] = dict(name=node.node_tree.name,
                                       next_tree='group:' + node.node_tree.name)
    return result


def describe_tree(tree, limit=12):
    limit = _bound(limit, 64, 'limit')
    nodes = list(tree.nodes)
    return dict(name=tree.name, type=tree.bl_idname, links=len(tree.links),
                nodes=dict(items=[_header(n) for n in nodes[:limit]], total=len(nodes),
                           truncated=len(nodes) > limit))


def resolve_socket(node, direction, selector):
    """Unique exact name, #index, or id:identifier; ambiguous labels raise."""
    if direction not in ('INPUT', 'OUTPUT'):
        raise ValueError('direction must be INPUT or OUTPUT')
    sockets = node.inputs if direction == 'INPUT' else node.outputs
    if selector.startswith('#'):
        index = int(selector[1:])
        if not 0 <= index < len(sockets):
            raise IndexError(f'{node.name} {direction} index {index} outside 0..{len(sockets)-1}')
        return sockets[index]
    by_id = selector.startswith('id:')
    requested = selector[3:] if by_id else selector
    matches = [s for s in sockets if (s.identifier if by_id else s.name) == requested]
    if len(matches) != 1:
        choices = ', '.join(f'#{i} {s.name!r} (id:{s.identifier})'
                            for i, s in enumerate(sockets) if i < 12)
        if len(sockets) > 12:
            choices += f'; {len(sockets) - 12} more: inspect this node with a larger limit'
        raise ValueError(f'{node.name} {direction} {selector!r}: {len(matches)} matches; '
                         f'available selectors: {choices}. '
                         'Select the intended identifier or #index; no substitute was chosen')
    return matches[0]


def _value(value):
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, bpy.types.ID):
        return dict(id=value.name, type=value.bl_rna.identifier)
    if hasattr(value, '__len__') and hasattr(value, '__iter__') and len(value) <= 16:
        return list(value)
    return dict(type=type(value).__name__, omitted=True)


def _endpoint(socket):
    return dict(node=socket.node.name, socket=socket.name, identifier=socket.identifier)


def _links(tree):
    """Index once: socket.links scans the full tree on each access in Blender."""
    incoming, outgoing = {}, {}
    for link in tree.links:
        incoming.setdefault(link.to_socket.as_pointer(), []).append(link)
        outgoing.setdefault(link.from_socket.as_pointer(), []).append(link)
    return incoming, outgoing


def _socket(socket, index, maps, limit):
    result = dict(index=index, name=socket.name, identifier=socket.identifier,
                  type=socket.bl_idname, direction='OUTPUT' if socket.is_output else 'INPUT')
    for key in ('enabled', 'hide', 'is_unavailable', 'is_inactive', 'is_linked', 'is_multi_input'):
        if key in socket.bl_rna.properties:
            result[key] = getattr(socket, key)
    if 'default_value' in socket.bl_rna.properties:
        result['stored_default'] = _value(socket.default_value)
        result['value_scope'] = ('Linked input: default is not its evaluated value'
                                 if not socket.is_output and socket.is_linked
                                 else 'Stored value only; animation, fields or graph may override its effect')
    else:
        result['value_scope'] = 'This socket type has no default_value'
    links = maps[1 if socket.is_output else 0].get(socket.as_pointer(), [])
    values = [dict(source=_endpoint(l.from_socket), destination=_endpoint(l.to_socket),
                   valid=l.is_valid, muted=l.is_muted) for l in links[:limit]]
    result['links'] = dict(items=values, total=len(links), truncated=len(links) > limit)
    return result


def describe_node(node, limit=12, _maps=None):
    limit = _bound(limit, 64, 'limit')
    maps = _maps if _maps is not None else _links(node.id_data)
    result = _header(node)
    for key in ('inputs', 'outputs'):
        sockets = getattr(node, key)
        result[key] = dict(items=[_socket(s, i, maps, limit) for i, s in enumerate(sockets)
                                 if i < limit], total=len(sockets), truncated=len(sockets) > limit)
    result['mute_bypass'] = _items([dict(source=_endpoint(l.from_socket),
                                       destination=_endpoint(l.to_socket))
                                  for l in node.internal_links], limit)
    return result


def trace_input(node, selector, depth=2, max_nodes=8, limit=12):
    """Trace physical incoming links, including muted/invalid ones with flags.

    Does not evaluate branches or cross groups. Inspect group internals separately;
    Group Input output defaults do not stand in for a caller's instance values.
    """
    depth = _bound(depth, 8, 'depth')
    max_nodes = _bound(max_nodes, 64, 'max_nodes')
    limit = _bound(limit, 64, 'limit')
    socket = resolve_socket(node, 'INPUT', selector)
    maps = _links(node.id_data)
    index = next(i for i, s in enumerate(node.inputs) if s == socket)
    queue = [(l.from_node, 1) for l in maps[0].get(socket.as_pointer(), [])]
    seen, nodes, stopped = {node.as_pointer()}, [], set()
    while queue:
        source, level = queue.pop(0)
        pointer = source.as_pointer()
        if pointer in seen:
            continue
        seen.add(pointer)
        if level > depth:
            stopped.add('depth')
            continue
        if len(nodes) >= max_nodes:
            stopped.add('max_nodes')
            break
        item = describe_node(source, limit, maps)
        item['distance'] = level
        nodes.append(item)
        if 'group_boundary' in item or source.bl_idname == 'NodeGroupInput':
            stopped.add('group_boundary')
            continue
        for inp in source.inputs:
            queue.extend((l.from_node, level + 1) for l in maps[0].get(inp.as_pointer(), []))
    return dict(target_node=_header(node), target=_socket(socket, index, maps, limit),
                upstream=nodes, stops=sorted(stopped), depth=depth, max_nodes=max_nodes,
                scope='Stored structure only. Change one control and evaluate/render to prove its effect. '
                      'Output reachability, group internals and shader/field evaluation are not established.')
