import input
import pygame
import time

SCREEN_COLUMNS = 40
SCREEN_ROWS = 6
COLUMN_SIZE = 23
ROW_SIZE = 20
INSTRUCTIONS = [(1, 0) if len(ins) == 1 else (2, int(ins[1])) for ins in input.read_lists(problem_number = 10)]
SCREEN = pygame.display.set_mode((SCREEN_COLUMNS * COLUMN_SIZE, SCREEN_ROWS * ROW_SIZE))

cells = []
instruction_index = 0

cicle = 0
x = 1

def simulate_screen():
    global instruction_index, x

    init()
    while True:
        # Execute the next instruction and draw the screen
        instruction = INSTRUCTIONS[instruction_index]
        for cicle_diff in range(instruction[0]):
            value = instruction[1] if cicle_diff == (instruction[0] - 1) else 0
            exit_if_needed()
            update(value)
            render()
            pygame.display.update()
            time.sleep(0.05)

        # Move the instruction pointer and reset everything if necessary
        instruction_index += 1
        if instruction_index >= len(INSTRUCTIONS):
            instruction_index = 0
            x = 1

def init():
    pygame.init()
    for _ in range(SCREEN_ROWS):
        cells.append([0] * SCREEN_COLUMNS)
    render()
    pygame.display.update()
    time.sleep(0.05)

def update(instruction_value):
    global x, cells, cicle
    
    # Execute instruction
    if abs(x - (cicle % SCREEN_COLUMNS)) <= 1:
        row = int(cicle / SCREEN_COLUMNS) % SCREEN_ROWS
        column = cicle % SCREEN_COLUMNS
        cells[row][column] = 255.0
    x += instruction_value

    # Make the previous cells fade away slightly
    for row in range(SCREEN_ROWS):
        for column in range(SCREEN_COLUMNS):
            cells[row][column] -= 0.75

    cicle += 1

def render():
    SCREEN.fill((0, 0, 0))

    # Draw X area
    pygame.draw.rect(
        SCREEN,
        (12, 15, 12),
        pygame.Rect((x - 1) * COLUMN_SIZE, 0, COLUMN_SIZE * 3, SCREEN_ROWS * ROW_SIZE),
    )

    # Draw cells
    for row in range(SCREEN_ROWS):
        for column in range(SCREEN_COLUMNS):
            strength = int(cells[row][column])
            if strength > 0:
                cell_color = (0, strength, 0)
                pygame.draw.rect(
                    SCREEN,
                    cell_color,
                    pygame.Rect(
                        column * COLUMN_SIZE,
                        row * ROW_SIZE,
                        COLUMN_SIZE,
                        ROW_SIZE,
                    ),
                )

    # Draw pulse cell
    pulse_color = (220, 255, 220) if abs((x % SCREEN_COLUMNS) - (cicle % SCREEN_COLUMNS)) <= 1 else (25, 120, 25)
    pygame.draw.rect(
        SCREEN,
        pulse_color,
        pygame.Rect(
            (cicle % SCREEN_COLUMNS) * COLUMN_SIZE,
            (int(cicle / SCREEN_COLUMNS) % SCREEN_ROWS) * ROW_SIZE,
            COLUMN_SIZE,
            ROW_SIZE,
        ),
    )

    # Draw lines in-between cells
    for column in range(1, SCREEN_COLUMNS):
        pygame.draw.line(SCREEN, (5, 25, 5), (column * COLUMN_SIZE, 0), (column * COLUMN_SIZE, SCREEN_ROWS * ROW_SIZE), 2)
    for row in range(1, SCREEN_ROWS):
        pygame.draw.line(SCREEN, (5, 25, 5), (0, row * ROW_SIZE), (SCREEN_COLUMNS * COLUMN_SIZE, row * ROW_SIZE), 2)

    # Draw X lines
    pygame.draw.line(SCREEN, (220, 255, 220), (((x - 1) * COLUMN_SIZE) - 1, 0), (((x - 1) * COLUMN_SIZE) - 1, SCREEN_ROWS * ROW_SIZE), 3)
    pygame.draw.line(SCREEN, (220, 255, 220), (((x + 2) * COLUMN_SIZE) - 1, 0), (((x + 2) * COLUMN_SIZE) - 1, SCREEN_ROWS * ROW_SIZE), 3)

def exit_if_needed():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

simulate_screen()