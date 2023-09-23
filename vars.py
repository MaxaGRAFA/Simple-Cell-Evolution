import pygame as p

window_size = 700
width = 700
height = 700
# Size of a cell on the canvas
cell_size = 7

# These values will change later
max_y = 0
min_y = 0

# Display mode.
mode = 0

# Cell step size (in pixels) and field boundaries. These values will change at startup
step_size = 0
borders = 0

# Maximum number of genes for one cell
MaxNumGenomes = 64

MinusEnergyStep = 5

MaxEnergy = 2500
show_screen = True

grid_surface = p.Surface((width + 400, height + 400))
grid_surface.set_colorkey((0, 0, 0))

screen = p.display.set_mode((window_size + 300, window_size + 80))

cells_to_remove = []

cells = []

# Occupied coordinates
lock_coord = {}
