# Regular Languages
A library to explore regular languages, and their various representations

Inspired by a reading of "Introduction to the Theory of Computation" by Michael
Sipser and "Introduction to Automata Theory, Languages, and Computation" by
Hopcroft, et. al.

The library includes:
- Implementations of NFAs, DFAs, and regular expressions
- Functions to convert between NFA, DFAs, and regular expressions
- Function to perform operations that are closed for regular languages, like
union, intersection, complement, and more
- A regular language abstraction that can be instantiated using any regular
language representation, have any operation performed on it for which regular
languages are closed, and be converted to any regular language representation
  - This effectively allows for performing operations on representations for
  which that operation may not be easy to perform. For example, taking the
  complement of a regular expression

## In Progress
- DFA minimization
- Supporting more advanced regex operations
- The regular language abstraction
- Most of the regular language operations
- FA state renaming

## Usage
- Run with Python 3.10. Because that includes some really nice typing
  capabilities, and pattern matching
- Create a virtual environment

```bash
python3 -m venv venv
```

- Activate the virtual environment

```bash
source ./venv/bin/activate
```

- Install the package in editable mode

```bash
pip3 install -e .
```

- Import the package

```python
from regular_languages import ...
```
