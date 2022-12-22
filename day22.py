import input
import sys

PROBLEM_NUMBER = 22

def execute(is_part_two):
    path, moves, position = read_path_and_moves_and_position(is_cube = is_part_two)
    return execute_moves(path, moves, position)

def execute_moves(path, moves, position):
    facing = 0

    for move in moves:
        if move == 'L':
            facing = (facing - 1) % 4
        elif move == 'R':
            facing = (facing + 1) % 4
        else:
            num_moves = 0
            while num_moves < move:
                candidate_position = path[position]['adjacent'][(facing + 2) % 4]
                if path[candidate_position[0]]['content'] != '#':
                    position = candidate_position[0]
                    facing += candidate_position[1]
                    num_moves += 1
                else:
                    break

    return (1000 * (position[1] + 1)) + (4 * (position[0] + 1)) + facing

def read_path_and_moves_and_position(is_cube):
    path = {}
    moves = []
    position = None

    # Read path
    ltrb = (sys.maxsize, sys.maxsize, -sys.maxsize - 1, -sys.maxsize - 1) # left, top. right, bottom
    y = 0
    for line in input.read_lines(problem_number = PROBLEM_NUMBER, strip = False):
        if line != '' and not line[0].isnumeric():
            # Read path line
            for x, content in enumerate(list(line)):
                if content != ' ':
                    path[(x, y)] = {'content': content}
                    if position == None and y == 0:
                        position = (x, y)
                ltrb = (min(ltrb[0], x), min(ltrb[1], y), max(ltrb[2], x), max(ltrb[3], y))
            y += 1
        else:
            # Read moves line
            index = 0
            while index < len(line):
                number_as_str = ""
                while index < len(line) and line[index].isnumeric():
                    number_as_str += line[index]
                    index += 1
                moves.append(int(number_as_str))
                if index < len(line):
                    moves.append(line[index])
                    index += 1

    if not is_cube:
        set_adjacent_positions(path, ltrb)
    else:
        set_adjacent_positions_for_cube(path, ltrb)

    return (path, moves, position)

def set_adjacent_positions(path, ltrb):
    for x, y in path.keys():
        left = (x - 1, y)
        if left not in path.keys():
            for candidate_x in range(ltrb[2], x - 1, -1):
                left = (candidate_x, y)
                if left in path.keys():
                    break
        top = (x, y - 1)
        if top not in path.keys():
            for candidate_y in range(ltrb[3], y - 1, -1):
                top = (x, candidate_y)
                if top in path.keys():
                    break
        right = (x + 1, y)
        if right not in path.keys():
            for candidate_x in range(ltrb[0], x + 1):
                right = (candidate_x, y)
                if right in path.keys():
                    break
        bottom = (x, y + 1)
        if bottom not in path.keys():
            for candidate_y in range(ltrb[1], y + 1):
                bottom = (x, candidate_y)
                if bottom in path.keys():
                    break
        path[(x, y)]['adjacent'] = ((left, 0), (top, 0), (right, 0), (bottom, 0))

def set_adjacent_positions_for_cube(path, ltrb):
    cube_side_size = abs((ltrb[2] - ltrb[0]) - (ltrb[3] - ltrb[1]))
    unfolded_cube_rows = ((ltrb[3] - ltrb[1]) + 1) // cube_side_size
    unfolded_cube_columns = ((ltrb[2] - ltrb[0]) + 1) // cube_side_size
    unfolded_cube_side_positions = []
    cube_side_connections = {}
    for y in range(0, unfolded_cube_rows * cube_side_size, cube_side_size):
        for x in range(0, unfolded_cube_columns * cube_side_size, cube_side_size):
            if (x, y) in path.keys():
                unfolded_cube_side_position = (x // cube_side_size, y // cube_side_size)
                unfolded_cube_side_positions.append(unfolded_cube_side_position)
                cube_side_connections[unfolded_cube_side_position] = {}

    # Find sides that are directly connected
    for side_position in unfolded_cube_side_positions:
        left_side_position = (side_position[0] - 1, side_position[1])
        if any(other_side_position for other_side_position in unfolded_cube_side_positions if other_side_position == left_side_position):
            cube_side_connections[side_position]['left'] = (left_side_position, 0)
            cube_side_connections[left_side_position]['right'] = (side_position, 0)
        top_side_position = (side_position[0], side_position[1] - 1)
        if any(other_side_position for other_side_position in unfolded_cube_side_positions if other_side_position == top_side_position):
            cube_side_connections[side_position]['top'] = (top_side_position, 0)
            cube_side_connections[top_side_position]['bottom'] = (side_position, 0)
    
    # Find sides that are connecetd through an intermediate connection, run it twice to allow all connections to be found
    for _ in range(2):
        for side_position in unfolded_cube_side_positions:
            find_indirect_side_connections(cube_side_connections, side_position)

    # Finally, create the adjacent positions
    for x, y in path.keys():
        left = ((x - 1, y), 0)
        if left[0] not in path.keys(): left = get_position_and_rotation(cube_side_size, cube_side_connections, x, y, 'left', (-1, 0))
        top = ((x, y - 1), 0)
        if top[0] not in path.keys(): top = get_position_and_rotation(cube_side_size, cube_side_connections, x, y, 'top', (0, -1))
        right = ((x + 1, y), 0)
        if right[0] not in path.keys(): right = get_position_and_rotation(cube_side_size, cube_side_connections, x, y, 'right', (1, 0))
        bottom = ((x, y + 1), 0)
        if bottom[0] not in path.keys(): bottom = get_position_and_rotation(cube_side_size, cube_side_connections, x, y, 'bottom', (0, 1))
        path[(x, y)]['adjacent'] = (left, top, right, bottom)

def find_indirect_side_connections(all_cube_side_connections, side_position):
    # For each side, find each directly connected side by traversing the indirectly connected sides.
    # Not a great explanation, but this code is madness and I refuse to try to break it all down with words. Cool problem though, super fun!
    side_connections = all_cube_side_connections[side_position]
    directions = ['left', 'top', 'right', 'bottom']
    for initial_target_connection_index in [0, 1, 2, 3]: # Left, top, right, bottom
        if directions[initial_target_connection_index] not in side_connections.keys():
            for initial_intermediate_connection_index in ([1, 3] if initial_target_connection_index in [0, 2] else [0, 2]):
                target_connection_index = initial_target_connection_index
                rotation = 0
                rotation_increment = 1 if initial_intermediate_connection_index == ((initial_target_connection_index + 1) % 4) else -1
                intermediate_connection_index = initial_intermediate_connection_index
                if directions[intermediate_connection_index] in side_connections.keys():
                    intermediate_connection = side_connections[directions[intermediate_connection_index]]
                    intermediate_connection_index = (intermediate_connection_index + intermediate_connection[1]) % 4
                    target_connection_index = (target_connection_index + intermediate_connection[1]) % 4
                    rotation += (rotation + (intermediate_connection[1] + rotation_increment)) % 4
                    intermediate_side = intermediate_connection[0]
                    distance = 1
                    while directions[target_connection_index] not in all_cube_side_connections[intermediate_side].keys():
                        if directions[intermediate_connection_index] in all_cube_side_connections[intermediate_side].keys():
                            intermediate_connection = all_cube_side_connections[intermediate_side][directions[intermediate_connection_index]]
                            intermediate_connection_index = (intermediate_connection_index + intermediate_connection[1]) % 4
                            target_connection_index = (target_connection_index + intermediate_connection[1]) % 4
                            rotation = (rotation + (intermediate_connection[1] + rotation_increment)) % 4
                            intermediate_side = intermediate_connection[0]
                            distance += 1
                            if distance == 3:
                                break
                        else:
                            break
                    if directions[target_connection_index] in all_cube_side_connections[intermediate_side].keys():
                        target_connection = all_cube_side_connections[intermediate_side][directions[target_connection_index]]
                        rotation = (rotation + target_connection[1]) % 4
                        side_connections[directions[initial_target_connection_index]] = (target_connection[0], rotation)

def get_position_and_rotation(cube_side_size, cube_side_connections, x, y, direction_label, direction):
    unfolded_cube_side_position = (x // cube_side_size, y // cube_side_size)
    relative_position = (x % cube_side_size, y % cube_side_size)
    side_connection = cube_side_connections[unfolded_cube_side_position][direction_label]
    placement = next(label for label, side in cube_side_connections[side_connection[0]].items() if side[0] == unfolded_cube_side_position)
    if placement == 'left': placement_offset = (-1, 0)
    elif placement == 'top': placement_offset = (0, -1)
    elif placement == 'right': placement_offset = (1, 0)
    elif placement == 'bottom': placement_offset = (0, 1)
    for _ in range(side_connection[1] % 4):
        relative_position = ((cube_side_size - 1) - relative_position[1], relative_position[0])
        direction = (-direction[1], direction[0])
    position = (relative_position[0] + ((side_connection[0][0] + placement_offset[0]) * cube_side_size) + direction[0], relative_position[1] + ((side_connection[0][1] + placement_offset[1]) * cube_side_size) + direction[1])

    return (position, (side_connection[1] % 4))

print("Part 1: " + str(execute(is_part_two = False)))
print("Part 2: " + str(execute(is_part_two = True)))