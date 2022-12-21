import input
import re

PROBLEM_NUMBER = 21

def execute(is_part_two):
    expressions = read_expressions()
    expressions['root']['operation'] = '=' if is_part_two else expressions['root']['operation']
    return get_value(expressions, 'root') if not is_part_two else find_human_value(expressions, 'root')

def get_value(expressions, expression_label):
    value = None

    expression = expressions[expression_label]
    if expression['value'] != None:
        value = expression['value']
    else:
        left_value = get_value(expressions, expression['left'])
        right_value = get_value(expressions, expression['right'])
        if expression['operation'] == '+': value = left_value + right_value
        elif expression['operation'] == '-': value = left_value - right_value
        elif expression['operation'] == '*': value = left_value * right_value
        elif expression['operation'] == '/': value = left_value / right_value

    expression['value'] = int(value)
    return int(value)

def find_human_value(expressions, expression_label, expected_result = 0):
    if expression_label == 'humn':
        return expected_result
    else:
        expression = expressions[expression_label]
        left_needs_human_value = check_if_human_value_is_needed(expressions, expression['left'])
        available_value = get_value(expressions, expression['right']) if left_needs_human_value else get_value(expressions, expression['left'])

        if expression['operation'] == '+': next_expected_result = (expected_result - available_value) if left_needs_human_value else (expected_result - available_value)
        elif expression['operation'] == '-': next_expected_result = (expected_result + available_value) if left_needs_human_value else (available_value - expected_result)
        elif expression['operation'] == '*': next_expected_result = (expected_result / available_value) if left_needs_human_value else (expected_result / available_value)
        elif expression['operation'] == '/': next_expected_result = (expected_result * available_value) if left_needs_human_value else (available_value / expected_result)
        elif expression['operation'] == '=': next_expected_result = available_value

        return find_human_value(expressions, expression['left' if left_needs_human_value else 'right'], expected_result = int(next_expected_result))

def check_if_human_value_is_needed(expressions, expression_label):
    expression = expressions[expression_label]
    needs_human_value = expression_label == 'humn' or ('needs_human_value' in expression.keys() and expression['needs_human_value'])

    if not needs_human_value and expression['value'] == None:
        left_result = check_if_human_value_is_needed(expressions, expression['left'])
        right_result = check_if_human_value_is_needed(expressions, expression['right'])
        needs_human_value = left_result or right_result
        expression['needs_human_value'] = needs_human_value

    return needs_human_value

def read_expressions():
    expressions = {}

    input_pattern = re.compile(r"(\w+): (?:(?:(\w+) ([\+\-\/\*]) (\w+))|(\d+))")
    for match in [match for line in input.read_lines(problem_number = PROBLEM_NUMBER) for match in input_pattern.finditer(line)]:
        if match.group(5) == None:
            expressions[match.group(1)] = {'left': match.group(2), 'right': match.group(4), 'operation': match.group(3), 'value': None}
        else:
            expressions[match.group(1)] = {'left': None, 'right': None, 'operation': None, 'value': int(match.group(5))}

    return expressions

print("Part 1: " + str(execute(is_part_two = False)))
print("Part 2: " + str(execute(is_part_two = True)))