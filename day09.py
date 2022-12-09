import input

PROBLEM_NUMBER = 9
ADJACENT_COORDINATES = [
    (-1, -1), (-1,  0), (-1,  1),
    ( 0, -1), ( 0,  0), ( 0,  1),
    ( 1, -1), ( 1,  0), ( 1,  1),
]

def execute(is_part_two):
    return simulate_rope_moves(moves = read_moves(), rope_length = (2 if not is_part_two else 10))

def simulate_rope_moves(moves, rope_length):
    visited_by_tail = [(0, 0)]

    rope = [(0, 0)] * rope_length
    for row_increment, column_increment in moves:
        for head_index in range(len(rope) - 1):
            # Each pair of points in the rope is considered its own two-length rope
            head = rope[head_index]
            tail = rope[head_index + 1]

            # We only move the head point as instructed if it is the actual head of the whole rope,
            # otherwise the move on this point will have already happend as a consequence of having
            # all the rope points follow the actual head, which will be leading the rope motions
            if head_index == 0:
                head = (head[0] + row_increment, head[1] + column_increment)
                rope[head_index] = head

            # Find the valid tail positions and move the tail appropriately if it is not in one of them
            valid_tail_positions = [(head[0] + adj_row, head[1] + adj_column) for adj_row, adj_column in ADJACENT_COORDINATES]
            while tail not in valid_tail_positions:
                row_diff = head[0] - tail[0]
                column_diff = head[1] - tail[1]
                tail = (
                    tail[0] + (min(1, row_diff) if row_diff >= 0 else max(-1, row_diff)),
                    tail[1] + (min(1, column_diff) if column_diff >= 0 else max(-1, column_diff)),
                )
                rope[head_index + 1] = tail

                # We only count the visit if this tail point is actually the tail of the whole rope
                if (head_index + 2) == len(rope) and tail not in visited_by_tail:
                    visited_by_tail.append(tail)

    return len(visited_by_tail)

def read_moves():
    moves = []

    instructions = [(direction, int(steps)) for direction, steps in input.read_lists(problem_number = PROBLEM_NUMBER)]
    for direction, steps in instructions:
        if direction == 'L': moves.extend((0, -1) for _ in range(steps))
        elif direction == 'U': moves.extend((-1, 0) for _ in range(steps))
        elif direction == 'R': moves.extend((0, 1) for _ in range(steps))
        elif direction == 'D': moves.extend((1, 0) for _ in range(steps))

    return moves

print("Part 1: " + str(execute(is_part_two = False)))
print("Part 2: " + str(execute(is_part_two = True)))