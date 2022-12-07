import input
import re

PROBLEM_NUMBER = 6

def execute(is_part_two):
    line = input.read_lines(problem_number = PROBLEM_NUMBER)[0]
    return detect_first_start_of_message_position(line, sequence_size = 4 if not is_part_two else 14)

def detect_first_start_of_message_position(line, sequence_size):
    # This regex is completely unnecessary, but we were talking about regex
    # yesterday and I wanted to use some today no matter what ¯\_(ツ)_/¯
    sequences = re.findall("(?=(\w{" + str(sequence_size) + "}))", line)
    return sequence_size + next(index for index, sequence in enumerate(sequences) if len(set(sequence)) == sequence_size)

print("Part 1: " + str(execute(is_part_two = False)))
print("Part 2: " + str(execute(is_part_two = True)))