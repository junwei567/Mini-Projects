puzzle = [
        [0, 0, 0, 2, 6, 0, 7, 0, 1],
        [6, 8, 0, 0, 7, 0, 0, 9, 0],
        [1, 9, 0, 0, 0, 4, 5, 0, 0],
        [8, 2, 0, 1, 0, 0, 0, 4, 0],
        [0, 0, 4, 6, 0, 2, 9, 0, 0],
        [0, 5, 0, 0, 0, 3, 0, 2, 8],
        [0, 0, 9, 3, 0, 0, 0, 7, 4],
        [0, 4, 0, 0, 5, 0, 0, 3, 6],
        [7, 0, 3, 0, 1, 8, 0, 0, 0]
    ]

def print_board(board):
    for i in range(len(board)): 
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")
# i = row, j = col
        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end = "")

            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ",end = "")

# zero represents empty spaces on the board
def find_zero(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)
    # when there is no more zero, sudoku is solved
    return None

def valid(board, inp, pos): # pos is a tuple, (i,j)
    # check through each entry in row to see if it is == inp
    for i in range(len(board[0])):
        if board[pos[0]][i] == inp and pos[1] != i:
            return False

    # check col
    for j in range(len(board)):
        if board[j][pos[1]] == inp and pos[0] != j:
            return False

    box_x = pos[1] // 3
    box_y = pos[0] // 3   

    for i in range(box_y * 3, box_y*3 + 3):
        for j in range(box_x*3, box_x * 3 + 3):
            if board[i][j] == inp and (i,j) != pos:
                return False

    return True # when passes all tests, must be valid  

def auto_solve(board):
    zero = find_zero(board)
    if not zero: # if not None
        return True
    else: # the zero here is a position in the form of a tuple (i,j)
        row, col = zero

    for i in range(1,10): # i will be our input, from 1 to 9
        if valid(board, i, (row,col)):
            board[row][col] = i

            if auto_solve(board):
                return True

            board[row][col] = 0

    return False


print_board(puzzle)
auto_solve(puzzle)
print("\nSolved\n")
print_board(puzzle)

