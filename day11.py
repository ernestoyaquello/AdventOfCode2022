import input
import re

PROBLEM_NUMBER = 11

def execute(is_part_two):
    monkeys = read_monkeys()
    execute_rounds(monkeys, num_rounds = 20 if not is_part_two else 10000, divide_by_three = not is_part_two)
    inspection_counts = sorted([monkey['inspected'] for monkey in monkeys], reverse = True)
    return inspection_counts[0] * inspection_counts[1]

def execute_rounds(monkeys, num_rounds, divide_by_three):
    # Calculate the modules of each item for each one of the divisors
    divisors = [monkey['divisor_test'] for monkey in monkeys]
    for monkey in monkeys:
        monkey['item_modules'] = [{divisor: item % divisor for divisor in divisors} for item in monkey['items']]

    for _ in range(num_rounds):
        for monkey in monkeys:
            items_key = 'items' if divide_by_three else 'item_modules'
            while monkey[items_key]:
                item = monkey[items_key].pop()

                op_symbol = monkey['operation'][0]
                op_right_side = monkey['operation'][1]
                if divide_by_three:
                    # Simply apply the logic to the item exactly as described, no need to update the modules
                    right_side = item if op_right_side == 'old' else int(op_right_side)
                    item = (item * right_side) if op_symbol == '*' else (item + right_side)
                    item //= 3
                    target_monkey = monkey['target'][(item % monkey['divisor_test']) == 0]
                else:
                    # Apply the logic, but without updating the item itself, we just update its modules
                    for divisor, module in item.items():
                        right_side = module if op_right_side == 'old' else int(op_right_side)
                        item[divisor] = (module * right_side) if op_symbol == '*' else (module + right_side)
                        item[divisor] %= divisor
                    target_monkey = monkey['target'][item[monkey['divisor_test']] == 0]

                # Inspection finished, throw the item
                monkeys[target_monkey][items_key].append(item)
                monkey['inspected'] += 1

def read_monkeys():
    monkeys = []

    full_input = input.read(problem_number = PROBLEM_NUMBER)
    input_pattern = re.compile(r"Monkey \d+:\s+[a-zA-z :]+((?:\d+(?:, )?)+)\s+[a-zA-z :]+= (?:\w|\d)+ ([*+]) ((?:\w|\d)+)\s+[a-zA-z :]+(\d+)\s+[a-zA-z :]+(\d+)\s+[a-zA-z :]+(\d+)")
    for input_match in input_pattern.finditer(full_input):
        monkeys.append({
            'items': list(map(int, input_match.group(1).split(', '))),
            'operation': (input_match.group(2), input_match.group(3)),
            'divisor_test': int(input_match.group(4)),
            'target': {True: int(input_match.group(5)), False: int(input_match.group(6))},
            'inspected': 0,
        })

    return monkeys

print("Part 1: " + str(execute(is_part_two = False)))
print("Part 2: " + str(execute(is_part_two = True)))