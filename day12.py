import input
import sys

PROBLEM_NUMBER = 12
ADJACENT_DIFFS = [(1, 0), (0, 1), (0, -1), (-1, 0)]

def execute(is_part_two):
    map, origin_coordinate, destination_coordinate = read_data()
    if is_part_two:
        return get_shortest_path_length(map, destination_coordinate)
    else:
        return get_shortest_path_length_from_origin(map, origin_coordinate, destination_coordinate)

def get_shortest_path_length(map, destination_coordinate):
    shortest_path = sys.maxsize

    all_coordinates = [(pos // len(map[0]), pos % len(map[0])) for pos in range(len(map) * len(map[0]))]
    candidate_origin_coordinates = list(filter(lambda c: map[c[0]][c[1]] == 'a', all_coordinates))
    for candidate_origin_coordinate in candidate_origin_coordinates:
        candidate_origin_shortest_path_length = get_shortest_path_length_from_origin(map, candidate_origin_coordinate, destination_coordinate, max_distance = shortest_path)
        shortest_path = min(shortest_path, candidate_origin_shortest_path_length)

    return shortest_path

def get_shortest_path_length_from_origin(map, origin_coordinate, destination_coordinate, max_distance = sys.maxsize):
    return get_distances(map, origin_coordinate, destination_coordinate, max_distance)[destination_coordinate]

def get_distances(map, origin_coordinate, destination_coordinate, max_distance):
    visited_coordinates = set()
    unvisited_coordinates = {(pos // len(map[0]), pos % len(map[0])) for pos in range(len(map) * len(map[0]))}
    distances = {unvisited_coordinate: sys.maxsize if unvisited_coordinate != origin_coordinate else 0 for unvisited_coordinate in unvisited_coordinates}

    current_coordinate = origin_coordinate
    while current_coordinate != None and current_coordinate != destination_coordinate and distances[current_coordinate] < max_distance:
        visited_coordinates.add(current_coordinate)
        unvisited_coordinates.remove(current_coordinate)

        for adjacent_coordinate in get_valid_adjacent_coordinates(map, current_coordinate, visited_coordinates):
            new_adjacent_distance = distances[current_coordinate] + 1
            if new_adjacent_distance < distances[adjacent_coordinate]:
                distances[adjacent_coordinate] = new_adjacent_distance

        current_coordinate = None
        min_next_distance = sys.maxsize
        for unvisited_coordinate in unvisited_coordinates:
            if distances[unvisited_coordinate] < min_next_distance:
                current_coordinate = unvisited_coordinate
                min_next_distance = distances[unvisited_coordinate]

    return distances

def get_valid_adjacent_coordinates(map, coordinate, visited_coordinates):
    adjacent_coordinates = []

    coordinate_value = ord(map[coordinate[0]][coordinate[1]])
    for row_diff, column_diff in ADJACENT_DIFFS:
        adjacent_row = coordinate[0] + row_diff
        adjacent_column = coordinate[1] + column_diff
        if 0 <= adjacent_row < len(map) and 0 <= adjacent_column < len(map[adjacent_row]):
            adjacent_coordinate_value = ord(map[adjacent_row][adjacent_column])
            adjacent_coordinate = (adjacent_row, adjacent_column)
            if (adjacent_coordinate_value < coordinate_value or (adjacent_coordinate_value - coordinate_value) <= 1) and adjacent_coordinate not in visited_coordinates:
                adjacent_coordinates.append(adjacent_coordinate)

    return adjacent_coordinates

def read_data():
    map = [list(line) for line in input.read_lines(problem_number = PROBLEM_NUMBER)]
    for row in range(len(map)):
        for column in range(len(map[0])):
            if map[row][column] == 'S':
                map[row][column] = 'a'
                origin_coordinate = (row, column)
            elif map[row][column] == 'E':
                map[row][column] = 'z'
                destination_coordinate = (row, column)
    return (map, origin_coordinate, destination_coordinate)

print("Part 1: " + str(execute(is_part_two = False)))
print("Part 2: " + str(execute(is_part_two = True)))