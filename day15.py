import input
import re
import sys
from collections import defaultdict

PROBLEM_NUMBER = 15
INPUT_PATTERN = re.compile(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")

def execute(is_part_two):
    data = read_data()
    return part_1(data, 2000000) if not is_part_two else part_2(data)

def part_1(data, y):
    num_positions_without_beacon = 0

    x = data['ltrb'][0]
    while x <= data['ltrb'][2]:
        for sensor in data['sensors']:
            diff_x = abs(x - sensor['position'][0])
            diff_y = abs(y - sensor['position'][1])
            distance_to_sensor = diff_x + diff_y
            if distance_to_sensor <= sensor['radius']:
                increment = ((sensor['position'][0] - x) + sensor['radius']) - diff_y
                num_positions_without_beacon += increment + 1
                x += increment
                break
        x += 1

    for beacon in data['beacons']:
        num_positions_without_beacon -= 1 if beacon[1] == y else 0

    return num_positions_without_beacon

def part_2(data):
    for x in range(0, 4000000 + 1):
        y = 0
        while y <= 4000000:
            candidate = (x ,y)
            for sensor in data['sensors']:
                diff_x = abs(x - sensor['position'][0])
                diff_y = abs(y - sensor['position'][1])
                distance_to_sensor = diff_x + diff_y
                if distance_to_sensor <= sensor['radius']:
                    y += ((sensor['position'][1] - y) + sensor['radius']) - diff_x
                    candidate = None
                    break
            if candidate != None:
                return (x * 4000000) + y
            y += 1

    return 0

def read_data():
    data = {
        'beacons': set(),
        'sensors': [{'position': (int(match.group(1)), int(match.group(2))), 'closest_beacon': (int(match.group(3)), int(match.group(4)))} for line in input.read_lines(PROBLEM_NUMBER) for match in INPUT_PATTERN.finditer(line)],
        'ltrb': (sys.maxsize, sys.maxsize, -sys.maxsize - 1, -sys.maxsize - 1),
    }

    for sensor in data['sensors']:
        sensor['radius'] = abs(sensor['closest_beacon'][0] - sensor['position'][0]) + abs(sensor['closest_beacon'][1] - sensor['position'][1])
        data['beacons'].add(sensor['closest_beacon'])
        data['ltrb'] = (
            min(data['ltrb'][0], sensor['position'][0] - sensor['radius']),
            min(data['ltrb'][1], sensor['position'][1] - sensor['radius']),
            max(data['ltrb'][2], sensor['position'][0] + sensor['radius']),
            max(data['ltrb'][3], sensor['position'][1] + sensor['radius']),
        )

    return data

print("Part 1: " + str(execute(is_part_two = False)))
print("Part 2: " + str(execute(is_part_two = True)))