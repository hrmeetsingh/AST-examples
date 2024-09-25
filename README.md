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

### Use case of Abstract Syntax Tree - Instrumentation (python example)

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
