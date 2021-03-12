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
from examgen.lib.algebra import LinearEq

# make an exam with a filename and title
myexam = Worksheet("algebra1", "Algebra 101 worksheet 1", savetex=True)

# add some problem sections 
myexam.add_section(
    prob_generator=LinearEq(),
    n=20,
    title="Linear equations",
    instructions="Solve the following equations for the specified variable."
)

# generate the exam and solutions pdf
myexam.write()
```
Running this code will generate algebra1.pdf and 
sols_algebra1.pdf. The LaTeX `.tex`, `.log` and
`.aux` files will automatically be deleted after successful compilation. If you would rather
save the `.tex` files for further modifications, pass the `savetex` flag when
making your exam:

```Python
myexam = Worksheet("algebra1", "Algebra 101 exam 1", savetex=True)
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
a `make` method. This method have to return a tuple of two LaTeX-compatible strings.
The first string is the problem generated, the second is
the corresponding solution. 

So for example, you can define a custom generating class something like this:

```python
from examgen.lib.algebra.base_classes import MathProb

class MyProblem(MathProb):
    def __init__(self, my_argument: int = 2):
        super().__init__()
        self.my_argument = my_argument 
    
    def make(self):
        """this function implements the problem my_argument+2 = something"""
        var = self.get_variable()
        solution = self.my_argument + 2
        return f"$${var} = {self.my_argument}+2$$", f"{var}={solution}"
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
from examgen.lib.algebra.base_classes import MathProb

class MyProblem(MathProb):
    def __init__(
            self,
            var="x",
            my_argument: int = 2
    ):
        super().__init__(var=var)
        self.my_argument = my_argument 
        
    def make(self):
        """this function implements the problem my_argument+2 = something"""
        var = self.get_variable()
        solution = self.my_argument + 2
        return f"$${var} = {self.my_argument}+2$$", f"{var}={solution}"


# this will use the default variable "x"
prob1 = MyProblem()

# this will use the set variable "a"
prob2 = MyProblem(var="a")

# this will use a random selection from the provided list:
prob3 = MyProblem(var=["a", "b", "c"])

# this will use a random selection from the builtin list:
prob4 = MyProblem(var=None)

myexam = Worksheet("myexam", "Adding 2 to different numbers")

myexam.add_section(
    prob_generator=prob1,
    n=1,
    title="problem with variable x",
    instructions=""
)
myexam.add_section(
    prob_generator=prob2,
    n=1,
    title="problem with variable a",
    instructions=""
)
myexam.add_section(
    prob_generator=prob1,
    n=1,
    title="problem with variable a or b or c",
    instructions=""
)
myexam.add_section(
    prob_generator=prob1,
    n=1,
    title="problem with random variable",
    instructions=""
)

myexam.write()
```


`MyProblem(MathProb)`, that has a method
`(arg1, arg2=val)` with
required argument `arg1` and keyword argument `arg2`, you can add a section of
15 problems of this type to your exam by calling:

```Python
myexam..add_section(my_problem, 15, "Cool problems",
                 "Solve these problems", arg1_val, arg2=arg2_val)
```

# Goals

Over time, I plan on implementing the following things:
- built-in support for more problem types
- graph generation via matplotlib
- saving/loading problems to file
- a library of static problems
