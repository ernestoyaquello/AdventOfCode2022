import input
from collections import defaultdict

PROBLEM_NUMBER = 17

#|OOOO
ROCK_1 = { 'id': 1, 'width': 4, 'height': 1, 'coordinates': [ (0, 0), (1, 0), (2, 0), (3, 0) ] }

#| O
#|OOO
#| O
ROCK_2 = { 'id': 2, 'width': 3, 'height': 3, 'coordinates': [ (1, 2), (0, 1), (1, 1), (2, 1), (1, 0) ] }

#|  O
#|  O
#|OOO
ROCK_3 = { 'id': 3, 'width': 3, 'height': 3, 'coordinates': [ (0, 2), (1, 2), (2, 2), (2, 1), (2, 0) ] }

#|O
#|O
#|O
#|O
ROCK_4 = { 'id': 4, 'width': 1, 'height': 4, 'coordinates': [ (0, 3), (0, 2), (0, 1), (0, 0) ] }

#|OO
#|OO
ROCK_5 = { 'id': 5, 'width': 2, 'height': 2, 'coordinates': [ (0, 1), (1, 1), (0, 0), (1, 0) ] }

ROCKS = [ROCK_1, ROCK_2, ROCK_3, ROCK_4, ROCK_5]

def execute(is_part_two):
    return add_rocks(list(ROCKS), read_move_patterns(), rocks_to_add = 2022 if not is_part_two else 1000000000000)

def add_rocks(rocks, move_patterns, rocks_to_add):
    # The initial scenario never repeats itself, so we add a few rocks first to leave it behind.
    # This way, we make sure that can safely look for repeating cycles later.
    initial_rocks_to_add = 1000
    placed_rocks_map = defaultdict(bool)
    tower_height, offset_y = calculate_tower_height(placed_rocks_map, rocks, move_patterns, rocks_to_add = initial_rocks_to_add)
    added_rocks = initial_rocks_to_add

    # Look for repeating cycles, stopping as soon as we find one
    map_snapshots = set()
    tower_height_increment_per_cycle = 0
    local_rocks_to_add = len(rocks)
    while True:
        new_tower_height, offset_y = calculate_tower_height(placed_rocks_map, rocks, move_patterns, local_rocks_to_add, initial_tower_height = tower_height, initial_offset_y = offset_y)
        added_rocks += local_rocks_to_add
        map_snapshot = take_map_snapshot(placed_rocks_map, rocks, move_patterns, offset_y)
        if map_snapshot not in map_snapshots:
            map_snapshots.add(map_snapshot)
            tower_height_increment_per_cycle += new_tower_height - tower_height
            tower_height = new_tower_height
        else:
            # We found a cycle! Let's get out of here
            tower_height = new_tower_height
            break

    # We have found a repeating cycle, let's use it to calculate (most of) the remaining iterations without actually iterating
    rocks_per_cycle = added_rocks - local_rocks_to_add - initial_rocks_to_add
    cycles_to_add = (rocks_to_add - added_rocks) // rocks_per_cycle
    added_rocks += cycles_to_add * rocks_per_cycle
    additional_tower_height = cycles_to_add * tower_height_increment_per_cycle

    # Calculate the result for the remaining rocks, if any
    remaining_rocks = rocks_to_add - added_rocks
    if remaining_rocks > 0:
        tower_height = calculate_tower_height(placed_rocks_map, rocks, move_patterns, remaining_rocks, initial_tower_height = tower_height, initial_offset_y = offset_y)[0]

    return tower_height + additional_tower_height

def calculate_tower_height(map, rocks, move_patterns, rocks_to_add, initial_tower_height = 0, initial_offset_y = -3):
    tower_height = initial_tower_height
    offset_y = initial_offset_y
    width = 7

    added_rocks = 0
    while added_rocks < rocks_to_add:
        rock = rocks.pop(0)

        rock_offset_x = 2
        rock_offset_y = offset_y - (rock['height'] - 1)
        is_added = False
        while not is_added:
            move = move_patterns.pop(0)
            move_x, move_y = move['move']

            is_valid_move = True
            coordinates_after_move = []
            for x, y in rock['coordinates']:
                adjusted_x = x + rock_offset_x + move_x
                adjusted_y = y + rock_offset_y + move_y
                coordinates_after_move.append((adjusted_x, adjusted_y))
                if adjusted_x < 0 or adjusted_x >= width or adjusted_y > 0 or map[(adjusted_x, adjusted_y)]:
                    is_valid_move = False

            if is_valid_move:
                rock_offset_x += move_x
                rock_offset_y += move_y
            elif move_y == 1:
                # The rock has found an obstacle when trying to go down, we can confirm it is now resting
                is_added = True
                added_rocks += 1
                # Let's find the new tower height
                previous_tower_height = tower_height
                for coordinate_after_move_x, coordinate_after_move_y in coordinates_after_move:
                    map[(coordinate_after_move_x, coordinate_after_move_y - 1)] = True
                    tower_height = max(tower_height, abs(coordinate_after_move_y - 2))
                offset_y -= tower_height - previous_tower_height

            move_patterns.append(move)

        rocks.append(rock)

    return (tower_height, offset_y)

def take_map_snapshot(map, rocks, move_patterns, total_offset_y):
    map_snapshot = str(rocks[0]['id']) + " | " + str(move_patterns[0]['id'])
    for y in range(total_offset_y - 2, total_offset_y + 20):
        map_snapshot += "\n"
        for x in range(7):
            map_snapshot += "#" if map[(x, y)] else '.'

    return map_snapshot

def read_move_patterns():
    move_patterns = [{ 'id': index, 'move': ((-1, 0) if symbol == '<' else (1, 0)) } for index, symbol in enumerate(list(input.read(problem_number = PROBLEM_NUMBER).strip()))]

    # Insert a move to go down right after each horizontal move
    for index in range(len(move_patterns), 0, -1):
        move_patterns.insert(index, { 'id': index, 'move': (0, 1) }) 

    return move_patterns

print("Part 1: " + str(execute(is_part_two = False)))
print("Part 2: " + str(execute(is_part_two = True)))