Math exam generator
====================

A Python module that can automatically generate mathematics worksheets/exams, with 
solution keys, using Sympy and LaTeX. Meant for instructors, tutors, and student
study groups, etc.

Based on a python3 reimplementation of the repository [https://github.com/thearn/examgen](https://github.com/thearn/examgen).

Since the parent project have been inactive for several years, this project will
eventually turn into a standalone one. Contributors are welcome!

# Requirements
- Python 3.6+
- Sympy
- pylatex
- jsonschema
- LaTeX

# Quickstart Example

```Python
from examgen.worksheet import Worksheet
from examgen.lib.algebra import QuadraticEq

ws = Worksheet(fname="example_worksheet", title="Example worksheet 1")

quad = QuadraticEq(var="x")
quad.add_integer_radicals(n=2)
quad.add_real_radicals(n=2)
quad.shuffle()

ws.add_section(prob_generator=quad)

# generate the exam and solutions pdf
ws.write()
```
Running this code will generate algebra1.pdf and 
sols_algebra1.pdf. The LaTeX `.tex`, `.log` and
`.aux` files will automatically be deleted after successful compilation. If you would rather
save the `.tex` files for further modifications, pass the `savetex` flag when
making your exam:

```Python
myexam = Worksheet(
    fname="example_worksheet",
    title="Example worksheet 1",
    savetex=True
)
```

The prob_generator argument takes a problem generating object. The classes for
problem generation can be found in `examgen.lib.algebra`, and `examgen.lib.calc1`.


# Extending for new problem types

New type of problems extending the functionality of this module should be
implemented as classes in `examgen.lib`.This part is currently under heavy development, and may change in the future. Current
version attempts to reimplement the features of  repository
[https://github.com/thearn/examgen](https://github.com/thearn/examgen),
while setting up for future changes. Contributions are welcome, contact me for
details.

If you need problems in your project that are not provided by the module,
you can implement your own problem classes.

Problem generating classes have to inherit `examgen.lib.base_classes.MathProb`, and implement
an `add_problem` method. This method have to append a problem and a solution as
LaTeX-compatible strings to attributes `problems` and `solutions` respectively, which
are defined in the base class.
So for example, you can define a custom generating class something like this:

```python
from examgen.lib.base_classes import MathProb

class MyProblem(MathProb):
    def __init__(self, my_argument: int = 2):
        super().__init__()
        self.my_argument = my_argument 
    
    def add_problem(self, n:int):
        """this function implements the problem my_argument+2 = something"""
        for i in range(n):
            var = self.get_variable()
            solution = self.my_argument + 2
            self.problems.append(f"$${var} = {self.my_argument}+2$$")
            self.solutions.append(f"{var}={solution}")
```

The base class MathProb has method `get_variable`, which returns a string containing
a single letter. This can be set in the constructor of MathProb by setting optional
argument `var` to either a string, or a list of strings. If `var` is set to a string to a string,
`get_variable()` will return that string. If set to a list of strings, `get_variable()`
will a string randomly selected from the list.

If `var` is not set, as in the example above, `get_variable()` will return a letter
randomly selected from `examgen.lib.constants.alpha`, which contains most ascii lowercase
and uppercase letters, omitting "l", "i", "I", "o", "O", as these would be confusing in
a math problem, being too similar to 0 or 1.

an example of a custom problem with custom variables:

```python
from examgen.lib.base_classes import MathProb
from examgen.worksheet import Worksheet

class MyProblem(MathProb):
    title = "adding 2 to something"
    instructions = "solve the following exercises"
    def __init__(
            self,
            var="x",
            my_argument: int = 2
    ):
        super().__init__(var=var)
        self.my_argument = my_argument 
        
    def add_problem(self, n:int):
        """this function implements the problem my_argument+2 = something"""
        for i in range(n):
            var = self.get_variable()
            solution = self.my_argument + 2
            self.problems.append(f"$${var} = {self.my_argument}+2$$")
            self.solutions.append(f"{var}={solution}")


# this will use the default variable "x"
prob1 = MyProblem()
prob1.add_problem(n=1)

# this will use the set variable "a"
prob2 = MyProblem(var="a")
prob2.add_problem(n=1)

# this will use a random selection from the provided list:
prob3 = MyProblem(var="abc")
prob3.add_problem(n=1)
# this will use a random selection from the builtin list:
prob4 = MyProblem(var=None)
prob4.add_problem(n=1)

myexam = Worksheet(fname="myexam", title="Adding 2 to different numbers")

myexam.add_section(prob_generator=prob1)
myexam.add_section(prob_generator=prob2)
myexam.add_section(prob_generator=prob1)
myexam.add_section(prob_generator=prob1)

myexam.write()
```
# Goals

Over time, I plan on implementing the following things:
- built-in support for more problem types
- graph generation via matplotlib
- saving/loading problems to file
- a library of static problems
