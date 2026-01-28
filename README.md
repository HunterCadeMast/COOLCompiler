# COOL Compiler (Compiler Construction Course Project)

This repository contains a multi-part compiler developed for a **Compiler Construction** course.
The compiler targets the **COOL (Classroom Object-Oriented Language)** and is implemented incrementally across six programming assignments.
Each assignment corresponds with a part of the compiler (Lexical, Syntax, Semantic, Code Generation, and Optimization).

---

## ▶️ How to Run

This compiler is designed to be used with the **COOL driver** (`cool.exe`).
Each phase of the compiler corresponds to a specific compilation stage.

```bash
cool.exe --command program.cl
```

COOL Commands:
- --lex
- --parse
- --type
- --codegen

These should create a `.cl` file.

```bash
python compiler.py file.cl
```

Run the Python compiler code with the COOL file to run.

---

## 🔹 PA2 – Lexical Analysis (Lexer)

### Overview

The lexical analyzer converts COOL source code into a stream of tokens for parsing.
It was implemented using **PLY (Python Lex-Yacc)** and closely replicates the behavior of the **reference COOL lexer** provided in the course.

Primary reference:

- PLY Documentation: https://ply.readthedocs.io/en/latest/

### Implementation Details

- Token definitions for:
  - Keywords.
  - Identifiers.
  - Integers.
  - Strings.
  - Operators.
- Case-insensitive keywords (except `true` and `false`).
- Line number tracking.

### Error Handling

- Unterminated strings.
- EOF inside comments.
- Illegal characters.
- Integer overflow.

### Challenges

- Correct handling of nested block comments.
- String escape processing.
- Matching reference formatting precisely.

---

## 🔹 PA3 – Syntax Analysis (Parser)

### Overview

The parser transforms the token stream into an **Abstract Syntax Tree (AST)** and validates the syntactic structure of COOL programs.

### Implementation Details

- Written using **PLY Yacc**.
- Full support for:
  - Class declarations.
  - Methods and attributes.
  - Expressions.
  - Control flow (`if`, `while`, `case`).
  - Dispatch expressions.
- Correct operator precedence and associativity.

### AST Construction

- AST nodes created directly in grammar actions.
- Source line information preserved for error reporting.

### Challenges

- Shift/reduce conflicts.
- Nested `let` and `case` expressions.
- Graceful syntax error recovery.

---

## 🔹 PA4 – Semantic Analysis (Type-Checking)

### Overview

PA4 performs static semantic analysis to ensure programs obey COOL’s type system rules.
This phase annotates the AST with type information and rejects invalid programs.

### Semantic Checks

- Inheritance graph validation.
- Detection of inheritance cycles.
- Method override correctness.
- Attribute redefinition errors.
- Scope and symbol resolution.
- Expression type checking.
- `SELF_TYPE` propagation.
- Case branch uniqueness.

### Implementation Details

- Symbol tables for:
  - Classes.
  - Methods.
  - Attributes.
  - Local variables.
- Depth-first traversal of class hierarchy.
- All semantic errors collected before termination.

### Output

- Produces a `.cl-type` file.
- Typed AST passed to code generation.

---

## 🔹 PA5 – Code Generation

### Overview

PA5 translates the typed AST into executable **COOL assembly code**.

### Features

- Class map generation.
- Parent map generation.
- Dispatch table construction.
- Object constructors.
- Method prologue and epilogue generation.
- Stack frame layout.
- Dynamic and static dispatch.

### Implementation Details

- Stack-based calling convention.
- Temporary stack space calculated per method.
- AST used directly as the IR.

### Challenges

- Correct dynamic dispatch behavior.
- Stack offset correctness.
- Runtime debugging of frame layout errors.

---

## 🔹 PA6 – Optimization

### Overview

PA6 applies a variety of classical compiler optimizations to reduce runtime cost and instruction count.

---

### Constant Propagation

- Compile-time evaluation of constant expressions.
- Strength reduction (e.g., `x + 0 → x`).
- Safe folding only when variables are immutable.

This optimization provided the largest performance improvement.

---

### Dead Code Elimination (DCE)

#### Standalone DCE

- Implemented as a separate `dce.py`.
- Operates on three-address code (TAC).
- Uses backward liveness analysis.
- Iteratively removes unused assignments.
- Preserves side-effecting instructions.

Limitations:
- Only operates on `main`.
- Ignores `case` expressions.

#### In-Compiler DCE (Disabled)

- Attempted AST-based DCE.
- Disabled due to incorrect removal in dispatch-heavy code.

---

### Assignment Propagation (Disabled)

- Attempts to eliminate redundant variable assignments.
- Disabled due to insufficient liveness guarantees.

---

### Unboxing (Limited)

- Replaces boxed constants (`new Int`, etc.) where safe.
- Full unboxing avoided due to complexity.

---

### Peephole Optimization

- Removes redundant assembly instructions.
- Minimal impact due to already compact code generation.

---

## 🎓 Academic Context

This project demonstrates a complete COOL compiler pipeline, from lexical analysis through optimization.
This project emphasizes conceptual understanding and clarity of compiler construction, rather than production-level performance.

---

## 📫 Contact

**Hunter Mast**  
GitHub: https://github.com/huntercademast
Email: huntercademast@gmail.com