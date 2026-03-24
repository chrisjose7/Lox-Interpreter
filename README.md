# Lox Interpreter (Python)

This project is a Python implementation of the Lox programming language,
based on the book *Crafting Interpreters* by Robert Nystrom.

The interpreter is built using a tree-walk architecture, including a scanner,
parser, and runtime environment.

## Features
- Expression evaluation with correct operator precedence
- Variables with block scoping
- Control flow (if statements and while loops)
- Functions with parameters and return values
- Recursion and closures

## Running the Interpreter

Run a file:

```
python lox.py yourfile.lox
```


Or start interactive mode:

```
python lox.py
```

## Example

```
fun add(a, b) {
  return a + b;
}

print add(2, 3); // 5
```

## Implementation Details

- Recursive descent parser
- Abstract syntax tree (AST) representation
- Environment chaining for scope resolution
- Function calls with closure support

## Acknowledgements

Based on *Crafting Interpreters* by Robert Nystrom.  
ChatGPT was used to help translate and understand parts of the implementation.
