'''
Julien Yang, 2230490
Jennifer You, 2232773
Emy Xiao, 2231329
420-LCW-MS Programming Techniques
Friday, May 3
R.Vincent, instructor
Final Project
'''

import tkinter as tk
from board import *
from checker_game import *
from checker_game import _isking

# colours
P1_PIECES = '#664229'		# brown
P2_PIECES = '#D2B48C'		# blonde
LIGHT_SQUARE = '#E5D3B3'	# light beige
DARK_SQUARE = '#987554'		# light brown
P1_KING = 'black'
P2_KING = 'red'
CORRECT = 'green'
BACKGROUND = LIGHT_SQUARE

# boards
DARK_SQUARE_MATRIX = [[0]*4]*8  # matrix representing only dark, playable, squares
DARK_SQUARES = []   # list of object ids of dark squares               
CURRENT = []        # current board in play

# pieces
PLAYER1 = []        # list of object ids of human player pieces

# game
LEGAL_MOVES = []    # list of possible moves (square) for selected square
CHOICES = []        # list of square ids that are possible moves
H_PAWN = (0, 1)     # coordinates of current selected square in (row, col) of matrix
H_MOVE = (0, 0)     # coordinates of selected move in (row, col) of matrix
LEVEL = 1           # level of difficulty

# double jump
JUMP_MOVES = []     # list of possible moves for jumper pawn after a capture
PAWN = 0            # coordinates of jumper pawn in (row, col)

# sizes
SQUARE_SIZE = 80	            # square size
BOARD_SIZE = SQUARE_SIZE * 8	# board size

# create tkinter window
root = tk.Tk()



# create canvas
canvas = tk.Canvas(root,
                    width = BOARD_SIZE,
                    height = BOARD_SIZE,
                    bg = BACKGROUND)
canvas.pack()

def row_col(object):
    '''Find coordinates (row, col) of an object from a given ID.'''
    # find top left corner coordinates of object
    x, y, x1, y1 = canvas.coords(object)

    # compute row and column by counting amount of squares in-between top left corner of the board and top left corner of object
    row = int(y/SQUARE_SIZE)
    col = int(x/SQUARE_SIZE)

    return row, col

def find_square(row, col):
    '''Find ID of dark square in given (row, col) coordinates of matrix.'''      
    # compute x and y coordinates of given square, add 1 pixel to each to be inside of the actual square
    y = row * SQUARE_SIZE+1
    x = col * SQUARE_SIZE+1

    # find objects under those coordinates            
    under = canvas.find_overlapping(x, y, x, y)

    return under[0] # squares come first in returned list of items, since they have smaller ID from being created first

def set_board(board):
    '''Set a board from a matrix of pieces' positions.'''
    
    global CURRENT, PLAYER1, DARK_SQUARES, LEVEL

    # clear 
    for l in [PLAYER1, DARK_SQUARES]:
        l.clear()
    canvas.delete('all')
    # create dark squares on the board
    i = 0	# row index
    y = 0
    for row in DARK_SQUARE_MATRIX:
        if i%2 == 0:
            x = SQUARE_SIZE
        else:
            x = 0
        for sq in row:                
            x1 = x + SQUARE_SIZE + 1
            y1 = y + SQUARE_SIZE + 1
            r = canvas.create_rectangle(x,y,x1,y1, width = 0,
                                        fill = DARK_SQUARE)
            DARK_SQUARES.append(r)
            x += 2*SQUARE_SIZE
        i += 1
        y += SQUARE_SIZE

    # place all the pieces on the board
    i = 0	# row index        
    y = 0        
    for row in board:
        x = 0
        y1 = y + SQUARE_SIZE 
        for sq in row:
            x1 = x + SQUARE_SIZE                       
            if sq:
                if sq == 1:
                    color = P1_PIECES
                    player = 1
                elif sq == 2:
                    color = P2_PIECES
                    player = 0
                elif sq == 3:
                    color = P1_KING
                    player = 1
                elif sq == 4:
                    color = P2_KING
                    player = 0
                p = canvas.create_oval(x,y,x1,y1, width = 0,
                                        fill = color)
                if player:
                    PLAYER1.append(p)
            x += SQUARE_SIZE
        i += 1
        y += SQUARE_SIZE 
    CURRENT = board
    print("jen's board")
    for row in board:
        print(row)
    print(LEVEL)
    print("------------------------")


    if game_over(CURRENT):
        root.quit()
        if game_over(CURRENT) == 1:
            print("You won!")
        else:
            print("You lost!")

def see_board(board):	# used to debug and run tests
    '''Display a board corresponding to the given board matrix.'''
    b = tk.Tk()
    can = tk.Canvas(b,
                    width = BOARD_SIZE,
                    height = BOARD_SIZE,
                    bg = BACKGROUND)

    can.pack()
    
    i = 0	# row index
    y = 0
    for row in DARK_SQUARE_MATRIX:
        if i%2 == 0:
            x = SQUARE_SIZE
        else:
            x = 0
        for sq in row:                
            x1 = x + SQUARE_SIZE + 1
            y1 = y + SQUARE_SIZE + 1
            r = can.create_rectangle(x,y,x1,y1, width = 0,
                                        fill = DARK_SQUARE)
            DARK_SQUARES.append(r)
            x += 2*SQUARE_SIZE
        i += 1
        y += SQUARE_SIZE

    i = 0	# row index        
    y = 0        
    for row in board:
        x = 0
        y1 = y + SQUARE_SIZE 
        for sq in row:
            x1 = x + SQUARE_SIZE                       
            if sq:
                if sq == 1:
                    color = P1_PIECES
                    player = 1
                elif sq == 2:
                    color = P2_PIECES
                    player = 0
                elif sq == 3:
                    player = 1
                    color = P1_KING
                elif sq == 4:
                    player = 2
                    color = P2_KING
                can.create_oval(x,y,x1,y1, width = 0,
                                             fill = color)

            x += SQUARE_SIZE
        i += 1
        y += SQUARE_SIZE
    b.mainloop()

def new_game():
    '''Set a new game board ready to play.'''
    set_board(game_start())
    
def on_click(event):
    '''Handles a left click from the mouse.'''
    global H_PAWN, H_MOVE, LEGAL_MOVES, CHOICES, CURRENT, JUMP_MOVES, PAWN, LEVEL
    
    # find [dark square, piece] clicked on
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    under = canvas.find_overlapping(x, y, x, y)

    # nothing clicked on
    if not under:
        return
    
    # assign clicked square
    square = under[0]
    
   
    if len(under) == 2 and under[1] in PLAYER1:
        # reset CORRECT squares to DARK_SQUARE color
        canvas.itemconfigure(find_square(H_PAWN[0], H_PAWN[1]), fill = DARK_SQUARE)
        for s in CHOICES:
            canvas.itemconfigure(s, fill = DARK_SQUARE)

        CHOICES.clear()
        canvas.itemconfigure(square, fill = CORRECT)

        H_PAWN = row_col(square) 
        if _isking(CURRENT,H_PAWN[0],H_PAWN[1],1):
            H_PAWN = (H_PAWN[0],H_PAWN[1],0)
        
        LEGAL_MOVES = legal_moves(CURRENT, 1)[H_PAWN]
        if JUMP_MOVES and H_PAWN == PAWN:
            LEGAL_MOVES = JUMP_MOVES.copy()
    
            for row, col, jump in JUMP_MOVES:
                s = find_square(row, col)
                CHOICES.append(s)
                canvas.itemconfigure(s, fill = CORRECT)
        elif not JUMP_MOVES:
            for square in LEGAL_MOVES:
                square = find_square(square[0], square[1])
                CHOICES.append(square)
                canvas.itemconfigure(square, fill = CORRECT)
        
        
    elif len(under) == 1 and square in CHOICES:
        JUMP_MOVES = 0
        H_MOVE = row_col(square)
        for move in LEGAL_MOVES:
            if move[0] == H_MOVE[0] and move[1] == H_MOVE[1]:
                H_MOVE = move
        JUMP_MOVES = game_turn(CURRENT, H_PAWN, H_MOVE, LEVEL)
        PAWN = H_MOVE[:-1]

        set_board(CURRENT)

def level_easy():
    '''Set level of difficulty to easy.'''
    global LEVEL
    LEVEL = 1 
def level_medium():
    '''Set level of difficulty to medium.'''
    global LEVEL
    LEVEL = 2 
def level_hard():
    '''Set level of difficulty to hard.'''
    global LEVEL
    LEVEL = 3
        
# create menu
menubar = tk.Menu(root)
gamemenu = tk.Menu(menubar, tearoff = 0)
gamemenu.add_command(label = 'New Game', command = new_game)
gamemenu.add_command(label = 'Quit', command = root.quit)
menubar.add_cascade(label="Game", menu=gamemenu)

levelmenu = tk.Menu(menubar, tearoff = 0)
levelmenu.add_command(label = 'Easy', command = level_easy)
levelmenu.add_command(label = 'Medium', command = level_medium)
levelmenu.add_command(label = 'Hard', command = level_hard)
menubar.add_cascade(label="Level", menu=levelmenu)

    

    
        

canvas.bind('<Button-1>', on_click)
root.config(menu=menubar)
new_game()

root.mainloop()
