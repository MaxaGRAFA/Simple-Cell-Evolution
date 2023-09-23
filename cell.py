import random
import numpy as np
import vars
import pygame as p

# Dictionary with directions
directions = {
    0: (1, 0),
    1: (1, -1),
    2: (0, -1),
    3: (-1, 0),
    4: (-1, 1),
    5: (0, 1),
    6: (1, 1),
    7: (1, 0)
}

class Cell():
    def __init__(self, color, x, y, genome=np.full(64, 20)) -> None:

        self.direction = (1, 0)
        self.x = x
        self.y = y

        self.color = color
        self.genome = genome

        self.cell_size = vars.cell_size
        
        self.set_color = 0

        self.MaxNumGenomes = vars.MaxNumGenomes

        self.energy = 500
        self.age = 0

        self.num_childrens = 0

        self.max_energy = vars.MaxEnergy

        self.cell_alive = True

        # Genome counter. It indicates which genome command to execute.
        # When it reaches 42, it resets and ends the cell's turn.
        self.genomic_counter = 0
        
        # List of all commands
        self.command_map = {
            0: lambda: (self.direction_change(0), self.add_counter(3)),  # Change direction
            1: lambda: (self.direction_change(1), self.add_counter(3)),
            2: lambda: (self.direction_change(2), self.add_counter(3)),
            3: lambda: (self.direction_change(3), self.add_counter(3)),
            4: lambda: (self.direction_change(4), self.add_counter(3)),
            5: lambda: (self.direction_change(5), self.add_counter(3)),
            6: lambda: (self.direction_change(6), self.add_counter(3)),
            7: lambda: (self.direction_change(7), self.add_counter(3)),
            8: lambda: (self.add_counter(self.check(0))),  # Check what's in a certain direction (returns value to add)
            9: lambda: (self.add_counter(self.check(1))),
            10: lambda: (self.add_counter(self.check(2))),
            11: lambda: (self.add_counter(self.check(3))),
            12: lambda: (self.add_counter(self.check(4))),
            13: lambda: (self.add_counter(self.check(5))),
            14: lambda: (self.add_counter(self.check(6))),
            15: lambda: (self.add_counter(self.check(7))),
            16: lambda: (self.mutation(self.genome), self.add_counter(15)),  # Mutate its genome
            18: lambda: (self.add_counter(self.check_IsSurrounded_I())),  # Check if surrounded (returns value to add)
            20: lambda: (self.photosynthesis(), self.add_counter(35)),  # Perform photosynthesis
            23: lambda: (self.move(), self.add_counter(8)),  # Move one cell forward
            25: lambda: (self.eat_cell(), self.add_counter(20)),  # Eat the cell in front
            26: lambda: (self.move_relatively(), self.add_counter(10)),  # Move relative to the next genome value
            28: lambda: (self.food_transfer(), self.add_counter(15)),  # Transfer food to the cell in front
        }

        # Add itself to the list of cells
        vars.cells.append(self)

    # Function where the main actions take place
    def step(self):
        if self.cell_alive:
            # Display the cell
            self.set_cell()

            self.energy -= vars.MinusEnergyStep
            self.age += 1

            if self.energy <= 0 or self.energy > self.max_energy:
                self.die()
                return

            if self.energy >= 750:
                self.reproduce()

            # Loop through genome commands
            while True:
                # If the genome counter reaches the limit, reset it and pass control to the next cell
                if self.genomic_counter >= self.MaxNumGenomes:
                    self.genomic_counter = 0
                    break
                
                # Execute a command from the genome
                self.commands_genome()

    # Function that executes commands from the genome
    def commands_genome(self):
        genome = self.genome
        genomic_counter = self.genomic_counter

        # Select a genome using the genome counter
        selected_gen =  genome[genomic_counter]

        # Check if such a command exists
        if not selected_gen in self.command_map:
            self.genomic_counter += genome[genomic_counter]
        else:
            command = self.command_map[selected_gen]
            command()

    # Set the cell - display it on the screen
    def set_cell(self):
        # Check if there is a cell at the occupied coordinates
        if not (self.x, self.y) in vars.lock_coord:
            vars.lock_coord[(self.x, self.y)] = self

        top_left_x = self.x - self.cell_size // 2
        top_left_y = self.y - self.cell_size // 2

        if vars.show_screen == True:
            p.draw.rect(vars.screen, color=self.color, rect=(top_left_x, top_left_y, self.cell_size, self.cell_size))
            p.draw.rect(vars.screen, color="BLACK", rect=(top_left_x, top_left_y, self.cell_size, self.cell_size), width=1) 

    # Transfer food
    def food_transfer(self):
        if self.can_i_move() == True:
            new_x = self.x + self.direction[0] * self.cell_size
            new_y = self.y + self.direction[1] * self.cell_size

            new_coord = (new_x, new_y)

            # Check if such a cell exists
            if new_coord in vars.lock_coord:
                target_cell = vars.lock_coord[new_coord]
                target_cell.energy += 15
                self.energy -= 15

                return

    # Can it move forward?
    def can_i_move(self):
        new_x = self.x + self.direction[0] * self.cell_size
        new_y = self.y + self.direction[1] * self.cell_size

        if vars.borders[0] <= new_x <= vars.borders[2] and vars.borders[1] <= new_y <= vars.borders[3]:
            if (new_x, new_y) not in vars.lock_coord:
                # Cell can move to these coordinates
                return (new_x, new_y)
            else:
                # Cell cannot move due to another cell
                return 'cell'
        # Cannot move due to the border
        return 'border'

    # Move relative to the next genome value
    def move_relatively(self):
        del vars.lock_coord[(self.x, self.y)]

        if (self.genomic_counter + 1) >= self.MaxNumGenomes:
            number = 1
        else:
            number = self.genome[(self.genomic_counter + 1)]

        remainder = number % 7
        first_digit = int(str(remainder)[0])
         
        old_direct = self.direction
        self.direction_change(first_digit)

        can_i_move = self.can_i_move()
        if can_i_move != 'border' and can_i_move != 'cell':
            self.x = can_i_move[0]
            self.y = can_i_move[1]

        self.set_cell()
        
        self.direction = old_direct

    # Move one cell forward
    def move(self):
        del vars.lock_coord[(self.x, self.y)]

        can_i_move = self.can_i_move()

        if can_i_move != 'border' and can_i_move != 'cell':
            self.x = can_i_move[0]
            self.y = can_i_move[1]

        self.set_cell()
        
    # Reproduce
    def reproduce(self):
        if self.num_childrens >= 4:
            self.die() 
            return

        allow_directions = self.AllowDirections()

        if allow_directions != None:
            self.energy -= (110 * self.num_childrens)
            direct = np.random.choice(allow_directions)  # Choose a random direction from available directions for variety
            old_direct = self.direction
            self.direction_change(direct)
            mutated_gen = self.mutation(self.genome)
            new_cell = Cell(color=self.color, x=self.x, y=self.y, genome=mutated_gen)
            new_cell.energy = self.energy // 2
            self.energy = self.energy // 2
            self.move()
            self.direction = old_direct
            new_cell.direction_change(np.random.randint(0, 8))  # Random direction for the new cell
            new_cell.set_cell()
            self.num_childrens += 1
            return new_cell
        else:
            return

    # Eat the cell in front
    def eat_cell(self):
        if (self.genomic_counter + 1) >= self.MaxNumGenomes:
            number = 1
        else:
            number = self.genome[(self.genomic_counter + 1)]

        old_direct =self.direction

        remainder = number % 7
        first_digit = int(str(remainder)[0])
        self.direction_change(first_digit)

        if self.can_i_move() == 'cell':
            new_x = self.x + self.direction[0] * self.cell_size
            new_y = self.y + self.direction[1] * self.cell_size
            new_coord = (new_x, new_y)
            if new_coord in vars.lock_coord:
                target_cell = vars.lock_coord[new_coord]
                diffence = np.sum(np.not_equal(target_cell.genome, self.genome))
                if diffence >= 1 and self != target_cell:
                    energy_add = target_cell.energy // 3
                    target_cell.die()
                    self.energy += energy_add
                    self.get_red(energy_add)
            self.direction = old_direct
        else:
            self.direction = old_direct

    # Get available directions for the cell
    def AllowDirections(self):
        allow_directions = []
        old_direct = self.direction
        direct = 0
        while direct < 7:
            self.direction_change(direct)
            can_i_move = self.can_i_move()
            if not (can_i_move == 'border' or can_i_move == 'cell'):
                allow_directions.append(direct)
            direct += 1
        self.direction = old_direct
        if len(allow_directions) != 0:
            return allow_directions
        else:
            return None

    # Check if surrounded
    def check_IsSurrounded_I(self):
        value = 0
        if self.AllowDirections() == None:
            value += 3
        else:
            value += 2
        return value

    # Kill the cell
    def die(self):
        del vars.lock_coord[(self.x, self.y)]
        self.genomic_counter = self.MaxNumGenomes
        self.cell_alive = False

    # Check what's in a certain direction
    def check(self, direction):
        old_direction = self.direction
        self.direction_change(direction)
        can_i_move = self.can_i_move
        value = 0
        if can_i_move == 'cell':
            value += 3
        elif can_i_move == 'border':
            value += 2
        else:
            value += 1
        self.direction = old_direction
        return value

    # Check at which level the cell is
    def my_level(self):
        total_levels = 10
        min_y = vars.min_y
        max_y = vars.max_y
        interval = (max_y - min_y) / total_levels
        level = int((self.y - min_y) // interval) + 1
        if level > total_levels:
            level = total_levels - 1
        return level

    # Perform photosynthesis
    def photosynthesis(self):
        level = self.my_level()
        energy = level
        if level <= 4:
            energy -= level
        self.energy += energy - 1
        self.get_green(energy)

    # Make the color more red
    def get_red(self, amount):
        red = self.color[0]
        green = self.color[1]
        blue = self.color[2]
        amount = abs(amount)
        green -= amount
        if green < 0:
            green = 0
        red += amount
        if red >= 255:
            red = 255
        self.color = (red, green, blue)

    # Make the color more green
    def get_green(self, amount):
        red = self.color[0]
        green = self.color[1]
        blue = self.color[2]
        amount = abs(amount - 30)
        green += amount
        if green >= 255:
            green = 255
        red -= amount
        if red < 0:
            red = 0
        self.color = (red, green, blue)

    # Mutate the genome
    def mutation(self, genome):
        new_genome = genome.copy()
        if random.randint(0, 1) == 1:
            new_genome[random.randint(0, self.MaxNumGenomes - 1)] = random.randint(0, 30)
        return new_genome

    # Change its direction
    def direction_change(self, new_direct):
        self.direction = directions.get(new_direct, self.direction)

    # Add a value to the genome counter
    def add_counter(self, value):
        self.genomic_counter += value

    # Get current coordinates
    def get_coordinates(self):
        return self.x, self.y
    

