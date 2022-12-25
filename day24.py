import input
import math
import sys
from collections import defaultdict
from copy import copy

PROBLEM_NUMBER = 24

def execute(is_part_two):
    total_turns = 0

    blizzards_per_turn, rows, columns = read_blizzards_per_turn()
    origin = (0, -1)
    destination = (columns - 1, rows)
    turns_to_arrive = calculate_min_turns(blizzards_per_turn, rows, columns, origin, destination)
    if not is_part_two:
        total_turns = turns_to_arrive
    else:
        turns_to_come_back = calculate_min_turns(blizzards_per_turn, rows, columns, destination, origin, turn = turns_to_arrive, is_forward = False)
        turns_to_arrive_again = calculate_min_turns(blizzards_per_turn, rows, columns, origin, destination, turn = turns_to_arrive + turns_to_come_back)
        total_turns = turns_to_arrive + turns_to_come_back + turns_to_arrive_again

    return total_turns

def calculate_min_turns(blizzards_per_turn, rows, columns, origin, destination, turn = 0, is_forward = True):
    return _calculate_min_turns(blizzards_per_turn, rows, columns, origin, destination, turn, is_forward, min_turns = [sys.maxsize], cache = {})

def _calculate_min_turns(blizzards_per_turn, rows, columns, origin, destination, turn, is_forward, min_turns, cache):
    cache_key = (turn % len(blizzards_per_turn), origin)
    if cache_key in cache.keys():
        return cache[cache_key]

    extra_turns = (sys.maxsize - turn) if origin != destination else 0
    if origin != destination:
        next_turn = turn + 1
        for next_position_diff in [(1, 0), (0, 1), (-1, 0), (0, -1), None] if is_forward else [(-1, 0), (0, -1), (1, 0), (0, 1), None]:
            if next_turn < min_turns[0]:
                next_origin = origin if next_position_diff == None else (origin[0] + next_position_diff[0], origin[1] + next_position_diff[1])
                if (0 <= next_origin[0] < columns and 0 <= next_origin[1] < rows) or next_origin == origin or next_origin == destination:
                    if len(blizzards_per_turn[next_turn % len(blizzards_per_turn)][next_origin]) == 0:
                        next_manhattan_distance = abs(destination[0] - next_origin[0]) + abs(destination[1] - next_origin[1])
                        if (next_turn + next_manhattan_distance) < min_turns[0]:
                            extra_turns = min(extra_turns, 1 + _calculate_min_turns(blizzards_per_turn, rows, columns, next_origin, destination, next_turn, is_forward, min_turns, cache))
                            min_turns[0] = min(min_turns[0], turn + extra_turns)

    cache[cache_key] = extra_turns
    return extra_turns

def read_blizzards_per_turn():
    blizzards_per_turn = []

    # Read initial map
    map = [list(line) for line in input.read_lines(problem_number = PROBLEM_NUMBER)]
    all_blizzards = defaultdict(list)
    for y, row in enumerate(map[1:len(map) - 1]):
        for x, character in enumerate(row[1:len(row) - 1]):
            if character == '<': all_blizzards[(x, y)].append((-1, 0))
            elif character == '^': all_blizzards[(x, y)].append((0, -1))
            elif character == '>': all_blizzards[(x, y)].append((1, 0))
            elif character == 'v': all_blizzards[(x, y)].append((0, 1))

    # Calculate the blizzards that will exist for each turn
    rows = len(map) - 2
    columns = len(map[0]) - 2
    loop_length = math.lcm(rows, columns)
    blizzards_per_turn.append(all_blizzards)
    for turn in range(1, loop_length):
        next_all_blizzards = defaultdict(list)
        for (x, y), blizzards in blizzards_per_turn[turn - 1].items():
            for next_x_diff, next_y_diff in blizzards:
                next_x = (x + next_x_diff) % columns
                next_y = (y + next_y_diff) % rows
                next_all_blizzards[(next_x, next_y)].append((next_x_diff, next_y_diff))
        blizzards_per_turn.append(next_all_blizzards)

    return (blizzards_per_turn, rows, columns)

print("Part 1: " + str(execute(is_part_two = False)))
print("Part 2: " + str(execute(is_part_two = True)))