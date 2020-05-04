from pprint import pprint 

# this code makes a 9x9 grid filled with zeros for us to start the sudoku game

grid = []
for i in range(9):

    lock = []
    for j in range(9):
        lock.append(0)

    grid.append(lock)

pprint(grid)


