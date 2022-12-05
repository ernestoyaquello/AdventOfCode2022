import input

PROBLEM_NUMBER = 5

# This implementation is absolutely ridiculous and unnecessarily complicated, but also kinda fun.
# Instead of doing the obvious and having a boring collection of stacks/lists with just the numbers,
# we have a two-dimensional array that captures the physical arrangement of the crates exactly as they
# appear on the problem text, including the empty spaces. A headache to code, but a joy to debug!
def execute(is_part_two):
    crates, instructions = read_crates_and_instructions()
    return part_1(crates, instructions) if not is_part_two else part_2(crates, instructions)

def part_1(crates, instructions):
    for num_moves, from_column, to_column in instructions:
        for _ in range(0, num_moves):
            from_row = 0
            to_row = len(crates) - 1
            while from_row < len(crates) and crates[from_row][from_column] == ' ': from_row += 1
            while to_row >= 0 and crates[to_row][to_column] != ' ': to_row -= 1
            if to_row >= 0:
                # The row we want to move the crate to exists, let's move it
                crates[to_row][to_column] = crates[from_row][from_column]
                crates[from_row][from_column] = ' '
            else:
                # The row we want to move the crate to doesn't exist, let's create it and then move the crate to it
                crates.insert(0, [' '] * len(crates[0]))
                crates[0][to_column] = crates[from_row + 1][from_column]
                crates[from_row + 1][from_column] = ' '
    return get_message(crates)

def part_2(crates, instructions):
    for num_moves, from_column, to_column in instructions:
        from_row = 0
        to_row = len(crates) - 1
        while from_row < len(crates) and crates[from_row][from_column] == ' ': from_row += 1
        while to_row >= 0 and crates[to_row][to_column] != ' ': to_row -= 1
        from_row += num_moves - 1
        for _ in range(0, num_moves):
            if to_row >= 0:
                # The row we want to move the crate to exists, let's move it
                crates[to_row][to_column] = crates[from_row][from_column]
                crates[from_row][from_column] = ' '
                to_row -= 1
                from_row -= 1
            else:
                # The row we want to move the crate to doesn't exist, let's create it and then move the crate to it
                crates.insert(0, [' '] * len(crates[0]))
                crates[0][to_column] = crates[from_row + 1][from_column]
                crates[from_row + 1][from_column] = ' '
    return get_message(crates)

def get_message(crates):
    message = ""

    for column in range(0, len(crates[0])):
        row = 0
        while row < len(crates) and crates[row][column] == ' ': row += 1
        if row < len(crates):
            message += crates[row][column]

    return message

def read_crates_and_instructions():
    lines = input.read_lines(problem_number = PROBLEM_NUMBER, strip = False)

    # Read crates into a two-dimensional array
    line_index = 0;
    crates = []
    for line in lines:
        line_index += 1
        if not line:
            break
        else:
            crates_row = []
            for index in range(0, len(line), 4):
                crate = list(line)[index + 1:index + 2][0]
                if not crate.isnumeric():
                    crates_row.append(crate)
                else:
                    break
            if len(crates_row) != 0:
                crates.append(crates_row)

    # Read instructions into a list, making sure the from/to columns are adjusted as indices (i.e., 1 -> 0, 2 -> 1, etc)
    instructions_raw = [instruction.replace("move ", "").replace("from ", "").replace("to ", "").split(' ') for instruction in lines[line_index:]]
    instructions = [(int(instruction_raw[0]), (int(instruction_raw[1]) - 1), (int(instruction_raw[2]) - 1)) for instruction_raw in instructions_raw]

    return (crates, instructions)

print("Part 1: " + str(execute(is_part_two = False)))
print("Part 2: " + str(execute(is_part_two = True)))