import ast
import astor
from typing import Any

class TimingInstrumentationTransformer(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        start_time = ast.parse("import time as __time__\n__start_time__ = __time__.time()").body
        end_time = ast.parse("__end_time__ = __time__.time()").body
        print_time = ast.parse("print(f'Function {0} took {1:.6f} seconds'.format(__name__, __end_time__ - __start_time__))").body
        node.body = start_time + node.body + end_time + print_time
        return node

def instrument_code(stringified_code):
    ast_tree = ast.parse(stringified_code)

    transformer = TimingInstrumentationTransformer()
    instrumented_tree = transformer.visit(ast_tree)

    instrumented_code = astor.to_source(instrumented_tree)
    return instrumented_code


def ast_to_tree(node: Any, level: int = 0, last: bool = True, prefix: str = "") -> str:
    tree = ""
    
    # Add the current node to the tree
    if level > 0:
        tree += prefix
        tree += "└── " if last else "├── "
    tree += type(node).__name__

    # Add attributes of the node
    attrs = []
    for attr in ["id", "name", "arg", "value"]:
        if hasattr(node, attr):
            value = getattr(node, attr)
            attrs.append(f"{attr}={repr(value)}")
    if attrs:
        tree += f" ({', '.join(attrs)})"
    tree += "\n"

    # Recursively process child nodes
    children = list(ast.iter_child_nodes(node))
    for i, child in enumerate(children):
        child_last = (i == len(children) - 1)
        child_prefix = prefix + ("    " if last else "│   ")
        tree += ast_to_tree(child, level + 1, child_last, child_prefix)

    return tree

def visualize_ast(code: str) -> str:
    tree = ast.parse(code)
    return ast_to_tree(tree)

if __name__ == "__main__":
    original_code = """
def greet(name):
    print(f"Hello, {name}!")

def calculate_sum(a, b):
    return a + b

greet("World")
result = calculate_sum(5, 3)
print(f"Sum: {result}")
"""

    instrumented_code = instrument_code(original_code)

    print("Original code AST tree:")
    print(visualize_ast(original_code))

    print("Instrumented code:")
    print(instrumented_code)

    print("\nExecuting instrumented code:")
    exec(instrumented_code)

    