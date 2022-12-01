import input

PROBLEM_NUMBER = 1

def execute(is_part_two):
    calories_per_elf = [sum(map(int, calories)) for calories in input.read_lists(problem_number = PROBLEM_NUMBER, list_separator = '\n\n', item_separator = '\n')]
    return sum(sorted(calories_per_elf, reverse=True)[0:(1 if not is_part_two else 3)])

print("Part 1: " + str(execute(is_part_two = False)))
print("Part 2: " + str(execute(is_part_two = True)))