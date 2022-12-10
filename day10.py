import input

PROBLEM_NUMBER = 10

def execute(is_part_two):
    instructions = [(1, 0) if len(ins) == 1 else (2, int(ins[1])) for ins in input.read_lists(problem_number = PROBLEM_NUMBER)]
    return part_1(instructions) if not is_part_two else part_2(instructions)

def part_1(instructions):
    signal_strengths = 0

    x = 1
    cicle = 0

    jump = 40
    jump_offset = 20
    processed_jumps = 0
    for cicles, value in instructions:
        cicle += cicles
        jumps = int((cicle + jump_offset) / jump)
        if jumps > processed_jumps:
            jump_cicle = (jumps * jump) - jump_offset
            signal_strengths += jump_cicle * x
            processed_jumps = jumps
        x += value

    return signal_strengths

def part_2(instructions):
    screen = ""

    x = 1
    cicle = 0

    screen_width = 40
    for cicles, value in instructions:
        for _ in range(cicles):
            if cicle % screen_width == 0:
                screen += "\n"
            screen += '#' if abs(x - (cicle % screen_width)) <= 1 else ' '
            cicle += 1
        x += value

    return screen

print("Part 1: " + str(execute(is_part_two = False)))
print("Part 2: " + str(execute(is_part_two = True)))