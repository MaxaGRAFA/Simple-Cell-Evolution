import pygame as p
import vars

class Grid():
    def __init__(self, cell_size, color) -> None:
        self.cell_size = cell_size
        self.color = color
        
        # Store the coordinates of the center of each cell here
        self.grid_x = []
        self.grid_y = []

        self.cell_size = vars.cell_size
    
    def create_grid(self, rows, columns):

        margin = 25

        for column in range(columns):
            for row in range(rows):
                x = margin + row * self.cell_size 
                y = margin + column * self.cell_size 
                
                top_left_x = x - self.cell_size // 2
                top_left_y = y - self.cell_size // 2

                # Check for a similar element in the list
                if x not in self.grid_x: 
                    self.grid_x.append(x)
                if y not in self.grid_y: 
                    self.grid_y.append(y)
                
                p.draw.rect(vars.grid_surface, color=self.color, rect=(top_left_x, top_left_y, self.cell_size, self.cell_size), width=1)
        
        # Determine the grid boundaries
        vars.borders = (self.grid_x[0], self.grid_y[0], self.grid_x[-1], self.grid_y[-1])

        return self.grid_x, self.grid_y
    
