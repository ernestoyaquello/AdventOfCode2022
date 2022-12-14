import input
import sys
from collections import defaultdict

PROBLEM_NUMBER = 14

def calculate_number_of_valid_drops(is_part_two):
    resting_units = 0

    # To avoid dropping from (500, 0) every single time, which is expensive, we keep track of which coordinate is the previous
    # one to any given coordinate in the latest fall path. This way, we can drop the next grain directly from that coordinate
    # (the previous in the fall path), no need to drop it from the very top every time.
    coordinate_to_previous_coordinate = {}
    map, ltrb = read_map_and_ltrb(is_part_two)
    drop_coordinate = (500, 0)
    while drop_coordinate != None:
        fall_coordinates = calculate_fall_coordinates(drop_coordinate, map, ltrb, floor_y = ltrb[3] if is_part_two else None)
        destination_coordinate = fall_coordinates[len(fall_coordinates) - 1]
        map[destination_coordinate] = True
        resting_units += 1 if destination_coordinate[1] != sys.maxsize else 0
        if destination_coordinate[1] < sys.maxsize and fall_coordinates != [(500, 0)]:
            # Calculate the previous coordinates mapping
            for visited_coordinate_index in range(1, len(fall_coordinates)):
                coordinate_to_previous_coordinate[fall_coordinates[visited_coordinate_index]] = fall_coordinates[visited_coordinate_index - 1]
            # Mark the previous coordinate in the fall path as the next one to drop a grain from
            drop_coordinate = coordinate_to_previous_coordinate[destination_coordinate]
        else:
            # Either grains aren't resting anymore or there isn't space to drop more of them
            drop_coordinate = None

    return resting_units

def calculate_fall_coordinates(drop_coordinate, map, ltrb, floor_y):
    fall_coordinates = [drop_coordinate]

    previous_fall_coordinate = drop_coordinate
    for candidate_y in range(drop_coordinate[1] + 1, ltrb[3] + 2):
        candidate_coordinate = (previous_fall_coordinate[0], candidate_y)
        if map[candidate_coordinate] or (floor_y != None and candidate_coordinate[1] == floor_y):
            candidate_coordinate = (previous_fall_coordinate[0] - 1, candidate_y)
        if map[candidate_coordinate] or (floor_y != None and candidate_coordinate[1] == floor_y):
            candidate_coordinate = (previous_fall_coordinate[0] + 1, candidate_y)
        if map[candidate_coordinate] or (floor_y != None and candidate_coordinate[1] == floor_y):
            # Cannot place the grain in any coordinate at this point, no need to continue looking for more coordinates
            break
        elif floor_y == None and (candidate_coordinate[1] > ltrb[3] or candidate_coordinate[0] < ltrb[0] or candidate_coordinate[0] > ltrb[2]):
            # Infinite fall, no need to continue looking for the next coordinate
            fall_coordinates.append((candidate_coordinate[0], sys.maxsize))
            break
        else:
            # Valid coordinate, let's continue simulating the fall of this grain
            fall_coordinates.append(candidate_coordinate)
            previous_fall_coordinate = fall_coordinates[len(fall_coordinates) - 1]
    
    return fall_coordinates

def read_map_and_ltrb(is_part_two):
    map = defaultdict(bool)
    ltrb = (500, 0, 500, 0) # Left, Top, Right, Bottom

    paths = input.read_lists(problem_number = PROBLEM_NUMBER, item_separator = ' -> ')
    for raw_path in paths:
        # Parse path segments
        path = [(int(raw_coordinate.split(',')[0]), int(raw_coordinate.split(',')[1])) for raw_coordinate in raw_path]
        # Determine global edges
        for segment_start, segment_end in path:
            ltrb = (min(ltrb[0], segment_start), min(ltrb[1], segment_end), max(ltrb[2], segment_start), max(ltrb[3], segment_end))
        # Fill the map with all the coordinates that belong to the path (true for wall; false for empty space)
        for index, next_copordinate in enumerate(path[1:]):
            previous_coordinate = path[index]
            for x in range(min(previous_coordinate[0], next_copordinate[0]), max(previous_coordinate[0], next_copordinate[0]) + 1):
                map[(x, previous_coordinate[1])] = True
            for y in range(min(previous_coordinate[1], next_copordinate[1]), max(previous_coordinate[1], next_copordinate[1]) + 1):
                map[(previous_coordinate[0], y)] = True

    # Add two extra rows at the bottom for the part 2 of the problem
    if is_part_two:
        ltrb = (ltrb[0], ltrb[1], ltrb[2], ltrb[3] + 2)

    return (map, ltrb)

print("Part 1: " + str(calculate_number_of_valid_drops(is_part_two = False)))
print("Part 2: " + str(calculate_number_of_valid_drops(is_part_two = True)))