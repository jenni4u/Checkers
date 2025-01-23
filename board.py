'''
Julien Yang, 2230490
Jennifer You, 2232773
Emy Xiao, 2231329
420-LCW-MS Programming Techniques
Friday, May 3
R.Vincent, instructor
Final Project
'''
'''Implementation of a checkers board, inspired by the reversi board implementation from Prog 101'''

#If a square has a 0 value, then it is empty. 1 represents the player and 2 represents the computer


def b_create(rows=8, cols=8):
    '''Create a matrix representation of a checkers board'''
    return [[0 for i in range(cols)] for x in range(rows)]

def b_rows(board):
    '''Return number of rows of the board'''
    return len(board)

def b_cols(board):
    '''Return number of columns of the board'''
    return len(board[0])

def b_eval(board, row, col):
    '''Returns value at a square'''
    if row > b_rows(board) or col > b_cols(board) or row<0 or col<0:
        raise ValueError('Impossible position')
    return board[row][col]

def b_copy(board):
    '''Returns a copy of the board)'''
    return [[x for x in row] for row in board]

def b_put(board,row,col,val):
    '''Changes the value at a square'''
    board[row][col] = val

def b_count(board,val):
    '''Returns the number of pieces of one player'''
    n = 0
    for row in board:
        for col in row:
            if col == val:
                n += 1
    return n
