import input
import re

PROBLEM_NUMBER = 7

def execute(is_part_two):
    content = read_content()
    return part_1(content) if not is_part_two else part_2(content)

def part_1(content):
    valid_directories = find_valid_directories(content, max_size = 100000)
    return sum(valid_dir['size'] for valid_dir in valid_directories)

def part_2(content):
    space_to_free = 30000000 - (70000000 - content['size'])
    valid_directories = find_valid_directories(content, min_size = space_to_free)
    return min(dir['size'] for dir in valid_directories)

def find_valid_directories(content, min_size = -1, max_size = -1):
    valid_directories = []

    for inner_content in content['content']:
        if inner_content['content'] != None:
            if (min_size == -1 or inner_content['size'] >= min_size) and (max_size == -1 or inner_content['size'] <= max_size):
                valid_directories.append(inner_content)
            valid_directories = valid_directories + find_valid_directories(inner_content, min_size, max_size)

    return valid_directories

def read_content():
    content = { 'name': '/', 'content': [], 'size': -1, 'parent': None }

    content_current = content
    for line in input.read_lists(problem_number = PROBLEM_NUMBER)[1:]:
        if line[0] == "$":
            if line[1] == "cd":
                if line[2] != "..":
                    # Enter directory line[2]
                    content_current = next(c for c in content_current['content'] if c['name'] == line[2])
                else:
                    # Move up to parent directory
                    content_current = content_current['parent']
        elif line[0] != 'ls':
            size = int(line[0]) if line[0].isnumeric() else -1
            new_content = { 'name': line[1], 'content': [] if size == -1 else None, 'size': size, 'parent': content_current }
            if new_content not in content_current['content']:
                # Add new content and increase all parents' size iteratively if able
                content_current['content'].append(new_content)
                if new_content['size'] >= 0:
                    content_parent = new_content['parent']
                    while content_parent != None:
                        content_parent['size'] += new_content['size'] if content_parent['size'] >= 0 else (new_content['size'] + 1)
                        content_parent = content_parent['parent']

    return content

print("Part 1: " + str(execute(is_part_two = False)))
print("Part 2: " + str(execute(is_part_two = True)))