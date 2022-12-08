import input

PROBLEM_NUMBER = 8

def execute(is_part_two):
    trees = [list(map(int, list(line))) for line in input.read_lines(problem_number = PROBLEM_NUMBER)]
    return part_1(trees) if not is_part_two else part_2(trees)

def part_1(trees):
    num_visible = 0

    for row in range(len(trees)):
        for column, tree in enumerate(trees[row]):
            for increment_row, increment_column in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                is_visible = True
                next_row = row + increment_row
                next_column = column + increment_column
                while is_visible and next_row >= 0 and next_row < len(trees) and next_column >= 0 and next_column < len(trees[row]):
                    if trees[next_row][next_column] < tree:
                        next_row += increment_row
                        next_column += increment_column
                    else:
                        is_visible = False
                if is_visible:
                    num_visible += 1
                    break

    return num_visible

def part_2(trees):
    max_scenic_score = 0

    for row in range(len(trees)):
        for column, tree in enumerate(trees[row]):
            scenic_score = 1
            for increment_row, increment_column in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                visible_trees = 0
                next_row = row + increment_row
                next_column = column + increment_column
                while next_row >= 0 and next_row < len(trees) and next_column >= 0 and next_column < len(trees[row]):
                    visible_trees += 1
                    if trees[next_row][next_column] < tree:
                        next_row += increment_row
                        next_column += increment_column
                    else:
                        break
                scenic_score *= visible_trees
            max_scenic_score = max(scenic_score, max_scenic_score)

    return max_scenic_score


print("Part 1: " + str(execute(is_part_two = False)))
print("Part 2: " + str(execute(is_part_two = True)))