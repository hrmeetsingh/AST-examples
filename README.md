## AbstractSyntaxTree
Code examples for demonstrating parsing and creating [Abstract Syntax Tree (AST)](https://en.wikipedia.org/wiki/Abstract_syntax_tree) for a program

### Code example -
```
while b ≠ 0:
    if a > b:
        a := a - b
    else:
        b := b - a
return a
```

### Abstract Syntax Tree for the code above -

![Abstract syntax tree](/images/Abstract_syntax_tree.png)

### Tree representation for the AST

![Abstract syntax tree](/images/AST_Tree.png)

### Use case 
#### 1. Instrumentation (python example)

```python
def gcd(a, b):
    import time as __time__
    __start_time__ = __time__.time()
    if a == 0:
        return b
    if b == 0:
        return a
    return gcd(b, a % b)
    __end_time__ = __time__.time()
    print(f'Function {0} took {1:.6f} seconds'.format(__name__, 
        __end_time__ - __start_time__))
```

#### 2. Code Coverage calculation using code spies
Example file for python code with spies inserted in code to observe calls to calculate coverage - `ast-function-spies.py`

Explanation -
- The input function `greet` is called twice with different parameters
- Code is parsed into an AST tree
- Spy functions are inserted at code execution points
- Instrumented code is executed
- Spy functions are tracked for executions and a record is kept
- Count of code execution is printed

Sample output -
```
Execution analysis:
-------------------
Line | Hit  | Code
-------------------
   1 |      | 
   2 |    2 | def greet(name):
   3 |      |     if name.startswith('Dr.'):
   4 |      |         print(f"Hello, Doctor {name[3:]}!")
   5 |      |     else:
   6 |      |         print(f"Hello, {name}!")
   7 |      | 
   8 |      | greet("Dr. Smith")
   9 |    1 | greet("Alice")
  10 |      |     
```

### TODO: Add javascript sample for coverage code as well
