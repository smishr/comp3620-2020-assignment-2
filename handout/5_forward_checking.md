# Exercise 3: Forward Checking (20 Marks)

## The Task

We want you to implement the Forward Checking inference procedure described in
the lectures. The implementation needs to be invoked via the function

```python
def forward_checking(var: str, assignment: Assignment, gamma: CSP) -> Optional[Pruned]:
    """Implement the forward checking inference procedure.

    Parameters
    ----------
    var : str
        The name of the variable which has just been assigned.
    assignment : Dict[str, str]
        A Python dictionary of the current assignment. The dictionary maps
        variable names to values. The function cannot change anything in
        `assignment`.
    gamma : CSP
        An instance of the class CSP, representing the constraint network
        to which we are looking for a solution. The function cannot change
        anything in `gamma`.

    Returns
    -------
    pruned_list : Optional[Pruned]
        In the case that the algorithm detects a conflict, the assignment and
        CSP should remain unchanged and the function should return None.

        Otherwise, the algorithm should return a pruned_list, which is a list
        of (variable, value) pairs that will be pruned out of the domains of
        the variables in the problem. Think of this as the "edits" that are
        required to be done on the variable domains.

    """
```

This function will be called every time a variable `x` is assigned a value (you
can retrieve this value by accessing `assignment[x]`).

## Grading Guide

Your implementation should expand a similar number of nodes and take the same
amount of time (within an order of magnitude) to the benchmark below:

| Instance      | Time (s) | Nodes Expanded |
| ------------- | -------- | -------------- |
| sudoku_01.csp | 0.002    | 128            |
| sudoku_02.csp | 0.06     | 3262           |
| sudoku_03.csp | 0.04     | 2538           |
| sudoku_04.csp | 0.4      | 26,801         |
| sudoku_05.csp | 0.1      | 6,272          |
| sudoku_06.csp | 0.01     | 898            |
| sudoku_07.csp | 0.05     | 3,266          |
| sudoku_08.csp | 1        | 66,827         |
| sudoku_09.csp | 0.2      | 14,176         |
| sudoku_10.csp | 0.1      | 10,726         |

The above benchmarks were tested on a MacBook Pro 2019 (2.3 GHz Intel Core i9).
For example, to get the results for solving the first Sudoku problem:

```sh
python3 solver.py -v lex -l lex -i forward test_problems/sudoku_01.csp
```

## What To Submit

The file `inference.py` with the your implementation in the function
`forward_checking`.

## Hints

1. To implement Forward Checking you will have to keep track of the domains
   that are being changed by the inference procedure yourself. Remember that
   the `gamma` object **needs to remain unchanged**.

2. The caller expects your code to comply with the following
   **post-condition**: `forward_checking` never reduces any variable domain to
   an empty set.

3. You may reduce the domain of a variable to a size of 1 (a singleton). If
   this variable would cause a direct conflict, you should return `None`.
   However, only check for direct conflicts. Don't perform forward checking on
   these variables (i.e. don't prune neighbours of neighbours).

4. Note that you can read but are not allowed to change any attribute inside
   the CSP instance `gamma`. Thus you might need to copy some information from
   `gamma`. But only copy what you need. Unnecessary copying will significantly
   slow down your program.

## Index

1. [Getting Started](1_getting_started.md)
2. [CSP File Format](2_csp_syntax.md)
3. [Exercise 1: Variable Selection Heuristics (10
   Marks)](3_variable_selection_heuristics.md)
4. [Exercise 2: Value Selection Heuristics (5
   Marks)](4_value_selection_heuristics.md)
5. **Exercise 3: Forward Checking (20 Marks)**
6. [Exercise 4: AC-3 (35 Marks)](6_ac_3.md)
7. [Exercise 5: Compiling n-ary Constraints into Binary Constraints (10 Marks)](7_compilation.md)
8. [Exercise 6: Wumpus Where Are You? (20 Marks)](8_wumpus_world.md)
9. [Wumpus World Maps Layouts](8a_map_layouts.md)
