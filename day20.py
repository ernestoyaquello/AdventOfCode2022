import input
from collections import defaultdict

PROBLEM_NUMBER = 20

def execute(is_part_two):
    numbers = [int(line) for line in input.read_lines(problem_number = PROBLEM_NUMBER)]
    return part_1(numbers) if not is_part_two else part_2(numbers)

def part_1(numbers):
    return decypher(numbers, 1)

def part_2(numbers):
    for index in range(len(numbers)):
        numbers[index] *= 811589153
    return decypher(numbers, 10)

def decypher(numbers, iterations):
    indices = {index: index for index in range(len(numbers))}
    reverse_indices = {index: index for index in range(len(numbers))}
    for _ in range(iterations):
        for index in range(len(numbers)):
            last_index = indices[index]
            number = numbers[last_index]
            if number != 0:
                new_index = last_index + number
                if new_index <= 0:
                    num_rounds = (((len(numbers) - 1) - last_index) + abs(number)) // (len(numbers) - 1)
                    new_index = (new_index - num_rounds) % len(numbers)
                elif new_index >= (len(numbers) - 1):
                    num_rounds = new_index // (len(numbers) - 1)
                    new_index = (new_index + num_rounds) % len(numbers)
                if new_index != last_index:
                    position_changes = [(index, new_index - indices[index])]
                    if new_index > last_index:
                        del numbers[last_index]
                        numbers.insert(new_index, number)
                        for i in range(new_index, last_index, -1):
                            j = reverse_indices[i]
                            position_changes.append((j, -1))
                    else:
                        numbers.insert(new_index, number)
                        del numbers[last_index + 1]
                        for i in range(new_index, last_index):
                            j = reverse_indices[i]
                            position_changes.append((j, 1))
                    for original_position, new_position_change in position_changes:
                        indices[original_position] += new_position_change
                        reverse_indices[indices[original_position]] = original_position

    zero_index = numbers.index(0)
    return numbers[(zero_index + 1000) % len(numbers)] + numbers[(zero_index + 2000) % len(numbers)] + numbers[(zero_index + 3000) % len(numbers)]

print("Part 1: " + str(execute(is_part_two = False)))
print("Part 2: " + str(execute(is_part_two = True)))