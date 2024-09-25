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

class Colors:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"

def colorize(text: str, color: str) -> str:
    return f"{color}{text}{Colors.RESET}"

def get_node_color(node: Any) -> str:
    if isinstance(node, ast.FunctionDef):
        return Colors.BLUE
    elif isinstance(node, ast.Call):
        return Colors.RED
    elif isinstance(node, ast.Name):
        return Colors.YELLOW
    elif isinstance(node, (ast.JoinedStr, ast.arguments, ast.Expr, ast.Assert, ast.Return)):
        return Colors.MAGENTA
    elif isinstance(node, ast.Call):
        return Colors.CYAN
    else:
        return Colors.RESET


def ast_to_tree(node: Any, level: int = 0, last: bool = True, prefix: str = "") -> str:
    tree = ""
    
    # Add the current node to the tree
    if level > 0:
        tree += prefix
        tree += colorize("└── ", Colors.BLUE) if last else colorize("├── ",Colors.BLUE)

    node_color = get_node_color(node)
    tree += colorize(type(node).__name__, node_color)

    # Add attributes of the node
    attrs = []
    for attr in ["id", "name", "arg", "value"]:
        if hasattr(node, attr):
            value = getattr(node, attr)
            attrs.append(f"{attr}={colorize(repr(value), Colors.CYAN)}")
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

    