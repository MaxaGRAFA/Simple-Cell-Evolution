import pygame as p
import cell
import vars
import grid
import numpy as np

p.init()
p.display.set_caption("My Life")

clock = p.time.Clock()
screen = vars.screen

background = (255, 255, 255)
color_cell = (0, 255, 0)

genome_set = np.full(vars.MaxNumGenomes, 20)

grid_ = grid.Grid(cell_size=vars.cell_size, color='GRAY')

grid_x, grid_y = grid_.create_grid(rows=100, columns=80)

vars.min_y = grid_y[0]
vars.max_y = grid_y[-1]

cell1 = cell.Cell(color=color_cell, x=grid_x[10], y=grid_y[50], genome=np.full(vars.MaxNumGenomes, 20))
cell1.set_cell()

count_step = 0

running = True
while running:
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False

        if event.type == p.KEYDOWN:

            # Show the current step
            if event.key == p.K_2:
                print("Current step:" + str(count_step))
            # Toggle cell display on or off
            elif event.key == p.K_5:
                if vars.show_screen == False:
                    vars.show_screen = True
                else:
                    vars.show_screen = False

        if event.type == p.MOUSEBUTTONDOWN:

            if event.button == 1 or event.button == 3:
                x_mouse, y_mouse = event.pos
                x_near = min(grid_x, key=lambda x: abs(x - x_mouse))
                y_near = min(grid_y, key=lambda x: abs(x - y_mouse))

                # Set a cell with the selected genome
                if event.button == 3:
                    new_cell = cell.Cell(color=color_cell, x=x_near, y=y_near, genome=genome_set)
                    new_cell.set_cell()

                    # Reset the genome
                    genome_set = np.random.randint(low=0, high=45, size=(vars.MaxNumGenomes,))

                    break

                # Display information about the selected cell and copy its genome
                if event.button == 1:
                    for i in vars.cells:
                        if (i.get_coordinates()) == (x_near, y_near):
                            genome_set = i.genome

                            print("Energy:" + str(i.max_energy))
                            print('Age:' + str(i.age))
                            print('Genome:' + str(i.genome))

    clock.tick(100)
    screen.fill(background)
    screen.blit(vars.grid_surface, (0, 0))

    for i in vars.cells:
        i.step()
        if i.cell_alive == False:
            vars.cells_to_remove.append(i)

    # Remove dead cells
    for one_cell in vars.cells_to_remove:
        if one_cell in vars.cells:
            vars.cells.remove(one_cell)

    vars.cells_to_remove = []
    count_step += 1

    p.display.flip()
p.quit()