# Lox Interpreter (Python)

A Python implementation of the Lox programming language from Robert Nystrom's
*Crafting Interpreters*. This is the **tree-walk interpreter** (jlox): source is
scanned into tokens, parsed into an AST by a recursive-descent parser, and
executed by walking the tree with an environment-based scope model.

A separate bytecode-VM implementation (the clox half) lives in
[cpsc323-project2-lox-vm](https://github.com/chrisjose7/cpsc323-project2-lox-vm).

## Features

- Expression evaluation with correct operator precedence and associativity
- Variables and assignment with lexical block scoping
- Control flow: `if`/`else`, `while`, and `for`
- Functions with parameters, return values, and recursion
- Closures (functions capture their defining environment)

## Running

Run a file:
```bash
python lox.py yourfile.lox
```

Start the REPL (interactive mode):
```bash
python lox.py
```

## Examples

Recursion:
```lox
fun fib(n) {
  if (n < 2) return n;
  return fib(n - 1) + fib(n - 2);
}
print fib(10); // 55
```

Closures (each counter keeps its own captured state):
```lox
fun makeCounter() {
  var count = 0;
  fun increment() {
    count = count + 1;
    return count;
  }
  return increment;
}

var counter = makeCounter();
print counter(); // 1
print counter(); // 2
```

## How it works

| Stage        | Responsibility                                              | File(s) |
|--------------|-------------------------------------------------------------|---------|
| Scanner      | Source text → tokens                                        | `scanner.py` |
| Parser       | Tokens → AST (recursive descent)                            | `parser.py`, `expr.py`, `stmt.py` |
| Interpreter  | Tree-walk evaluation                                        | `interpreter.py` |
| Environment  | Variable storage and scope chaining                        | `environment.py` |
| Functions    | Callable objects, closures, `return` via control-flow exception | `lox_function.py`, `lox_callable.py`, `return_exception.py` |

Scope is resolved by chaining `Environment` objects: each block/function creates
a child environment that falls back to its enclosing scope, which is what makes
closures work. `return` is implemented by raising a dedicated exception that
unwinds the call stack back to the function boundary.

## Known limitations

- No static resolution pass, so some closure edge cases from later chapters of
  the book are not handled.
- No classes/inheritance (implemented through the functions chapter, not the OOP chapters).
- Tree-walk execution is intentionally simple over fast; the bytecode VM repo is the performance-oriented counterpart.

## Acknowledgements

Implementation based on *Crafting Interpreters* by Robert Nystrom. I used
ChatGPT as a learning aid to understand parts of the book's design while
implementing it in Python.
