"""Heuristics for variable selection and value ordering.

COMP3620/6320 Artificial Intelligence
The Australian National University
Authors: Nathan Robinson, Miquel Ramirez, Alasdair Tran
Date:    2014, 2015, 2016, 2019

Student Details
---------------
Student Name: Zheyuan Zhang
Student Number: u6870923
Date: 2020.5.2 - 2020.5.5

This is where you need to write your heuristics for variable selection and
value ordering.
"""
from typing import Callable, Dict, List, Optional

from csp import CSP

Assignment = Dict[str, str]


# -----------------------------------------------------------------------------
# Variable Selection Heuristics
# -----------------------------------------------------------------------------


def next_variable_lex(assignment: Assignment, gamma: CSP) -> Optional[str]:
    """Select the next variable by lexicographic order.

    Select the next variable from the remaining variables according to
    lexicographic order. We have implemented this one for you.

    Parameters
    ----------
    assignment : Dict[str, str]
        A Python dictionary that maps variable names to values.
    gamma : CSP
        An instance of the class CSP, representing the constraint network
        to which we are looking for a solution.

    Returns
    -------
    variable : Optional[str]
        The name of the next variable chosen by this heuristic. If there are no
        remaining unassigned variables, we return None.

    """
    # gamma.variables is a list of variable names (as strings). See line 43 in
    # csp.py. We consider them in the order they are added in.
    for var in gamma.variables:
        if var not in assignment:
            return var
    return None


def next_variable_md(assignment: Assignment, gamma: CSP) -> Optional[str]:
    """Implement the most constraining variable (MD) heuristic.

    Choose the variable that that is involved in as many constraints as
    possible. See Lecture 11 for the precise definition. Break ties by
    lexicographic order.

    Parameters
    ----------
    assignment : Dict[str, str]
        A Python dictionary that maps variable names to values.
    gamma : CSP
        An instance of the class CSP, representing the constraint network
        to which we are looking for a solution.

    Returns
    -------
    variable : Optional[str]
        The name of the next variable chosen by this heuristic. If there are no
        remaining unassigned variables, we return None.

    """
    # *** YOUR CODE HERE ***
    max_num = 0
    answer = None
    for key in gamma.variables:
        if key not in assignment:
            count = 0
            for var in gamma.neighbours[key]:
                if var not in assignment:
                    count += 1
            if count > max_num:
                max_num = count
                answer = key
            elif count == max_num and count == 0:
                answer = key

    return answer


def next_variable_mrv(assignment: Assignment, gamma: CSP) -> Optional[str]:
    """Implement the most constrained variable heuristic (MRV).

    Choose the variable with the smallest consistent domain. See Lecture 11 for
    the precise definition. Break ties by lexicographic order.

    Parameters
    ----------
    assignment : Dict[str, str]
        A Python dictionary that maps variable names to values.
    gamma : CSP
        An instance of the class CSP, representing the constraint network
        to which we are looking for a solution.

    Returns
    -------
    variable : Optional[str]
        The name of the next variable chosen by this heuristic. If there are no
        remaining unassigned variables, we return None.

    """
    # *** YOUR CODE HERE ***
    answer = None
    count = 1000
    for var in gamma.variables:
        if var not in assignment:
            var_count = len(gamma.current_domains[var])
            for v in gamma.current_domains[var]:
                if gamma.count_conflicts(var, v):
                    var_count -= 1
            if var_count < count:
                count = var_count
                answer = var

    return answer


def next_variable_md_mrv(assignment: Assignment, gamma: CSP) -> Optional[str]:
    """Implement MD heuristic, breaking ties with MRV.

    Choose the variable that is involved in as many constraints as possible. If
    there is a tie, choose the variable with the smallest consistent domain.
    See Lecture 11 for the precise definition.

    Parameters
    ----------
    assignment : Dict[str, str]
        A Python dictionary that maps variable names to values.
    gamma : CSP
        An instance of the class CSP, representing the constraint network
        to which we are looking for a solution.

    Returns
    -------
    variable : Optional[str]
        The name of the next variable chosen by this heuristic. If there are no
        remaining unassigned variables, we return None.

    """
    # *** YOUR CODE HERE ***
    max_num = 0
    answer_md = []
    for key in gamma.variables:
        if key not in assignment:
            count = 0
            for var in gamma.neighbours[key]:
                if var not in assignment:
                    count += 1
            if count > max_num:
                max_num = count
                answer_md.clear()
                answer_md.append(key)
            elif count == max_num:
                answer_md.append(key)

    answer = None
    count = 1000
    for var in answer_md:
        if var not in assignment:
            var_count = len(gamma.current_domains[var])
            for v in gamma.current_domains[var]:
                if gamma.count_conflicts(var, v):
                    var_count -= 1
            if var_count < count:
                count = var_count
                answer = var

    return answer


def next_variable_mrv_md(assignment: Assignment, gamma: CSP) -> Optional[str]:
    """Implement MRV heuristic, breaking ties with MD.

    Choose the variable with the smallest consistent domain. If there is a tie,
    choose the variable that is involved in as many constraints as
    possible. See Lecture 11 for the precise definition.

    Parameters
    ----------
    assignment : Dict[str, str]
        A Python dictionary that maps variable names to values.
    gamma : CSP
        An instance of the class CSP, representing the constraint network
        to which we are looking for a solution.

    Returns
    -------
    variable : Optional[str]
        The name of the variable chosen by this heuristic. If there are no
        remaining unassigned variables, we return None.

    """
    # *** YOUR CODE HERE ***
    answer_mrv = []
    count = 1000
    for var in gamma.variables:
        if var not in assignment:
            var_count = len(gamma.current_domains[var])
            for v in gamma.current_domains[var]:
                if gamma.count_conflicts(var, v):
                    var_count -= 1
            if var_count < count:
                count = var_count
                answer_mrv.clear()
                answer_mrv.append(var)
            elif var_count == count:
                answer_mrv.append(var)

    max_num = 0
    answer = None
    for key in answer_mrv:
        if key not in assignment:
            count = 0
            for var in gamma.neighbours[key]:
                if var not in assignment:
                    count += 1
            if count > max_num:
                max_num = count
                answer = key
            elif count == max_num and count == 0:
                answer = key

    return answer


# -----------------------------------------------------------------------------
# Value Ordering Heuristics
# -----------------------------------------------------------------------------


def value_ordering_lex(var: str, assignment: Assignment, gamma: CSP) -> List[str]:
    """Order the values based on lexicographic order.

    In this heuristic, variable values are ordered in lexicographic order. We
    have implemented this heuristic for you. We make use of the attribute
    `gamma.current_domains` to be useful. This is a dictionary that maps a
    variable name (a string) to a set of values (a set of strings) in that
    variable's current domain.

    Parameters
    ----------
    var : str
        The name of the variable which we want to assign a value.
    assignment : Dict[str, str]
        A Python dictionary that maps variable names to values.
    gamma : CSP
        An instance of the class CSP, representing the constraint network
        to which we are looking for a solution.

    Returns
    -------
    values : List[str]
        A list the values (represented a strings) in the current domain of the
        variable, sorted according to this heuristic.

    """
    # We need to explicitly convert a set to a list.
    return list(gamma.current_domains[var])


def value_ordering_lcvf(var: str, assignment: Assignment, gamma: CSP) -> List[str]:
    """Order the values based on the Least Constraining Value heuristic.

    This heuristic returns values in order of how constraining they are. It
    prefers the value that rules out the fewest choices for the neighbouring
    variables in the constraint graph. In other words,  it prefers values which
    remove the fewest elements from the current domains of their neighbouring
    variables.

    See Lecture 11 for the precise definition. You might find the attribute
    `gamma.current_domains` to be useful. This is a dictionary that maps a
    variable name (a string) to a set of values (a set of strings) in that
    variable's current domain.

    Parameters
    ----------
    var : str
        The name of the variable which we want to assign a value.
    assignment : Dict[str, str]
        A Python dictionary that maps variable names to values.
    gamma : CSP
        An instance of the class CSP, representing the constraint network
        to which we are looking for a solution.

    Returns
    -------
    values : List[str]
        All the values in  the current domain of the variable, sorted according
        to this heuristic.

    """
    # *** YOUR CODE HERE ***
    answer_list = []
    answer = []

    if var not in assignment:
        for v in gamma.current_domains[var]:
            conflicts = 0
            all_conflicts = gamma.conflicts[(var, v)]
            for key in all_conflicts.keys():
                if key in gamma.neighbours[var] and key not in assignment:
                    if v in all_conflicts[key] and v in gamma.current_domains[key]:
                        conflicts += 1
            answer_list.append((conflicts, v))

    for key in sorted(answer_list, key=(lambda x: x[0])):
        answer.append(key[1])
    return answer


# -------------------------------------------------------------------------------
# Functions used by the system to select from the above heuristics for the search
# You do not need to look any further.
# -------------------------------------------------------------------------------

def get_variable_selection_function(variable_heuristic: str) -> Callable:
    """Return the appropriate variable selection function."""
    if variable_heuristic == "lex":
        return next_variable_lex
    if variable_heuristic == "md":
        return next_variable_md
    if variable_heuristic == "mrv":
        return next_variable_mrv
    if variable_heuristic == "md-mrv":
        return next_variable_md_mrv
    if variable_heuristic == "mrv-md":
        return next_variable_mrv_md

    raise ValueError(f"Error: the variable selection heuristic "
                     f"'{variable_heuristic}' is not supported")


def get_value_ordering_function(value_heuristic: str) -> Callable:
    """Return the appropriate value ordering function."""
    if value_heuristic == "lex":
        return value_ordering_lex
    if value_heuristic == "lcvf":
        return value_ordering_lcvf

    raise ValueError(f"Error: the value selection heuristic "
                     f"'{value_heuristic}' is not supported")
