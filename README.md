# Simple Cell Evolution
Cell evolution using a genetic algorithm

This project represents the evolution of cells, where each cell can eat others or reproduce using a genetic algorithm. Here's what came out in the end:

<img src="https://github.com/MaxaGRAFA/Simple-Cell-Evolution/assets/89744777/041d733c-7d14-4799-a176-ac70a23310fa" width="500">
<img src="https://github.com/MaxaGRAFA/Simple-Cell-Evolution/assets/89744777/fff2d728-a91c-4d70-82bf-a7a8e75ad571" width="500">

## Basic rules

Each cell has its own energy, genome, color, and more. The genome is a list of size 64, containing numbers from 0 to 64. Each number represents a command, for example, 25 stands for photosynthesis. When a command is executed, a number is added to a special "counter". When the "counter" reaches 64, the cell finishes its turn.

When a cell's energy reaches 650, reproduction occurs. If there is space around, the cell divides, and one number in the genome mutates with a certain probability. 
However, when a cell has more than 5 children, it dies.

And in the lower field, a cell appears with a genome that performs only photosynthesis, but over time the cell mutates.

## How to start a simulation

You just need to run the 'main' file.

Also, the project uses the "numpy" and "pygame" libraries, which must be installed on you.


### Inspirers

The project was inspired by these videos: 

https://www.youtube.com/watch?v=PCx228KcOow&t=336s

https://www.youtube.com/watch?v=KLv0Z43ijyQ&t=258s

## License

This project is distributed under the MIT license.
