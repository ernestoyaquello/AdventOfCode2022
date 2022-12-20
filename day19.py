import input
import re
import sys

PROBLEM_NUMBER = 19
INPUT_PATTERN = re.compile(r"Blueprint \d+: Each ore robot costs (\d+) ore\. Each clay robot costs (\d+) ore\. Each obsidian robot costs (\d+) ore and (\d+) clay\. Each geode robot costs (\d+) ore and (\d+) obsidian\.")

def execute(is_part_two):
    robot_amounts = [1, 0, 0, 0] # ore robots, clay robots, obsidian robots, geode robots
    material_amounts = [0, 0, 0, 0] # ore, clay, obsidian, geodes
    blueprints = [([int(match.group(1)), 0, 0, 0], [int(match.group(2)), 0, 0, 0], [int(match.group(3)), int(match.group(4)), 0, 0], [int(match.group(5)), 0, int(match.group(6)), 0]) for line in input.read_lines(problem_number = PROBLEM_NUMBER) for match in INPUT_PATTERN.finditer(line)]
    max_material_amounts = {}
    for index, robot_costs in enumerate(blueprints):
        blueprint_id = index + 1
        local_max_material_amounts = [0, 0, 0, sys.maxsize]
        for robot_cost in robot_costs:
            for cost_index, cost in enumerate(robot_cost[0:3]):
                local_max_material_amounts[cost_index] = max(local_max_material_amounts[cost_index], cost)
        max_material_amounts[blueprint_id] = local_max_material_amounts
    return part_1(robot_amounts, material_amounts, blueprints, max_material_amounts) if not is_part_two else part_2(robot_amounts, material_amounts, blueprints, max_material_amounts)

def part_1(robot_amounts, material_amounts, blueprints, max_material_amounts):
    sum_quality_levels = 0

    for index, robot_costs in enumerate(blueprints):
        blueprint_id = index + 1
        sum_quality_levels += blueprint_id * calculate_max_number_of_geodes(blueprint_id, robot_amounts, material_amounts, robot_costs, max_material_amounts[blueprint_id], 24, {})
        print("Part 1 ... " + str(round(100 * (index + 1) / len(blueprints), 2)) + "%")

    return sum_quality_levels

def part_2(robot_amounts, material_amounts, blueprints, max_material_amounts):
    mul_max_number_of_geodes = 1

    for index, robot_costs in enumerate(blueprints[0:3]):
        blueprint_id = index + 1
        mul_max_number_of_geodes *= calculate_max_number_of_geodes(blueprint_id, robot_amounts, material_amounts, robot_costs, max_material_amounts[blueprint_id], 32, {})
        print("Part 2 ... " + str(round(100 * (index + 1) / 3.0, 2)) + "%")

    return mul_max_number_of_geodes

def calculate_max_number_of_geodes(blueprint_id, last_robot_amounts, last_material_amounts, robot_costs, max_material_amounts, minutes, cache, last_skipped_robots = []):
    cache_key = (minutes, str(last_robot_amounts), str(last_material_amounts))
    if cache_key in cache.keys():
        return cache[cache_key]

    max_number_of_geodes = last_material_amounts[len(last_material_amounts) - 1]

    # Rough attempt at skipping branches, we project an ideal scenario of geode robots being constantly generated and compare the result to the existing maximum
    global_max_number_of_geodes = max(cache.values() if len(cache.values()) > 0 else [-1])
    projected_geodes = max_number_of_geodes
    projected_geode_robots = last_robot_amounts[len(last_robot_amounts) - 1]
    for _ in range(minutes):
        projected_geodes += projected_geode_robots
        projected_geode_robots += 1
        if projected_geodes > global_max_number_of_geodes:
            break
    if projected_geodes <= global_max_number_of_geodes:
        cache[cache_key] = 0
        return 0

    if minutes > 0:
        # Keep going recursively after building each possible robot, trying to start with the most valuable one
        buildable_robots = []
        can_build_geode_robot = False
        for reverse_robot_index, robot_cost in enumerate(robot_costs[::-1]):
            robot_index = len(robot_costs) - reverse_robot_index - 1
            robot_amounts = list(last_robot_amounts)
            material_amounts = list(last_material_amounts)
            if robot_amounts[robot_index] < max_material_amounts[robot_index]:
                can_build_robot = True
                for material_amount_index in range(len(material_amounts)):
                    if material_amounts[material_amount_index] >= robot_cost[material_amount_index]:
                        material_amounts[material_amount_index] -= robot_cost[material_amount_index]
                    else:
                        material_amounts = list(last_material_amounts)
                        can_build_robot = False
                        break
                if can_build_robot:
                    # We only build the robot if it wasn't buildable and skipped before, as it would make no sense to wait unnecessarily before building it
                    if robot_index not in last_skipped_robots:
                        for index in range(len(robot_amounts)):
                            material_amounts[index] += robot_amounts[index]
                        robot_amounts[robot_index] += 1
                        can_build_geode_robot = robot_index == (len(robot_amounts) - 1)
                        max_number_of_geodes = max(max_number_of_geodes, calculate_max_number_of_geodes(blueprint_id, robot_amounts, material_amounts, robot_costs, max_material_amounts, minutes - 1, cache))
                    buildable_robots.append(robot_index)

        # Keep going recursively without building any robot, unless there was an option to build a geode robot, then we just do that
        if not can_build_geode_robot:
            robot_amounts = list(last_robot_amounts)
            material_amounts = list(last_material_amounts)
            for index in range(len(robot_amounts)):
                material_amounts[index] += robot_amounts[index]
            max_number_of_geodes = max(max_number_of_geodes, calculate_max_number_of_geodes(blueprint_id, robot_amounts, material_amounts, robot_costs, max_material_amounts, minutes - 1, cache, buildable_robots))

    cache[cache_key] = max_number_of_geodes
    return max_number_of_geodes

print("Part 1: " + str(execute(is_part_two = False)))
print("Part 2: " + str(execute(is_part_two = True)))