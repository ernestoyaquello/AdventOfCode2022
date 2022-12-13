import input
from functools import cmp_to_key

PROBLEM_NUMBER = 13

def part_1():
    valid_indices_sum = 0

    pairs = [input.read_lists(problem_number = PROBLEM_NUMBER, list_separator = "\n\n", item_separator = "\n")][0]
    processed_pairs = [(process_expression(left), process_expression(right)) for left, right in pairs]
    for index, (left, right) in enumerate(processed_pairs):
        valid_indices_sum += (index + 1) if (compare(left, right) < 0) else 0

    return valid_indices_sum

def part_2():
    decoder = 1

    packages = list(filter(lambda l: l != '', input.read_lines(problem_number = PROBLEM_NUMBER))) + ["[[2]]", "[[6]]"]
    processed_packages = sorted([process_expression(package) for package in packages], key = cmp_to_key(compare))
    for index, package in enumerate(processed_packages):
        decoder *= (index + 1) if package == [[2]] or package == [[6]] else 1

    return decoder

def compare(left, right):
    result = 0

    index = 0
    while result == 0:
        if index < len(left) and index < len(right):
            # There are still available items on both sides and no result, let's keep comparing
            if isinstance(left[index], int) and isinstance(right[index], int):
                result = (left[index] > right[index]) - (left[index] < right[index])
            else:
                left_list = left[index] if isinstance(left[index], list) else [left[index]]
                right_list = right[index] if isinstance(right[index], list) else [right[index]]
                result = compare(left_list, right_list)
            index += 1
        else:
            # No more items are available to compare and still no result, let's compare the list sizes
            result = (len(left) > len(right)) - (len(left) < len(right))
            break

    return result

def process_expression(expression):
    return _process_expression(list(expression))[0]

def _process_expression(expression):
    expression_list = []

    while len(expression) > 0:
        character = expression.pop(0)
        if character == '[':
            expression_list.append(_process_expression(expression))
        elif character.isnumeric():
            number = str(character)
            next_digit = expression[0]
            while next_digit.isnumeric():
                del expression[0]
                number += next_digit
                next_digit = expression[0]
            expression_list.append(int(number))
        elif character == ']':
            break

    return expression_list

print("Part 1: " + str(part_1()))
print("Part 2: " + str(part_2()))