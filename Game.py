import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Grid dimensions
n_cells_x, n_cells_y = 40, 30
cell_width = width // n_cells_x
cell_height = height // n_cells_y

# Game state
game_state = np.random.choice([0, 1], size=(n_cells_x, n_cells_y), p=[0.8, 0.2])

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
green = (0, 255, 0)

# Button dimensions
button_width, button_height = 200, 50
button_spacing = 10
next_button_x, next_button_y = (width - button_width) // 2, height - button_height - 10
save_button_x, save_button_y = next_button_x - button_width - button_spacing, next_button_y
load_button_x, load_button_y = next_button_x + button_width + button_spacing, next_button_y
pause_button_x, pause_button_y = next_button_x, next_button_y - button_height - button_spacing

# Simulation parameters
tick_interval = 1  # in seconds
is_paused = False
last_update_time = 0

def draw_button(x, y, label):
    pygame.draw.rect(screen, green, (x, y, button_width, button_height))
    font = pygame.font.Font(None, 36)
    text = font.render(label, True, black)
    text_rect = text.get_rect(center=(x + button_width // 2, y + button_height // 2))
    screen.blit(text, text_rect)

def draw_grid():
    for y in range(0, height, cell_height):
        for x in range(0, width, cell_width):
            cell = pygame.Rect(x, y, cell_width, cell_height)
            pygame.draw.rect(screen, gray, cell, 1)

def next_generation():
    global game_state
    new_state = np.copy(game_state)

    for y in range(n_cells_y):
        for x in range(n_cells_x):
            n_neighbors = game_state[(x - 1) % n_cells_x, (y - 1) % n_cells_y] + \
                          game_state[(x)     % n_cells_x, (y - 1) % n_cells_y] + \
                          game_state[(x + 1) % n_cells_x, (y - 1) % n_cells_y] + \
                          game_state[(x - 1) % n_cells_x, (y)     % n_cells_y] + \
                          game_state[(x + 1) % n_cells_x, (y)     % n_cells_y] + \
                          game_state[(x - 1) % n_cells_x, (y + 1) % n_cells_y] + \
                          game_state[(x)     % n_cells_x, (y + 1) % n_cells_y] + \
                          game_state[(x + 1) % n_cells_x, (y + 1) % n_cells_y]

            if game_state[x, y] == 1 and (n_neighbors < 2 or n_neighbors > 3):
                new_state[x, y] = 0
            elif game_state[x, y] == 0 and n_neighbors == 3:
                new_state[x, y] = 1

    game_state = new_state

def draw_cells():
    for y in range(n_cells_y):
        for x in range(n_cells_x):
            cell = pygame.Rect(x * cell_width, y * cell_height, cell_width, cell_height)
            if game_state[x, y] == 1:
                pygame.draw.rect(screen, black, cell)

def pause_resume_simulation():
    global is_paused
    is_paused = not is_paused

def save_simulation():
    np.save("save.npy", game_state)

def load_simulation():
    global game_state
    try:
        game_state = np.load("save.npy")
    except FileNotFoundError:
        print("Save file not found.")

running = True
while running:
    screen.fill(white)
    draw_grid()
    draw_cells()
    draw_button(next_button_x, next_button_y, "Next Generation")
    draw_button(save_button_x, save_button_y, "Save")
    draw_button(load_button_x, load_button_y, "Load")
    draw_button(pause_button_x, pause_button_y, "Pause/Resume")
    pygame.display.flip()

    current_time = pygame.time.get_ticks() // 1000  # Convert milliseconds to seconds
    if not is_paused and current_time - last_update_time >= tick_interval:
        next_generation()
        last_update_time = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if next_button_x <= event.pos[0] <= next_button_x + button_width and next_button_y <= event.pos[1] <= next_button_y + button_height:
                next_generation()
            elif save_button_x <= event.pos[0] <= save_button_x + button_width and save_button_y <= event.pos[1] <= save_button_y + button_height:
                save_simulation()
            elif load_button_x <= event.pos[0] <= load_button_x + button_width and load_button_y <= event.pos[1] <= load_button_y + button_height:
                load_simulation()
            elif pause_button_x <= event.pos[0] <= pause_button_x + button_width and pause_button_y <= event.pos[1] <= pause_button_y + button_height:
                pause_resume_simulation()
            else:
                x, y = event.pos[0] // cell_width, event.pos[1] // cell_height
                game_state[x, y] = not game_state[x, y]

pygame.quit()
