import ast
import astor

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
    print("Instrumented code:")
    print(instrumented_code)

    print("\nExecuting instrumented code:")
    exec(instrumented_code)