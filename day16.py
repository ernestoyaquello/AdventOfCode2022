import input
import re

PROBLEM_NUMBER = 16
INPUT_PATTERN = re.compile(r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? ((?:\w+(?:, )?)+)")

cache = {}

def execute(is_part_two):
    global cache
    cache = {}

    valves = {match.group(1): {'label': match.group(1), 'flow_rate': int(match.group(2)), 'connections': match.group(3).split(', '), 'open': False} for line in input.read_lines(PROBLEM_NUMBER) for match in INPUT_PATTERN.finditer(line)}
    for valve in valves.values():
        valve['connections'] = sorted(valve['connections'], key = lambda c: valves[c]['flow_rate'], reverse = True)

    return calculcate_max_total_release(valves, ['AA'] if not is_part_two else ['AA', 'AA'], 30 if not is_part_two else 26)

def calculcate_max_total_release(valves, labels, max_minutes, turn = 0, previous_total_release = 0, previous_minutes = 0, previous_rate = 0, previous_rate_tmp = None, maxx = [0]):
    global cache

    total_release = 0

    cache_key = (turn, ",".join(labels), ",".join(map(lambda v: v['label'], filter(lambda v: v['flow_rate'] > 0 and v['open'], valves.values()))), previous_minutes)
    if cache_key in cache.keys():
        return cache[cache_key]

    # Absolutely horrendous pruning that simulates an ideal scenario going forward to compare the result with the current maximum.
    # It makes almost no sense and it has been given close to zero thought, but it *kinda* works... ¯\_(ツ)_/¯
    simulate_total_release = previous_total_release
    simulate_minutes = previous_minutes
    simulate_rate = previous_rate
    for valve_to_open in sorted(filter(lambda v: v['flow_rate'] > 0 and not v['open'], valves.values()), key = lambda v: v['flow_rate'], reverse = True):
        simulate_rate += valves[valve_to_open['label']]['flow_rate']
        simulate_extra_minutes = min(2, max_minutes - simulate_minutes)
        simulate_minutes += simulate_extra_minutes
        simulate_total_release += simulate_rate * simulate_extra_minutes
        if simulate_minutes >= max_minutes:
            break
    simulate_total_release += simulate_rate * (max_minutes - simulate_minutes)
    if simulate_total_release < maxx[0]:
        return 0

    # If able, perform action (either valve opening or move) and then continue performing actions with recursion
    if previous_minutes < max_minutes:
        next_total_release = previous_rate if previous_rate_tmp == None else previous_rate_tmp
        next_minutes = previous_minutes + (1 if turn == (len(labels) - 1) else 0)
        next_rate_tmp = 0 if turn == 0 and len(labels) > 1 else None
        next_turn = (turn + 1) % len(labels)

        label = labels[turn]
        max_total_release = 0
        labels_to_visit = [label] + valves[label]['connections']
        for label_to_visit in labels_to_visit:
            open_state_backup = valves[label]['open']

            next_rate = previous_rate
            if label_to_visit == label:
                if valves[label]['flow_rate'] > 0 and not valves[label]['open']:
                    valves[label]['open'] = True
                    next_rate += valves[label]['flow_rate']
                else:
                    continue

            next_labels = list(labels)
            next_labels[turn] = label_to_visit
            max_total_release = max(max_total_release, next_total_release + calculcate_max_total_release(valves, next_labels, max_minutes, next_turn, previous_total_release + next_total_release, next_minutes, next_rate, next_rate_tmp, maxx))
            maxx[0] = max(maxx[0], max_total_release)

            valves[label]['open'] = open_state_backup
        total_release = max_total_release

    cache[cache_key] = total_release
    return total_release

print("Part 1: " + str(execute(is_part_two = False)))
print("Part 2: " + str(execute(is_part_two = True)))