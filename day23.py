import input
import sys
from collections import defaultdict

PROBLEM_NUMBER = 23

MOVES = [(0, -1), (0, 1), (-1, 0), (1, 0)]
ADJACENT_DIFFS = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

def execute(is_part_two):
    return simulate_rounds(read_elves())[0] if not is_part_two else simulate_rounds(read_elves(), max_rounds = None)[1]

def simulate_rounds(elves, max_rounds = 10):
    round = 0
    while max_rounds == None or round < max_rounds:
        # First half, propose moves
        proposed_moves = []
        proposed_destinations = defaultdict(bool)
        for elf_position in elves.keys():
            has_elves_around = False
            for x_diff, y_diff in ADJACENT_DIFFS:
                if (elf_position[0] + x_diff, elf_position[1] + y_diff) in elves.keys():
                    has_elves_around = True
                    break
            if has_elves_around:
                proposed_next_position = None
                next_move_index = round % len(MOVES)
                inspected_moves = 0
                while proposed_next_position == None and inspected_moves < len(MOVES):
                    proposed_next_position = (elf_position[0] + MOVES[next_move_index][0], elf_position[1] + MOVES[next_move_index][1])
                    positions_to_check = [proposed_next_position]
                    if MOVES[next_move_index][0] != 0: positions_to_check.extend([(proposed_next_position[0], proposed_next_position[1] - 1), (proposed_next_position[0], proposed_next_position[1] + 1)])
                    elif MOVES[next_move_index][1] != 0: positions_to_check.extend([(proposed_next_position[0] - 1, proposed_next_position[1]), (proposed_next_position[0] + 1, proposed_next_position[1])])
                    if any(position_to_check for position_to_check in positions_to_check if position_to_check in elves.keys()):
                        # Valid move not found because there is an elf in a forbidden position, keep looking
                        proposed_next_position = None
                        next_move_index = (next_move_index + 1) % len(MOVES)
                        inspected_moves += 1
                    else:
                        # Valid move found
                        if not proposed_destinations[proposed_next_position]:
                            # Destination hasn't been proposed yet, let's add the move
                            proposed_moves.append((elf_position, proposed_next_position))
                            proposed_destinations[proposed_next_position] = True
                        else:
                            # Destination has already been proposed, so we don't add this move and we delete the existing move with this destination
                            move_to_remove = next(proposed_move for proposed_move in proposed_moves if proposed_move[1] == proposed_next_position)
                            proposed_moves.remove(move_to_remove)
                        break

        # Second half, apply the moves or stop simulating rounds if there aren't any possible moves
        if len(proposed_moves) > 0:
            for old_elf_position, new_elf_position in proposed_moves:
                if not any(1 for inner_old_elf_position, inner_new_elf_position in proposed_moves if inner_old_elf_position != old_elf_position and inner_new_elf_position == new_elf_position):
                    del elves[old_elf_position]
                    elves[new_elf_position] = True
        else:
            break

        round += 1

    # Calculate minimum rectangle area that contains every elf
    ltrb = (sys.maxsize, sys.maxsize, -sys.maxsize - 1, -sys.maxsize - 1)
    for elf_x, elf_y in elves:
        ltrb = (min(ltrb[0], elf_x), min(ltrb[1], elf_y), max(ltrb[2], elf_x), max(ltrb[3], elf_y))
    minimum_rectangle_area = (ltrb[2] - ltrb[0] + 1) * (ltrb[3] - ltrb[1] + 1)

    # Return both the number of empty tiles and the round when movement stopped
    return (minimum_rectangle_area - len(elves), round + 1)

def read_elves():
    elves = {}

    initial_map = [list(row) for row in input.read_lines(problem_number = PROBLEM_NUMBER)]
    for y, row in enumerate(initial_map):
        for x, value in enumerate(row):
            if value == '#':
                elves[(x, y)] = True

    return elves

print("Part 1: " + str(execute(is_part_two = False)))
print("Part 2: " + str(execute(is_part_two = True)))