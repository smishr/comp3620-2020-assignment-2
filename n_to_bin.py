"""N-ary to binary constraint compiler.

COMP3620/6320 Artificial Intelligence
The Australian National University
Authors: Miquel Ramirez, Alasdair Tran
Date: 2016, 2019

Student Details
---------------
Student Name: Zheyuan Zhang
Student Number: u6870923
Date: 2020.5.10
"""
import argparse
import os
import sys
from typing import Dict, List, Set, Tuple


def process_command_line_arguments() -> argparse.Namespace:
    """Parse the command line arguments and return an object with attributes
    containing the parsed arguments or their default values.

    Returns
    -------
    args : an argparse.Namespace object
        This object will have two attributes:
            - input: a string with the path of the input file specified via
            the command line.
            - output: a string with the path of the file where the binarised
            CSP is to be found.

    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", dest="input", metavar="INPUT",
                        type=str, help="Input file with an n-ary CSP (MANDATORY)")
    parser.add_argument("-o", "--output", dest="output", metavar="OUTPUT",
                        default='binarised.csp',
                        help="File to write the binarised CSP (default: %(default)s)")

    args = parser.parse_args()
    if args.input is None:
        raise SystemExit("Error: No input file was specified.")

    if not os.path.exists(args.input):
        raise SystemExit(
            "Error: Input file '{}' does not exist".format(args.input))

    return args


def main():
    args = process_command_line_arguments()
    input_path = args.input
    output_path = args.output
    variables, constraints = parse_nary_file(input_path)

    # *** YOUR CODE HERE ***
    # print(constraints)
    new_variables = {}

    count = 0

    var_name_map = {}
    # create new variable name map
    for con_info in constraints:
        var_combine = ''
        for var in con_info[0]:
            var_combine += var
        var_name_map[var_combine] = 'var' + str(count)
        new_variables[var_combine] = con_info[1:]
        count += 1

    # create new values for new variables
    for name in new_variables.keys():
        new_list = []
        for values in new_variables[name][0]:
            new_val = ''
            for value in values:
                new_val += value
            new_list.append(new_val)
        new_variables[name] = new_list

    # find new constrain pairs
    con_list = {}
    for key1 in new_variables.keys():
        for key2 in new_variables.keys():
            if key2 != key1 and ((key2, key1) not in con_list.keys() and (key1, key2) not in con_list.keys()):
                con_list[(key1, key2)] = ''

    # find new constrain values' location
    c_location = {}
    for key1, key2 in con_list.keys():
        loc = ''
        for c1 in key1:
            for c2 in key2:
                if c1 == c2:
                    loc += (str(key1.find(c1)) + str(key2.find(c2)) + ' ')
        c_location[(key1, key2)] = loc

    # find values of new constrain pairs
    for key in con_list.keys():
        for val1 in new_variables[key[0]]:
            for val2 in new_variables[key[1]]:
                conflict = False
                for con in c_location[key].split():
                    if val1[int(con[0])] != val2[int(con[1])]:
                        conflict = True
                        break
                if conflict is False:
                    con_list[key] = con_list[key] + val1 + ' ' + val2 + ' : '

    try:
        file = open(output_path, 'w')
        for var, values in new_variables.items():
            val_str = ''
            for val in values:
                val_str += val + ' '
            file.write('var '+var_name_map[var]+" : " + val_str.strip()+'\n')

        for con, values in con_list.items():
            file.write('con '+var_name_map[con[0]]+' '+var_name_map[con[1]]+' : '+values[:-3]+'\n')
    except IOError:
        print("failed")
    finally:
        file.close()


# -----------------------------------------------------------------------------
# You might like to use the helper functions below. Feel free to modify these
# functions to suit your needs.
# -----------------------------------------------------------------------------


def parse_nary_file(file_name: str):
    """Parse an n-ary CSP file.

    Parameters
    ----------
    file_name : str
        The path to the n-ary CSP file.

    Returns
    -------
    variables : Dict[str, Set[str]]
        A dictionary mapping variable names to their domains. Each domain is
        represented by a set of values.

    constraints : List[Tuple[Tuple[str, ...], List[Tuple[str, ...]]]]
        A list of constraints. Each constraint is a tuple with two elements:
            1) The first element is the tuple of the variables involved in the
               constraint, e.g. ('x', 'y', 'z').

            2) The second element is the list of values those variables are
               allowed to take, e.g. [('0', '0', '0'), ('0', '1', '1')].

    """
    variables: Dict[str, Set[str]] = {}
    constraints: List[Tuple[Tuple[str, ...], List[Tuple[str, ...]]]] = []

    with open(file_name, "r") as file:
        for line in file:
            if line.startswith('var'):
                var_names, domain = line[3:].split(':')
                domain_set = set(domain.split())
                for v in var_names.split():
                    variables[v] = domain_set

            elif line.startswith('con'):
                content = line[3:].split(':')
                vs = tuple(content[0].split())
                values = [tuple(v.split()) for v in content[1:]]
                constraints.append((vs, values))

    return variables, constraints


if __name__ == '__main__':
    main()
