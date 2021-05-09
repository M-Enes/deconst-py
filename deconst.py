#! /usr/bin/python3

import os
import sys

def copy_file(file, destination):
    os.system(f'cp {file} {destination}')


def process_lines(lines, variables):
    lines_to_change = []  # (line_index, new_line)
    print(lines)
    for k, line in enumerate(lines):
        is_comment_line = False
        for i, ch in enumerate(line):
            if ch == '#' and line[:i].count(' ') == i:
                is_comment_line = True
        if is_comment_line:
            break

        for var in variables:
            if not line.count(var[0]):
                break
            var_index = line.index(var[0])
            for i in range(var_index):  # TODO: fix here
                if not line[var_index - 1].isalnum() and line[var_index:var_index + len(var[0])] == var[0] and not line[
                        var_index + len(var[0])].isalnum():
                    line = line[:var_index] + var[1] + line[var_index + len(var[0]):]

        lines_to_change.append((k, line))

    for line in lines_to_change:
        lines[line[0]] = line[1]

    return lines


def read_file(file):
    """returns list of lines, constants"""
    lines = []
    variables = []  # (name, value)
    with open(file) as f:
        lines = f.readlines()

    lines_to_pop = []
    lines_to_change = []  # (line_index, new_line)

    for i, line in enumerate(lines):
        names = []
        values = []
        upper_name_indexes = []
        for j, char in enumerate(line):
            if char == '#':
                break
            elif j == len(line) - 1:
                break
            if char == '=' and line[j + 1] == '=':
                break
            elif char == '=' and line[j + 1] != '=':
                names_before_equal = line[:j].split(',')

                for k, name in enumerate(names_before_equal):
                    name = name.strip()
                    if name.isupper():
                        names.append(name)
                        upper_name_indexes.append(k)

                all_openings_closed = line[j:].count('{') == line[j:].count('}') and \
                    line[j:].count('[') == line[j:].count(']') and \
                    line[j:].count('(') == line[j:].count(')') and \
                    line[j:].count('"') % 2 == 0 and line[j:].count("'") % 2 == 0

                if all_openings_closed:
                    values_after_equal = line[j + 1:-1].split(',')

                    for k, value in enumerate(values_after_equal):
                        value = value.strip()
                        if upper_name_indexes.count(k):
                            values.append(value)
                            variables.append((names[len(values) - 1], value))
                    if len(names_before_equal) != len(upper_name_indexes):

                        for t, name in enumerate(names):
                            for p in range(line.index(name)):
                                if line[p:line.index(name)].count(' ') == line.index(name) - p and line[p - 1] == ',':
                                    line = line[:p - 1] + line[p:]
                                    break
                            line = line[:line.index(name)] + line[line.index(name) + len(name):]

                        for t, value in enumerate(values):
                            for p in range(line.index(value)):
                                if line[line.index(value):line.index(value) + p].count(' ') == line.index(value) - p \
                                        and line[p - 1] == ',':
                                    line = line[:p - 1] + line[p:]
                                    break
                            line = line[:line.index(value)] + line[line.index(value) + len(value):]
                            lines_to_change.append((i, line))
                    else:
                        lines_to_pop.append(i)
                else:
                    is_multiline_value = True  # TODO: add multiline variables

    for line in lines_to_change:
        lines[line[0]] = line[1]

    for i, line in enumerate(lines_to_pop):
        lines.pop(line - i)

    return lines, variables


def write_file(file, lines):
    print(lines)
    with open(file, 'w') as f:
        f.writelines(lines)


def main(args):
    if not os.path.isfile('/bin/deconstpy'):
        isCommandApply = input('Would you like to set deconstpy command for use in all folders (type y for apply)')
        if isCommandApply == 'y':
            copy_file("deconst.py", "/bin/deconstpy")
            print('deconstpy command set successfully.')
            exit()

    if len(args) < 2:
        print('File argument not passed. If you want to get info for usage, type --help argument.')
        return
    if args[1] == '--help':
        print('''deconstpy: deconstpy [--help] [arg ...]
        Deconstants arguments.

        Arguments must be a Python files and have .py extension.

        Options:
          --help         display help message

        Constant syntax must like that:
        EXAMPLE_CONSTANTS1 = 'sample string'

        Please check directory deconstpy. If exits, remove or move it.''')
        return

    try:
        os.mkdir('deconstpy')
    except FileExistsError:
        print('Directory deconstpy exists. Please remove or move it.')

    for arg in args[1:]:
        if arg.startswith('--'):
            continue #TODO: add implementation for flags
        print(f'{arg} is copied')
        copy_file(arg, os.path.join(os.curdir, 'deconstpyfiles'))
        lines, variables = read_file(os.path.join(os.curdir, 'deconstpyfiles', arg))
        lines = process_lines(lines, variables)
        write_file(os.path.join(os.curdir, 'deconstpyfiles', arg), lines)


if __name__ == '__main__':
    argv = sys.argv
    main(argv)
