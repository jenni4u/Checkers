'''
Julien Yang, 2230490
Jennifer You, 2232773
Emy Xiao, 2231329
420-LCW-MS Programming Techniques
Friday, May 3
R.Vincent, instructor
Final Project
'''

'''Checkers implementation using board from checker_board.py and represented using the UI in checker_ui.py'''
from random import randint
from board import *

HUMAN = 1
COMPUTER = 2
H_KING = 3
C_KING = 4
H_CAPTURE = False
h_capt_moves = []
def game_start(): #DONE
    '''Initialize board and positions'''
    #Create an 8x8 board
    board = b_create()

    #Initialize piece positions
    for row in range(0,3,2):
        for col in range(1,len(board[row]),2):
            b_put(board,row,col, COMPUTER)
    for col in range(0,len(board[row]),2):
        b_put(board,1,col,COMPUTER)

    for row in range(0,3,2):
        for col in range(0,len(board[row]),2):
            b_put(board,-row-1,col, HUMAN)
    for col in range(1,len(board[row]),2):
        b_put(board,6,col,HUMAN)

    return board

def game_turn(board, h_pawn, h_move):
    '''Run a turn of the game, with the human move already chosen
    h_pawn = tuple(int,int)
    h_move = tuple(int,int)
    '''
    global H_CAPTURE, h_capt_moves
    if H_CAPTURE:
        print(h_capt_moves)
    
    #Check if it is a capture move
    capture_h = True #Initialization
    while capture_h:

        capture_h = False
        #Check for capture

        if len(h_move) == 3:
            
            jumped_row, jumped_col = h_move[2]
            board[jumped_row][jumped_col] = 0
            h_move = h_move[:2]
            capture_h = True
        

        #Move piece from original pawn position to final position
        board[h_pawn[0]][h_pawn[1]] = 0
        if len(h_pawn) == 3:
            board[h_move[0]][h_move[1]] = H_KING
        else:
            board[h_move[0]][h_move[1]] = HUMAN
            #Upgrade pawn into king if it reached the final row
            if _isking(board,h_move[0],h_move[1],HUMAN):
                board[h_move[0]][h_move[1]] = H_KING
        
        
        #If it was a capture, human turn again
        while capture_h:
            capture_h = False
            moved_pawn = (h_move[0],h_move[1])
            moved_moves = legal_moves(board,HUMAN).get(moved_pawn, -1)
 
            if moved_moves == -1:
                break
            capt_moves = [move if len(move) == 3 else None for move in moved_moves]

            for move in capt_moves:
                if move:
                    h_capt_moves.append(move) #GLOBAL
                    capture_h = True
                    H_CAPTURE = True

            if capture_h:
                return h_capt_moves
            else:
                break

        

                  
    
    #Choose computer move
    
    capture_c = True #initialization
    chosen_move = False #For if it takes
    while capture_c:
      if chosen_move:
          capture_c = False
      if game_over(board):
          return
      if not chosen_move: #If the move is not a second capture move, choose using algorithm
          computer_moves = legal_moves(board,COMPUTER)
          #Function here can be changed to choose the algorithm to choose move
          c_pawn, c_move = _choose_move_random(board, computer_moves, COMPUTER)
          print(c_pawn, c_move)
          if c_pawn == -1:
              return
      
      #Check if chosen move is a capture
      if len(c_move) == 3:
          jumped_row, jumped_col = c_move[2]
          board[jumped_row][jumped_col] = 0
          capture_c = True #Will be computer turn again if it is a capture

      #Move chosen computer piece
      board[c_pawn[0]][c_pawn[1]] = 0
      if len(c_pawn) == 3:
          board[c_move[0]][c_move[1]] = C_KING
      else:
          board[c_move[0]][c_move[1]] = COMPUTER
          print("julien's board")
          for row in board:
              print(row)
          print('------------------------')
          #Upgrade pawn into king if it reached the final row
          if _isking(board, c_move[0], c_move[1], COMPUTER):
              board[c_move[0]][c_move[1]] = C_KING
              
      #If it was a capture, computer turn again
      while capture_c:
            chosen_move = False
            capture_c = False
            moved_pawn = c_move[:2]
            moved_moves = legal_moves(board,COMPUTER).get(moved_pawn, -1)

            if moved_moves == -1:
                break
            capt_moves = [move if len(move) == 3 else None for move in moved_moves]

            for move in capt_moves:
                if move:
                    c_pawn = moved_pawn
                    c_move = move
                    capture_c = True
                    chosen_move = True

                    
            if chosen_move:
                break
     
def _choose_move_random(board,moves,player):
    '''Choose a move for the computer depending on RANDOM or BST or GREED or RECURSION
    Should return a tuple consisting of the initial position of a piece and the final
    position of a piece: tuple(tuple(int,int),tuple(int,int))'''
    #find a dict of all the pieces that have moves
    dict_moves = {}
    #find a list of all the keys
    ls_keys = []
    for piece, pack in moves.items():
        if len(pack):
            dict_moves[piece] = pack
            ls_keys.append(piece)
    #choose a random key
    if len(ls_keys) == 1:
      random = 0
    elif len(ls_keys) == 0:
        return -1,-1
    else:
      random = randint(0,len(ls_keys)-1)
    initial = ls_keys[random]
    nb_moves = len(dict_moves[initial])
    nb = randint(0,nb_moves-1)
    return initial, dict_moves[initial][nb]

def _choose_move_greed(board,moves,player):
    '''GREED'''
    
    for pawn, captures in moves.items():
        for move in captures:
            if len(move) == 3:
                return pawn, move
    return _choose_move_random(board, moves, player)

def _choose_move_recursion(board,moves,player, depth = 2):
    '''RECURSION'''
    y = [True if x==[] else False for x in moves.values()] #If no more moves, return -1,-1
    if all(y):
        return -1,-1
    if player == COMPUTER: #Find opponent
        opp = HUMAN
    else:
        opp = COMPUTER

    if depth == 0: #BASE CASE - use greedy algorithm

        return _choose_move_greed(board,moves,player)

    else:
        #iterate over all possible moves
        #value system
        value_dict = {}

        for pawn,pawn_moves in moves.items():
            for potential_move in pawn_moves:
                value = 0 #Value of this move
                temp_board = b_copy(board) #Make a copy board so that we don't affect the actual game
                
                #Check for captures
                if len(potential_move) == 3:
                    jumped_row, jumped_col = potential_move[2]
                    temp_board[jumped_row][jumped_col] = 0
                    value +=2

                # Move piece from original pawn position to final position
                temp_board[pawn[0]][pawn[1]] = 0
                if len(pawn) == 3:
                    temp_board[potential_move[0]][potential_move[1]] = player+2
                else:
                    temp_board[potential_move[0]][potential_move[1]] = player

                # Upgrade pawn into king if it reached the final row
                if _isking(board, potential_move[0], potential_move[1], player):
                    board[potential_move[0]][potential_move[1]] = player+2

                #Check next opponent move
                next_pawn, next_move = _choose_move_recursion(temp_board,legal_moves(temp_board,opp),opp, depth-1)
                
                #If opponent has no more moves, choose that move
                if next_pawn == -1:
                    return pawn,potential_move
                if len(next_move) != 3:
                    value+=1

                value_dict[value] = (pawn,potential_move)
        for val in range(4,-1,-1):
            if value_dict.get(val,0):
                return value_dict[val][0], value_dict[val][1]
                #Check if the next move is a capture and if your move is a capture


def _isking(board,row, col, val): #DONE
    '''Returns True if the pawn at the position should become a king'''
    if board[row][col] == val+2:
        return True
    if val == HUMAN and row == 0 and board[row][col] == 1:
        return True
    elif val == COMPUTER and row == 7 and board[row][col] == 2:
        return True
    else:
        return False

def player_turn(board): #Not used when UI is implemented. Only used for debugging
    '''Asks the human for a move and checks if the move is legal'''
    while True:
        #user_pawn = input('Which piece do you want to play?').split(',') #also will be inputted from UI
        #user_move = input('What move do you want to play?').split(',') #only for test, will be input from UI
        #input should be comma separated row,col
        #if len(user_pawn) == 3:
        #  user_pawn = (int(user_pawn[0]), int(user_pawn[1]),int(user_pawn[2]))
        #else:
        #  user_pawn = (int(user_pawn[0]), int(user_pawn[1]))
        #user_move = (int(user_move[0]),int(user_move[1]))
        user_pawn = pawn
        user_move = move
        #check if the move is legal
        if b_eval(board,user_pawn[0],user_pawn[1]) != HUMAN and b_eval(board,user_pawn[0],user_pawn[1]) != H_KING:
            print('You dont have a pawn at that spot')
            continue
        human_moves = legal_moves(board,HUMAN)
        for move in human_moves[user_pawn]:
            if move[:2] == user_move: #Check if the chosen move is legal
                return user_pawn, move
        raise ValueError('Illegal Move')

def legal_moves(board, val):
    '''Checks all the legal moves for a player
    All King pieces are denoted by an extra element 0
    All Jump moves are denoted by an extra element with the coordinates of the jumped over element
    '''
    pieces = []
    l_moves = {}

    #Find all of the pieces of the player
    for row in range(len(board)):
        for col in range(len(board[row])):
            if b_eval(board,row,col) == val:
                pieces.append((row,col))
            elif b_eval(board,row,col) == val+2:
                pieces.append((row,col,0)) #add a 0 to differentiate kings

    #Check which side is forward
    if val == HUMAN:
        diff = -1
        OPP = COMPUTER
    elif val == COMPUTER:
        diff = 1
        OPP = HUMAN
    else:
        raise ValueError('Not a valid player value')

    #Find all possible moves
    # first two diagonals go forward, last two are for kings
    DIAGONALS = [(diff,-1),(diff,1),(-diff,-1),(-diff,1)]

    for piece in pieces:
        DIAG_PIECES = 2  # For pawns, 2 diagonals. For kings, 4 diagonals
        if len(piece) == 3:
            DIAG_PIECES = 4 #Redefine the nb of diagonals if the piece is a king
        l_moves[piece] = []
        for DIAG in DIAGONALS[:DIAG_PIECES]: #Only check first two diagonals since pieces can't move backwards
            possible_move = (piece[0]+DIAG[0], piece[1]+DIAG[1])

            #Check if the move stays on the board
            if 0 <= possible_move[0] <= 7 and 0 <= possible_move[1] <= 7:
                #Check if the wanted move moves to an empty position
                if board[possible_move[0]][possible_move[1]] == 0:
                    l_moves[piece].append(possible_move)
                #Check if the wanted move moves to opponent square
                elif board[possible_move[0]][possible_move[1]] == OPP or board[possible_move[0]][possible_move[1]] == OPP+2:
                    #Check if the next square over the opponent is free (if you can capture)
                    if 0<= possible_move[0]+DIAG[0] <= 7 and 0<= possible_move[1]+DIAG[1] <= 7:
                        if board[possible_move[0]+DIAG[0]][possible_move[1]+DIAG[1]] == 0:
                            #Add a third element to note that it is a jump move
                            jump_move = (possible_move[0]+DIAG[0],possible_move[1]+DIAG[1],possible_move)
                            l_moves[piece].append(jump_move)

    return l_moves

def game_over(board):
    '''Returns winner if one of the players has no more pieces or
    if one of the players has no more moves'''
    #Check if one side has no more pieces
    if not b_count(board, HUMAN) and not b_count(board,H_KING):
        print('GAME OVER, COMPUTER WINS (NO PIECES)')
        return COMPUTER
    elif not b_count(board, COMPUTER) and not b_count(board,C_KING):
        print('GAME OVER, HUMAN WINS (NO PIECES)')
        return HUMAN

    #Check if HUMAN has ran out of moves
    human_moves = False
    for move in legal_moves(board,HUMAN).values():
        #If HUMAN still has a move, the function will return False
        if move:
            human_moves = True
            break
    #Computer wins if HUMAN has no more moves
    if not human_moves:
        print('GAME OVER, COMPUTER WINS (NO MOVES)')
        return COMPUTER
    #Check if COMPUTER has ran out of moves
    computer_moves = False
    for move in legal_moves(board,COMPUTER).values():
        if move:
            computer_moves = True
            break
    if not computer_moves:
        print('GAME OVER, HUMAN WINS (NO MOVES)')
        return HUMAN

    #Game is not over if it passes all of the possible end scenarios
    return False

#TESTS FOR THE GAME CODE - COMPUTER VS COMPUTER
#c_wins = 0
#h_wins = 0
#draw = 0
#for trial in range(100):
#    test_board = game_start()
#    assert test_board == [[0, 2, 0, 2, 0, 2, 0, 2], [2, 0, 2, 0, 2, 0, 2, 0], [0, 2, 0, 2, 0, 2, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1, 0, 1], [1, 0, 1, 0, 1, 0, 1, 0]]
#    assert len(legal_moves(test_board,1).items()) == 12
#    assert len(legal_moves(test_board, 2).items()) == 12
#    assert not game_over(test_board)
#    
#    #Play a game to test it out
#    n_turns = 1
#    while not game_over(test_board):
#        #Choose random human move
#
#        h_move = _choose_move_greed(test_board,legal_moves(test_board,HUMAN),HUMAN)
#        #Run a round of the game
#        game_turn(test_board, *h_move)
#
#        
#        
#        n_turns += 1
#        #make the game quit after 100 turns if it doesn't end
#        if n_turns>200:
#            break
#        
#    #Print how many pieces of each side is left and the number of turns
#    
#    if n_turns != 201 and game_over(test_board) == HUMAN:
#        h_wins +=1
#    elif n_turns != 201 and game_over(test_board) == COMPUTER:
#        c_wins +=1
#    else:
#        draw +=1
#    print('H: {},K: {}, C: {},K: {}, N = {}'.format(b_count(test_board,HUMAN),b_count(test_board,H_KING),b_count(test_board,COMPUTER),b_count(test_board,C_KING),n_turns))
#    print(test_board)
#    print('-'*100)
#print('''HUMAN : {}
#COMPUTER: {}
#DRAW: {}'''.format(h_wins,c_wins,draw))
##GAME RUN CODE - PLAYER VS COMPUTER
#'''board = game_start()
#n = 0
#while not game_over(board) or n<50:
#    print(legal_moves(board,HUMAN)) # TO REMOVE -----------------
#    print(b_count(board,COMPUTER), b_count(board, HUMAN), b_count(board, C_KING))
#    player_move = player_turn(board)
#    game_turn(board,*player_move)
#    n+=1
#print('The winner is {}'.format(game_winner(board)))'''
#        
#
