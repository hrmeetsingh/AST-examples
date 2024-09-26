import ast
import astor
import sys
from typing import Dict, Set

class SpyFunctionTransformer(ast.NodeTransformer):
    def __init__(self):
        self.spy_count = 0

    def visit(self, node: ast.AST):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
            return self.generic_visit(node)

        spy_call = ast.Expr(
            value=ast.Call(
                func=ast.Name(id='__spy__', ctx=ast.Load()),
                args=[ast.Constant(value=self.spy_count)],
                keywords=[]
            )
        )
        self.spy_count += 1

        if isinstance(node, ast.stmt):
            return [spy_call, node]
        elif isinstance(node, ast.expr):
            return ast.Call(
                func=ast.Lambda(
                    args=ast.arguments(args=[], vararg=None, kwarg=None, defaults=[]),
                    body=node
                ),
                args=[],
                keywords=[]
            )
        return node

def add_spy_functions(code: str) -> str:
    tree = ast.parse(code)
    transformer = SpyFunctionTransformer()
    modified_tree = transformer.visit(tree)
    return astor.to_source(modified_tree)

spy_hits: Dict[int, int] = {}

def __spy__(spy_id: int):
    spy_hits[spy_id] = spy_hits.get(spy_id, 0) + 1

def analyze_spy_hits(original_code: str, spy_hits: Dict[int, int]):
    original_lines = original_code.split('\n')
    instrumented_lines = add_spy_functions(original_code).split('\n')
    
    spy_to_line: Dict[int, int] = {}
    for i, line in enumerate(instrumented_lines):
        if line.strip().startswith('__spy__('):
            spy_id = int(line.split('(')[1].split(')')[0])
            spy_to_line[spy_id] = i

    print("\nExecution analysis:")
    print("-------------------")
    print("Line | Hit  | Code")
    print("-------------------")
    for i, line in enumerate(original_lines):
        hit_count = sum(spy_hits.get(spy_id, 0) for spy_id, line_num in spy_to_line.items() if line_num == i)
        if hit_count > 0:
            print(f"{i+1:4d} | {hit_count:4d} | {line}")
        else:
            print(f"{i+1:4d} |      | {line}")

# Example usage
if __name__ == "__main__":
    original_code = """
def greet(name):
    if name.startswith('Dr.'):
        print(f"Hello, Doctor {name[3:]}!")
    else:
        print(f"Hello, {name}!")

greet("Dr. Smith")
greet("Alice")
    """

    instrumented_code = add_spy_functions(original_code)
    
    print("Original code:")
    print(original_code)
    print("\nInstrumented code:")
    print(instrumented_code)
    
    exec(instrumented_code)
    
    # print("\nExecution analysis:")
    analyze_spy_hits(original_code, spy_hits)