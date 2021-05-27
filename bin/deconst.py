#!/usr/bin/env python3
import os
import sys


def copy_file(file, destination):
    """Copy file to destination."""
    os.system(f'cp {file} {destination}')


def process_lines(lines, variables):
    """Returns lines to write. Only replaces values with constant variable names."""
    lines_to_change = []  # (line_index, new_line)
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
                if not line[var_index - 1].isalnum() and line[var_index:var_index + len(var[0])] == var[0] and not \
                        line[var_index + len(var[0])].isalnum():
                    line = line[:var_index] + var[1] + line[var_index + len(var[0]):]

        lines_to_change.append((k, line))

    for line in lines_to_change:
        lines[line[0]] = line[1]

    return lines


def read_file(file):
    """Return list of lines, constants. Only removes definitions of constant variables."""
    lines = []
    variables = []  # (name, value)
    with open(file) as f:
        lines = f.readlines()

    lines_to_pop = []  # line_index
    lines_to_change = []  # (line_index, new_line)
    lines_to_skip = []  # line_index

    for i, line in enumerate(lines):
        names = []
        values = []
        upper_name_indexes = []
        if i in lines_to_skip:
            continue
        for j, char in enumerate(line):
            if char == '#':  # comment line
                break
            elif j == len(line) - 1:  # last element
                break
            if char == '=' and line[j + 1] == '=':  # exists if condition (there mustn't definition)
                break
            elif char == '=':  # don't exists if condition (definitions can be found)
                names_before_equal = line[:j].split(',')  # names that there is potential to be variable names

                for k, name in enumerate(names_before_equal):
                    name = name.strip()
                    if name.isupper():
                        names.append(name)  # append name into names array if name has upper syntax
                        upper_name_indexes.append(k)


                values_after_equal = line[j + 1:-1]  # TODO: fix paranthesis problem

                # for k, value in enumerate(values_after_equal):
                    # value = value.strip()
                    # is_there_complex_value = value.startswith('"') or value.startswith("'") or \
                    #                          value.startswith('{') or value.startswith('[') or \
                    #                          value.startswith('(')
                    #
                    # if is_there_complex_value:
                    #     # NAME = {prop: 1, otherprop: "some string", anotherprop: {sample:'nested prop', prop: {name: "muzo"}}, othernested: {prop: "nested"}}
                    #     # parse this
                    #
                    #     opencurly = 0
                    #     openparantehesis = 0
                    #     opensquarebracket = 0
                    #     closecurly = 0
                    #     closeparanthesis = 0
                    #     closesquarebracket = 0
                    #     doublequotes = 0
                    #     singlequote = 0
                    #     z = k
                    #
                    #     if value.startswith('{'):
                    #         opencurly += 1
                    #     elif value.startswith('('):
                    #         openparantehesis += 1
                    #     elif value.startswith('['):
                    #         opensquarebracket += 1
                    #     elif value.startswith('"'):
                    #         doublequotes += 1
                    #     elif value.startswith("'"):
                    #         singlequote += 1
                    #
                    #     while (opencurly != closecurly or
                    #            openparantehesis != closeparanthesis or
                    #            opensquarebracket != closesquarebracket
                    #            or doublequotes % 2 == 1 or
                    #            singlequote % 2 == 1) and z != len(values_after_equal):
                    #         opencurly += values_after_equal[z].count('{')
                    #         openparantehesis += values_after_equal[z].count('(')
                    #         opensquarebracket += values_after_equal[z].count('[')
                    #         closecurly += values_after_equal[z].count('}')
                    #         closeparanthesis += values_after_equal[z].count(')')
                    #         closesquarebracket += values_after_equal[z].count(']')
                    #         doublequotes += values_after_equal[z].count('"')
                    #         singlequote += values_after_equal[z].count("'")
                    #
                    #         z += 1
                    #
                    #     if z == len(values_after_equal) - 1 and (opencurly != closecurly or
                    #                                              openparantehesis != closeparanthesis or
                    #                                              opensquarebracket != closesquarebracket
                    #                                              or doublequotes % 2 == 1 or
                    #                                              singlequote % 2 == 1):
                    #
                    #         pass  # TODO: add multiline variable
                    #     else:
                    #         for p, values_to_add in enumerate(values_after_equal[k:z]):
                    #             value += ','
                    #             value += values_to_add
                    #             values_after_equal.pop(k + p + 1)

                        # for t, value_after_value in enumerate(values_after_equal[k:]):
                        #
                        #     closing_value = value_after_value.endswith('"') or value_after_value.endswith("'") or \
                        #                     value_after_value.endswith('}') or value_after_value.endswith('}') or \
                        #                     value_after_value.endswith('}')
                        #
                        #     if closing_value:
                        #         for p in range(t):
                        #             value += ","
                        #             value += values_after_equal[k + p + 1]
                        #             values_after_equal.pop(k + p + 1)
                for k, value in enumerate(values_after_equal):
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

    for line in lines_to_change:
        lines[line[0]] = line[1]

    for i, line in enumerate(lines_to_pop):
        lines.pop(line - i)

    return lines, variables


def write_file(file, lines):
    with open(file, 'w') as f:
        f.writelines(lines)


def main(args):
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

        Please check directory deconstpy. If exists, remove or move it.''')
        return

    try:
        os.mkdir(os.path.join(os.path.curdir, 'deconstpyfiles'))
    except FileExistsError:
        print('Directory deconstpyfiles exists. Please remove or move it.')
        is_approve = input('Do you still approve copying file into deconstpyfiles? (y or anything): ')
        if not is_approve == 'y' and not is_approve == 'Y':
            print('Application closed.')
            exit()

    for arg in args[1:]:
        if arg.startswith('--'):
            continue  # TODO: add implementation for flags
        print(f'{arg} is copying...')
        deconstfile = os.path.join(os.path.curdir, 'deconstpyfiles', os.path.basename(arg))
        copy_file(arg, deconstfile)
        print(f'{arg} is reading...')
        lines, variables = read_file(deconstfile)
        print(f'{arg} is processing...')
        lines = process_lines(lines, variables)
        print(f'{arg} is writing...')
        write_file(deconstfile, lines)
        print(f'{arg} deconstanted.')


if __name__ == '__main__':
    argv = sys.argv
    main(argv)
