"""Helper functions te facilitate sampling from an AST."""

import ast

def traverse_nodes(tree):
    """Return a generator that traverses all nodes of a tree."""
    queue = [tree]
    while queue:
        current_node = queue.pop(0)
        #children = list(ast.iter_child_nodes(current_node))
        children = current_node['child']
        queue.extend(children)
        yield current_node
