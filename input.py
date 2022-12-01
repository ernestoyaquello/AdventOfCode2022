def read_lines(problem_number, line_separator = '\n', strip = True):
    with open("inputs/" + str(problem_number) + ".txt") as input:
        return list(map(str.strip, input.read().split(line_separator))) if strip else input.read().split(line_separator)

def read_numbers(problem_number, line_separator = '\n'):
    return list(map(int, read_lines(problem_number = problem_number, line_separator = line_separator)))

def read_lists(problem_number, list_separator = '\n', item_separator = ' '):
    return [list.split(item_separator) for list in read_lines(problem_number, line_separator = list_separator)]