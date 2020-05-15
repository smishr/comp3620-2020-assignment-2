"""Wumpus World.

COMP3620/6320 Artificial Intelligence
The Australian National University
Authors: Miquel Ramirez, Alasdair Tran
Date: 2016, 2019, 2020

Student Details
---------------
Student Name: Zheyuan Zhang
Student Number: u6870923
Date: 2020.5.1-2020.5.15
"""
import argparse
import os
import sys


def process_command_line_arguments() -> argparse.Namespace:
    """Parse the command line arguments and return an object with attributes
    containing the parsed arguments or their default values.
    """
    import json

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", dest="input", metavar="INPUT",
                        type=str, help="Input file with the Wumpus World parameters and observations (MANDATORY)")
    parser.add_argument("-a", "--action", dest="action", metavar="ACTION",
                        type=str, choices=["north", "south", "east", "west"],
                        help="Action to be tested for safety (MANDATORY)")
    parser.add_argument("-o", "--output", dest="output", metavar="OUTPUT", default='wumpus_outputs',
                        help="Output folder (default: %(default)s)")

    args = parser.parse_args()
    if args.action is None:
        raise SystemExit("Error: No action was specified.")

    if args.input is None:
        raise SystemExit("Error: No input file was specified.")

    if not os.path.exists(args.input):
        raise SystemExit(
            "Error: Input file '{}' does not exist".format(args.input))

    try:
        with open(args.input) as instream:
            args.domain_and_observations = json.load(instream)
    except IOError:
        raise SystemExit("Error: could not open file {}".format(args.input))

    return args


def main():
    # Processes the arguments passed through the command line
    args = process_command_line_arguments()

    # The name of the action to test
    action = args.action

    # The path of the directory that will contain the generated CSP files
    output_path = args.output

    # The description of the Wumpus World features and sequence of observations
    # resulting from the agent actions.
    dao = args.domain_and_observations
    n_rows = dao["rows"]
    n_columns = dao["columns"]
    n_wumpuses = dao["wumpuses"]
    n_pits = dao["pits"]
    observations = dao["observations"]

    # YOUR CODE HERE
    observed_loc = []
    for obs in observations:
        observed_loc.append(obs['location'])

    # move according to action
    current_loc = [observations[-1]['location'][0], observations[-1]['location'][1]]
    if action == 'north':
        moves = [[current_loc[0], current_loc[1] + 1]]
    elif action == 'south':
        moves = [[current_loc[0], current_loc[1] - 1]]
    elif action == 'east':
        moves = [[current_loc[0] + 1, current_loc[1]]]
    else:
        moves = [[current_loc[0] - 1, current_loc[1]]]

    # Create variables map
    variables = {'a': moves}
    wumpus_variable = {}
    pit_variable = {}

    # Create possible wumpuses location
    count = 0
    for obs in observations:
        if 'Stench' in obs['percepts']:
            new_w = 'w' + str(count)
            wumpus_variable[new_w] = []
            new_loc = [[obs['location'][0], obs['location'][1] + 1], [obs['location'][0], obs['location'][1] - 1],
                       [obs['location'][0] + 1, obs['location'][1]], [obs['location'][0] - 1, obs['location'][1]]]
            for loc in new_loc:
                if loc[0] < 1 or loc[0] > n_columns or loc[1] < 1 or loc[1] > n_rows:
                    continue
                elif loc in observed_loc:
                    continue
                else:
                    if loc not in wumpus_variable[new_w]:
                        wumpus_variable[new_w].append(loc)
            count += 1

    # Create possible pits location
    count = 0
    for obs in observations:
        if 'Breeze' in obs['percepts']:
            new_p = 'p' + str(count)
            pit_variable[new_p] = []
            new_loc = [[obs['location'][0], obs['location'][1] + 1], [obs['location'][0], obs['location'][1] - 1],
                       [obs['location'][0] + 1, obs['location'][1]], [obs['location'][0] - 1, obs['location'][1]]]
            for loc in new_loc:
                if loc[0] < 1 or loc[0] > n_columns or loc[1] < 1 or loc[1] > n_rows:
                    continue
                elif loc in observed_loc:
                    continue
                else:
                    if loc not in pit_variable[new_p]:
                        pit_variable[new_p].append(loc)
            count += 1

    special_con_list = {}
    import itertools
    wumpus_special = False
    pit_special = False
    # create special constrain for wumpuses
    if len(wumpus_variable.keys()) > n_wumpuses:
        wumpus_special = True
        # get all the permutation
        possible_list = list(itertools.product(*wumpus_variable.values()))
        # print(possible_list)
        key_set = 'con '
        for key in wumpus_variable.keys():
            key_set += key + ' '
        temp_con = []
        if n_wumpuses == 1:
            # all the elements must be same
            for candidate in possible_list:
                if candidate[1:] == candidate[:-1]:
                    if key_set not in special_con_list.keys():
                        temp_con.append(candidate)
                        # print(special_con_list)
            special_con_list[key_set] = temp_con
        else:
            for p in possible_list:
                for val in p:
                    if p.count(val) == n_wumpuses and p not in temp_con:
                        temp_con.append(p)
                        # print(p)
            special_con_list[key_set] = temp_con
        # print(special_con_list)
    else:
        for key in wumpus_variable.keys():
            variables[key] = wumpus_variable[key]

    # create special constrain for pits
    if len(pit_variable.keys()) > n_pits:
        pit_special = True
        # get all the permutation
        possible_list = list(itertools.product(*pit_variable.values()))
        # print(possible_list)
        key_set = 'con '
        for key in pit_variable.keys():
            key_set += key + ' '
        temp_con = []
        if n_pits == 1:
            # all the elements must be same
            for candidate in possible_list:
                if candidate[1:] == candidate[:-1]:
                    if key_set not in special_con_list.keys():
                        temp_con.append(candidate)
                        # print(special_con_list)
            special_con_list[key_set] = temp_con
        else:
            for p in possible_list:
                for val in p:
                    if p.count(val) == n_pits and p not in temp_con:
                        temp_con.append(p)
                        # print(p)
            special_con_list[key_set] = temp_con
        # print(special_con_list)
    else:
        for key in pit_variable.keys():
            variables[key] = pit_variable[key]

    # print(variables)

    # Create normal constrain
    con_list = {}
    for key1 in variables.keys():
        for key2 in variables.keys():
            if key2 != key1 and ((key2, key1) not in con_list.keys() and (key1, key2) not in con_list.keys()):
                con_list[(key1, key2)] = ''
    # print(con_list)
    if wumpus_special:
        for w in wumpus_variable.keys():
            con_list[('a', w)] = ''
            for p in pit_variable.keys():
                con_list[(w, p)] = ''

    if pit_special:
        for p in pit_variable.keys():
            con_list[('a', p)] = ''
            for w in wumpus_variable.keys():
                con_list[(p, w)] = ''

    for key in wumpus_variable:
        variables[key] = wumpus_variable[key]
    for key in pit_variable:
        variables[key] = pit_variable[key]

    # print(con_list)
    for key in con_list.keys():
        for val1 in variables[key[0]]:
            for val2 in variables[key[1]]:
                if val1 != val2:
                    con_list[key] = con_list[key] + '<' + str(val1[0]) + ',' + str(val1[1]) + '>' + ' ' \
                                    + '<' + str(val2[0]) + ',' + str(val2[1]) + '>' + ' : '
    # print(con_list)

    try:
        scenario = (args.input.split('/')[1]).split('.')[0]
        target = 'b'
        new_out = output_path + '/' + scenario + '_' + action + '_' + target + '.csp'
        path = os.path.exists(output_path)
        if not path:
            os.makedirs(output_path)
        file = open(new_out, 'w')
        for var, values in variables.items():
            val_str = ''
            for val in values:
                val_str += '<' + str(val[0]) + ',' + str(val[1]) + '>' + ' '
            file.write('var ' + var + " : " + val_str.strip() + '\n')

        for con, values in con_list.items():
            if values:
                file.write('con ' + con[0] + ' ' + con[1] + ' : ' + values[:-3] + '\n')
        for con, values in special_con_list.items():
            if values:
                val_str = ''
                for v in values:
                    if len(v) == 2:
                        val_str += '<' + str(v[0][0]) + ',' + str(v[0][1]) + '>' + ' ' + '<' + str(v[1][0]) + ',' + str(
                            v[1][1]) + '> : '
                    else:
                        val_str += '<' + str(v[0][0]) + ',' + str(v[0][1]) + '>' + ' ' + '<' + str(v[1][0]) + ',' + str(
                            v[1][1]) + '>' + ' ' + '<' + str(v[2][0]) + ',' + str(v[2][1]) + '> : '
            file.write(con + ': ' + val_str[:-3] + '\n')

        file.close()
        # from reference_n_to_bin import convert
        # convert(new_out, new_out)

    except IOError:
        print("failed")


    # constrains for a.csp
    delete_list = []
    shadow_con_list = con_list
    for key in con_list.keys():
        if 'a' in key:
            delete_list.append(key)
    for key in delete_list:
        con_list.pop(key)
    possible_list = list(itertools.product(*variables.values()))
    key_set = ''
    temp_con = []
    for key in variables.keys():
        key_set += key + ' '
    for k in possible_list:
        count = 0
        for val in k:
            if val == k[0]:
                count += 1
        if count > 1:
            temp_con.append(k)
    special_con_list[key_set] = temp_con

    try:
        scenario = (args.input.split('/')[1]).split('.')[0]
        target = 'a'
        new_out = output_path + '/' + scenario + '_' + action + '_' + target + '.csp'
        path = os.path.exists(output_path)
        if not path:
            os.makedirs(output_path)
        file = open(new_out, 'w')
        for var, values in variables.items():
            val_str = ''
            for val in values:
                val_str += '<' + str(val[0]) + ',' + str(val[1]) + '>' + ' '
            file.write('var ' + var + " : " + val_str.strip() + '\n')

        for con, values in con_list.items():
            if values:
                file.write('con ' + con[0] + ' ' + con[1] + ' : ' + values[:-3] + '\n')

        for con, values in special_con_list.items():
            if values:
                val_str = ''
                for v in values:
                    for x in v:
                        val_str += '<' + str(x[0]) + ',' + str(x[1]) + '>' + ' '
                    val_str += ' : '
                file.write(con + ': ' + val_str[:-3] + '\n')

        file.close()
        from reference_n_to_bin import convert
        convert(new_out, new_out)

    except IOError:
        print("failed")


if __name__ == '__main__':
    main()

