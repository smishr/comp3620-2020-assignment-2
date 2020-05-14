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

    # Create possible wumpuses location
    wumpuse_loc = []
    for obs in observations:
        if 'Stench' in obs['percepts']:
            new_loc = [[obs['location'][0], obs['location'][1] + 1], [obs['location'][0], obs['location'][1] - 1],
                       [obs['location'][0] + 1, obs['location'][1]], [obs['location'][0] - 1, obs['location'][1]]]
            for loc in new_loc:
                if loc[0] < 1 or loc[0] > n_columns or loc[1] < 1 or loc[1] > n_rows:
                    continue
                elif loc in observed_loc:
                    continue
                else:
                    if loc not in wumpuse_loc:
                        wumpuse_loc.append(loc)
    # print(wumpuse_loc)

    # Create possible pits location
    pit_loc = []
    for obs in observations:
        if 'Breeze' in obs['percepts']:
            new_loc = [[obs['location'][0], obs['location'][1] + 1], [obs['location'][0], obs['location'][1] - 1],
                       [obs['location'][0] + 1, obs['location'][1]], [obs['location'][0] - 1, obs['location'][1]]]
            for loc in new_loc:
                if loc[0] < 1 or loc[0] > n_columns or loc[1] < 1 or loc[1] > n_rows:
                    continue
                elif loc in observed_loc:
                    continue
                else:
                    if loc not in pit_loc:
                        pit_loc.append(loc)
    # print(pit_loc)

    # Create possible moves
    current_loc = [observations[-1]['location'][0], observations[-1]['location'][1]]
    moves = []
    possible_moves = [[current_loc[0], current_loc[1] + 1], [current_loc[0], current_loc[1] - 1],
                     [current_loc[0] + 1, current_loc[1]], [current_loc[0] - 1, current_loc[1]]]
    for move in possible_moves:
        if move[0] < 1 or move[0] > n_columns or move[1] < 1 or move[1] > n_rows:
            continue
        elif move in observed_loc:
            continue
        else:
            if move not in moves:
                moves.append(move)
    # print(moves)

    # Create variables map
    variables = {'a': moves}
    for w in range(n_wumpuses):
        variables['w'+str(w)] = wumpuse_loc
    for p in range(n_pits):
        variables['p'+str(p)] = pit_loc
    # print(variables)

    # Create constrain map:

if __name__ == '__main__':
    main()
