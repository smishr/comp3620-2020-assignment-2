"""Inference functions used with backtracking search.

COMP3620/6320 Artificial Intelligence
The Australian National University
Authors: Nathan Robinson, Miquel Ramirez, Alasdair Tran
Date:    2014, 2015, 2016, 2019, 2020

Student Details
---------------
Student Name: Zheyuan Zhang
Student Number: u6870923
Date: 2020.5.5
"""

import collections
from typing import Callable, Dict, List, Optional, Tuple

from csp import CSP

Assignment = Dict[str, str]
Pruned = List[Tuple[str, str]]


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
    # *** YOUR CODE HERE ***
    answer = []
    all_conflicts = gamma.conflicts[(var, assignment[var])]
    for next_step in all_conflicts.keys():
        temp_domain = gamma.domains[next_step].copy()
        for val in all_conflicts[next_step]:
            if val in gamma.current_domains[next_step]:
                answer.append((next_step, val))
                temp_domain.remove(val)
                if len(temp_domain) < 1:
                    return None

    return answer


def arc_consistency(var: Optional[str], assignment: Assignment, gamma: CSP) -> Optional[Pruned]:
    """Implement the AC-3 inference procedure.

    Parameters
    ----------
    var : Optional[str]
        The name of the variable which has just been assigned. In the case that
        AC-3 is used for preprocessing, `var` will be `None`.
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
    # *** YOUR CODE HERE ***
    import copy

    answer = []
    arc_queue = collections.deque()
    domains = copy.deepcopy(gamma.current_domains)
    if var is None:
        for key in gamma.variables:
            for con_key in gamma.neighbours[key]:
                if key not in assignment and con_key not in assignment:
                    arc_queue.append((key, con_key))
    else:
        for binary_var in gamma.neighbours[var]:
            if binary_var not in assignment:
                arc_queue.append((binary_var, var))

    ac3(gamma, assignment, domains, arc_queue, answer)

    return answer


def ac3(gamma: CSP, assignment,  domains, arc_queue, answer):
    while arc_queue:
        var, binary_var = arc_queue.pop()
        change, temp_answer = reduce_arc(var, binary_var, gamma, [], domains)
        if change:
            if len(domains[var]) == 1:
                return None
            for key in temp_answer:
                if key not in answer:
                    answer.append(key)
            for new_var in gamma.neighbours[var]:
                if new_var != binary_var and new_var not in assignment:
                    arc_queue.append((new_var, var))

    return answer


def reduce_arc(var, binary_var, gamma: CSP, temp_answer, domains):
    change = None
    for val in list(domains[var]):
        change = True
        all_conflicts = gamma.conflicts[(var, val)]
        if binary_var in all_conflicts.keys():
            for b_val in domains[binary_var]:
                if b_val not in all_conflicts[binary_var]:
                    change = False
                    break
        if change:
            temp_answer.append((var, val))
            domains[var].remove(val)
    return change, temp_answer


# -------------------------------------------------------------------------------
# A function use to get the correct inference method for the search
# You do not need to touch this.
# -------------------------------------------------------------------------------

def get_inference_function(inference_type: str) -> Callable:
    """Return the function that does the specified inference."""
    if inference_type == "forward":
        return forward_checking
    if inference_type == "arc":
        return arc_consistency

    # If no inference is specified, we simply do nothing.
    def no_inference(var, assignment, csp):
        return []

    return no_inference
