import input
import sys

PROBLEM_NUMBER = 18

def execute(is_part_two):
    cubes = [(int(x), int(y), int(z)) for x, y, z in input.read_lists(problem_number = PROBLEM_NUMBER, item_separator = ',')]
    return part_1(cubes) if not is_part_two else part_2(cubes)

def part_1(cubes):
    total_non_touching_sides = len(cubes) * 6

    for i, cube in enumerate(cubes):
        for other_cube in cubes[i + 1:]:
            if (abs(cube[0] - other_cube[0]) + abs(cube[1] - other_cube[1]) + abs(cube[2] - other_cube[2])) == 1:
                total_non_touching_sides -= 2

    return total_non_touching_sides

def part_2(cubes):
    #dimension_ranges = get_dimension_ranges(cubes)
    #first_steam_cube = (dimension_ranges[0][0] - 1, dimension_ranges[1][0] - 1, dimension_ranges[2][0] - 1)
    #return cound_steam_touched_sides_recursively(first_steam_cube, set(cubes), dimension_ranges)
    return count_steam_touched_sides(set(cubes), get_dimension_ranges(cubes))

def count_steam_touched_sides(lava_cubes, dimension_ranges, visited_steam_cubes = set(), unvisited_steam_cubes = set()):
    steam_touched_lava_sides = 0

    unvisited_steam_cubes.add((dimension_ranges[0][0] - 1, dimension_ranges[1][0] - 1, dimension_ranges[2][0] - 1))
    while len(unvisited_steam_cubes) > 0:
        steam_cube = unvisited_steam_cubes.pop()
        visited_steam_cubes.add(steam_cube)
        for relative_adjacent in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
            adjacent_cube = (steam_cube[0] + relative_adjacent[0], steam_cube[1] + relative_adjacent[1], steam_cube[2] + relative_adjacent[2])
            if adjacent_cube[0] >= dimension_ranges[0][0] - 1 and adjacent_cube[0] <= dimension_ranges[0][1] + 1 and adjacent_cube[1] >= dimension_ranges[1][0] - 1 and adjacent_cube[1] <= dimension_ranges[1][1] + 1 and adjacent_cube[2] >= dimension_ranges[2][0] - 1 and adjacent_cube[2] <= dimension_ranges[2][1] + 1:
                if adjacent_cube in lava_cubes:
                    steam_touched_lava_sides += 1
                elif adjacent_cube not in visited_steam_cubes:
                    unvisited_steam_cubes.add(adjacent_cube)

    return steam_touched_lava_sides

# Unused, causes stackoverflow when used with the actual input!
#def count_steam_touched_sides_recursively(cube, lava_cubes, dimension_ranges, visited_steam_cubes = set(), steam_touched_sides = [0]):
#    if cube in lava_cubes:
#        steam_touched_sides[0] += 1
#    else:
#        visited_steam_cubes.add(cube)
#        relative_adjacents = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
#        for relative_adjacent in relative_adjacents:
#            adjacent_cube = (cube[0] + relative_adjacent[0], cube[1] + relative_adjacent[1], cube[2] + relative_adjacent[2])
#            if adjacent_cube not in visited_steam_cubes and adjacent_cube[0] >= dimension_ranges[0][0] - 1 and adjacent_cube[0] <= dimension_ranges[0][1] + 1 and adjacent_cube[1] >= dimension_ranges[1][0] - 1 and adjacent_cube[1] <= dimension_ranges[1][1] + 1 and adjacent_cube[2] >= dimension_ranges[2][0] - 1 and adjacent_cube[2] <= dimension_ranges[2][1] + 1:
#                count_steam_touched_sides_recursively(adjacent_cube, lava_cubes, dimension_ranges, visited_steam_cubes, steam_touched_sides)
#    return steam_touched_sides[0]

def get_dimension_ranges(cubes):
    dimension_ranges = [(sys.maxsize, -sys.maxsize - 1), (sys.maxsize, -sys.maxsize - 1), (sys.maxsize, -sys.maxsize - 1)]

    for x, y, z in cubes:
        if x < dimension_ranges[0][0]: dimension_ranges[0] = (x, dimension_ranges[0][1])
        elif x > dimension_ranges[0][1]: dimension_ranges[0] = (dimension_ranges[0][0], x)
        if y < dimension_ranges[1][0]: dimension_ranges[1] = (y, dimension_ranges[1][1])
        elif y > dimension_ranges[1][1]: dimension_ranges[1] = (dimension_ranges[1][0], y)
        if z < dimension_ranges[2][0]: dimension_ranges[2] = (z, dimension_ranges[2][1])
        elif z > dimension_ranges[2][1]: dimension_ranges[2] = (dimension_ranges[2][0], z)

    return dimension_ranges

print("Part 1: " + str(execute(is_part_two = False)))
print("Part 2: " + str(execute(is_part_two = True)))