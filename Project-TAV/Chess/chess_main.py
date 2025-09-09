import pygame as pg
import time
import os

pg.init()

os.chdir(os.path.abspath(__file__)[0:-14])

"""
Constants and initialization
"""

phone = False
SQUARE = 135 if phone else 70
WIDTH = 8*SQUARE
HEIGHT = 8*SQUARE

button_pos = [(int(WIDTH+SQUARE), int(3.5*SQUARE)),(int(WIDTH+3*SQUARE), int(3.5*SQUARE))] #redo button (x,y) and undo button (x,y)
button_size = int(SQUARE)

win = pg.display.set_mode((WIDTH+5*SQUARE, HEIGHT))
pg.display.set_caption("Chess")
win.fill((50, 50, 50))

GREEN = (118,150,86)
dGREEN = (88,120,56)
WHITE = (238,238,210)
dWHITE = (208,208,180)
GREY = (50, 50, 50)


# variables and dictionaries
position = [["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

coor_to_alpha = {0:"a", 1:"b", 2:"c", 3:"d", 4:"e", 5:"f", 6:"g", 7:"h"}

k_move = {"w": False,
          "b": False}

a_rook_move = {"w":False,
                "b" : False}
h_rook_move = {"w":False,
                "b" : False}

k_pos = {"w": (4, 7),
         "b": (4, 0)}

last_move = (None, None, None, None, None)
check = False

liste_position = [[rank[:] for rank in position]]
liste_moves = []
liste_last_moves = [last_move]
pos_index = 0

"""
Functions
"""
# draws the board
def draw_board():
    for col in range(8): # for every column
        for rank in range(8): # for every rank
            if (col+rank) % 2 == 0: # if the sum of the indices is even
                pg.draw.rect(win, WHITE, (col*SQUARE, rank*SQUARE, SQUARE, SQUARE)) # draws a white square
            else: # else
                pg.draw.rect(win, GREEN, (col * SQUARE, rank * SQUARE, SQUARE, SQUARE)) # draws a green square

# draws the pieces
def draw_pieces():
    global position # imports the position
    for rank in enumerate(position): # goes through every rank
        for col in enumerate(rank[1]): # goes through every column
            if col[1] != " ": # if the square is not empty
                # draws the piece by importing the right image
                win.blit(pg.transform.scale(pg.image.load(f"Pieces/{col[1]}.png"), (SQUARE, SQUARE)), ((col[0])*SQUARE, (rank[0])*SQUARE))

# draws undo and redo buttons if phone_mode
def draw_buttons(undo =True, redo=True):
    if undo: win.blit(pg.transform.scale(pg.image.load("Images/Undo-button.png"), (button_size, button_size)), (button_pos[0][0], button_pos[0][1]))
    if redo: win.blit(pg.transform.scale(pg.image.load("Images/Redo-button.png"), (button_size, button_size)), (button_pos[1][0], button_pos[1][1]))

# translates mouse position to chess coordinates
def mouse_to_pos(m_pos):
    m_x, m_y = m_pos # transcripts the pos tuple into x and y coordinates
    if 0 <= m_x <= WIDTH and 0 <= m_y <= HEIGHT: # if the pixel coordinate is on the chess board
        return True, (m_x//SQUARE, m_y//SQUARE) # returns True and gives the column and row number (starting at 0)
    else: # else
        return False, None # returns False and no coordinates

# checks if there is a piece on a certain square
def if_piece(col, rank):
    global position # import the position
    square = position[rank][col] # gets the string corresponding to the right coordinates
    if square != " ": # if the square is not empty
        return square # returns the string
    else: # else
        return False # returns False

# gets the type of piece on the square
def get_type(col, rank):
    piece = position[rank][col][1] # gets the type of piece
    if piece == "R": # if it's a Rook
        return Piece().Rook() # returns object type Rook
    elif piece == "P": # if it's a Pawn
        return Piece().Pawn() # returns object type Pawn
    elif piece == "K": # if it's a King
        return Piece().King() # returns object type King
    elif piece == "N": # if it's a kNight
        return Piece().Knight() # returns object type kNight
    elif piece == "Q": # if it's a queen
        return Piece().Queen() # returns object type Queen
    elif piece == "B": # if it's a Bishop
        return Piece().Bishop() # returns object type Bishop

# gets the color of the piece
def get_color(col, rank):
    return position[rank][col][0]

# checks if the move is legal
def is_valid_move(player, col_i, rank_i, col_f, rank_f):
    if (col_f, rank_f) in remove_illegal(player, col_i, rank_i, get_type(col_i, rank_i).legal_moves(col_i, rank_i)):
        return True
    else:
        return False

# plays the move
def move(col_i, col_f, rank_i, rank_f):
    global position

    piece = position[rank_i][col_i]

    position[rank_f][col_f] = piece
    position[rank_i][col_i] = " "

# blits all the legal moves
def blit_legal_moves(liste):
    for move in liste:
        col = move[0]
        rank = move[1]
        if if_piece(col, rank):
            pg.draw.circle(win, (168,168,168), (col*SQUARE+SQUARE//2, rank*SQUARE+SQUARE//2), SQUARE//2-2, 3)
        else:
            pg.draw.circle(win, (168,168,168), (col * SQUARE + SQUARE // 2, rank * SQUARE + SQUARE // 2), 10)

# checks if there is a check
def in_check(player, col_k, rank_k):
    global position # imports the position

    opposite_color = "b" if player == "w" else "w" # sets the opposite piece color

    for rank in enumerate(position): # for every rank in the position
        for col in enumerate(rank[1]): # for every column in the position
            # if the piece is the opposite color and not a king
            if position[rank[0]][col[0]][0] == opposite_color and position[rank[0]][col[0]][1] != "K":
                # gets all of its legal moves
                moves = get_type(col[0], rank[0]).legal_moves(col[0], rank[0])
                for move in moves: # and for every move
                    if move == (col_k, rank_k): # if the end square is the square the king is currently on
                        return True # returns True (in check)
            # else if the piece is the opposite color and is a king
            elif position[rank[0]][col[0]][0] == opposite_color and position[rank[0]][col[0]][1] == "K":
                if abs(col[0]-col_k)<=1 and abs(rank[0]-rank_k)<=1: # if the two pieces touch
                    return True # returns True (in check)
    return False # else return False (not in check)

# remove illegal moves if check
def remove_illegal(player, col_i, rank_i, liste):
    global position # imports the position

    legal_moves = []
    if position[rank_i][col_i][1] == "K": # if the piece is a king
        king = True
    else: # else
        king = False

    for moves in liste: # for every move in every possible move of the piece
        last_piece = position[moves[1]][moves[0]] # gets the piece of the end square

        move(col_i, moves[0], rank_i, moves[1]) # simulates the move

        if king: # if the played piece is a king
            k_col, k_rank = moves # "updates" the position of the king
        else: # else
            # gets the real position of the king
            k_col = k_pos[player][0]
            k_rank = k_pos[player][1]


        if not in_check(player, k_col, k_rank): # if the simulated move does not come with a check
            legal_moves.append(moves) # it's definitely legal and adds it to the "real" legal moves

        move(moves[0], col_i, moves[1], rank_i) # re-initialize the position
        position[moves[1]][moves[0]] = last_piece # replaces the end square piece

    return legal_moves

# checks if checkmate
def checkmate(player):
    global position

    if in_check(player, k_pos[player][0], k_pos[player][1]):
        for rank in enumerate(position):
            for col in enumerate(rank[1]):
                if position[rank[0]][col[0]][0] == player:
                    if len(remove_illegal(player, col[0], rank[0], get_type(col[0], rank[0]).legal_moves(col[0], rank[0]))) != 0:
                        return False
        return True

    else:
        return False

# checks if stalemate
def stalemate(player):
    global position

    if not in_check(player, k_pos[player][0], k_pos[player][1]):
        for rank in enumerate(position):
            for col in enumerate(rank[1]):
                if position[rank[0]][col[0]][0] == player:
                    if len(remove_illegal(player, col[0], rank[0],
                                          get_type(col[0], rank[0]).legal_moves(col[0], rank[0]))) != 0:
                        return False
        return True

    else:
        return False

#finds a specific Piece
def find_piece(piece_to_find, pos=0):
    global position
    if pos==0: pos=position
    for y, rank in enumerate(pos):
        for x, piece in enumerate(rank):
            if piece == piece_to_find:
                return (x,y)
    else: #if no piece finded
        return None

"""
Pieces
"""
class Piece:
    global position

    class Pawn:
        def legal_moves(self, col_i, rank_i):
            color = get_color(col_i, rank_i)

            legal_moves = []
            last_move = liste_last_moves[pos_index]

            if color == "w":
                if rank_i == 6:
                    if not if_piece(col_i, rank_i-2) and not if_piece(col_i, rank_i-1):
                        legal_moves.append((col_i, rank_i-2))

                if not if_piece(col_i, rank_i-1):
                    legal_moves.append((col_i, rank_i-1))

                if 1 <= col_i <= 7 and position[rank_i-1][col_i-1][0] == "b":
                    legal_moves.append((col_i-1, rank_i-1))

                if 0 <= col_i <= 6 and position[rank_i-1][col_i+1][0] == "b":
                    legal_moves.append((col_i+1, rank_i-1))

                # en passant
                if (last_move[0] == "bP"
                    and last_move[3] == 1
                    and last_move[4] == 3
                    and rank_i == 3):
                    if col_i == last_move[2]+1:
                        legal_moves.append((col_i-1, 2))
                    elif col_i == last_move[2]-1:
                        legal_moves.append((col_i+1, 2))


            elif color == "b":
                if rank_i == 1:
                    if not if_piece(col_i, rank_i+2):
                        legal_moves.append((col_i, rank_i+2))

                if not if_piece(col_i, rank_i+1):
                    legal_moves.append((col_i, rank_i+1))

                if 1 <= col_i <= 7 and position[rank_i+1][col_i-1][0] == "w":
                    legal_moves.append((col_i-1, rank_i+1))

                if 0 <= col_i <= 6 and position[rank_i+1][col_i+1][0] == "w":
                    legal_moves.append((col_i+1, rank_i+1))

                # en passant
                if (last_move[0] == "wP"
                    and last_move[3] == 6
                    and last_move[4] == 4
                    and rank_i == 4):
                    if col_i == last_move[2]+1:
                        legal_moves.append((col_i-1, 5))
                    elif col_i == last_move[2]-1:
                        legal_moves.append((col_i+1, 5))

            return legal_moves

    class Rook:
        def legal_moves(self, col_i, rank_i):
            color = get_color(col_i, rank_i)

            dir = [(0, 1), (0, -1), (1, 0), (-1, 0)]

            legal_moves = []

            for direction in dir:
                col = col_i
                rank = rank_i
                while 0 <= col <= 7 and 0 <= rank <= 7:
                    rank += direction[0]
                    col += direction[1]

                    if col < 0 or col > 7 or rank < 0 or rank > 7:
                        break

                    if position[rank][col][0] != color:
                        legal_moves.append((col, rank))
                        if position[rank][col] != " ":
                            break
                    else:
                        break
            return legal_moves

    class Knight:
        def legal_moves(self, col_i, rank_i):
            color = get_color(col_i, rank_i)

            dir = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)]

            legal_moves = []

            for direction in dir:
                rank = rank_i+direction[0]
                col = col_i+direction[1]

                if 0 <= rank <= 7 and 0 <= col <= 7:
                    if position[rank][col][0] != color:
                        legal_moves.append((col, rank))

            return legal_moves

    class Bishop:
        def legal_moves(self, col_i, rank_i):
            color = get_color(col_i, rank_i)

            dir = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

            legal_moves = []

            for direction in dir:
                col = col_i
                rank = rank_i
                while 0 <= col <= 7 and 0 <= rank <= 7:
                    rank += direction[0]
                    col += direction[1]

                    if col < 0 or col > 7 or rank < 0 or rank > 7:
                        break

                    if position[rank][col][0] != color:
                        legal_moves.append((col, rank))
                        if position[rank][col] != " ":
                            break
                    else:
                        break

            return legal_moves

    class King:
        def legal_moves(self, col_i, rank_i):
            color = get_color(col_i, rank_i)

            dir = [(1, 1), (1, -1), (1, 0), (-1, 1), (-1, -1), (-1, 0), (0, 1), (0, -1)]

            legal_moves = []

            for direction in dir:
                col = col_i + direction[1]
                rank = rank_i + direction[0]

                if 0 <= col <= 7 and 0 <= rank <= 7:
                    if position[rank][col][0] != color and not in_check(color, col, rank):
                        legal_moves.append((col, rank))


            # short castle
            if (not k_move[color]
                    and not h_rook_move[color]
                    and not in_check(color, 4, rank_i)
                    and not in_check(color, 5, rank_i)
                    and not in_check(color, 6, rank_i)
                    and not if_piece(5, rank_i)
                    and not if_piece(6, rank_i)):
                legal_moves.append((6, rank_i))

            # long castle
            if (not k_move[color]
                    and not a_rook_move[color]
                    and not in_check(color, 2, rank_i)
                    and not in_check(color, 3, rank_i)
                    and not in_check(color, 4, rank_i)
                    and not if_piece(3, rank_i)
                    and not if_piece(2, rank_i)):
                legal_moves.append((2, rank_i))

            return legal_moves

    class Queen:
        def legal_moves(self, col_i, rank_i):
            rook_moves = Piece.Rook().legal_moves(col_i, rank_i)
            bishop_moves = Piece.Bishop().legal_moves(col_i, rank_i)

            legal_moves = []

            for move in rook_moves:
                legal_moves.append(move)
            for move in bishop_moves:
                legal_moves.append(move)

            return legal_moves

"""
Game
"""
def main():
    global k_move, a_rook_move, h_rook_move, k_pos, last_move, liste_position, position, liste_moves, liste_last_moves, pos_index

    running = True

    col_i = None
    col_f = None

    rank_i = None
    rank_f = None

    move_i = False
    move_f = False
    clic = False
    click_move = False

    player = "w"

    end=0

    while running:
        #inputs
        mouse_pos = pg.mouse.get_pos()
        user_input = pg.key.get_pressed()
        leftarrow, rightarrow = False, False

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                end=0 #seconds before the window is closed

            # if the mouse button gets down
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                val, get_pos = mouse_to_pos(mouse_pos) #val: if mouse is in the chessboard; get_pos: coordinates of the square
                if val: clic = True #if the mouse button is down
                if val and move_i: #if move started
                    if get_pos[0]==col_i and get_pos[1]==rank_i: move_i=False #same square clicked --> aborting
                    if click_move: #if it is the second click
                        if position[get_pos[1]][get_pos[0]][0] == player: #aborting a click move if th player wants to play another piece
                            col_i = get_pos[0]
                            rank_i = get_pos[1]
                            click_move = False
                        else: #finishing the move
                            move_f = True
                            click_move = False
                            col_f = get_pos[0]
                            rank_f = get_pos[1]
                elif val and position[get_pos[1]][get_pos[0]] != " ":
                    move_i = True
                    col_i = get_pos[0]
                    rank_i = get_pos[1]
                else:
                    move_i = False
                if not val and phone: #arrows for phone
                    if button_pos[0][0] < mouse_pos[0] < button_pos[0][0] + button_size and button_pos[0][1] < mouse_pos[1] < button_pos[0][1] + button_size: leftarrow = True
                    if button_pos[1][0] < mouse_pos[0] < button_pos[1][0] + button_size and button_pos[1][1] < mouse_pos[1] < button_pos[1][1] + button_size: rightarrow = True

            # if the mouse button gets up
            if event.type == pg.MOUSEBUTTONUP and event.button==1:
                if 0<=mouse_pos[0]<=WIDTH and 0<=mouse_pos[1]<=HEIGHT:
                    val, get_pos = mouse_to_pos(mouse_pos)
                    if val: clic = False
                    if val and move_i and not move_f:#if in the move
                        if get_pos[0]==col_i and get_pos[1]==rank_i and position[rank_i][col_i][0]==player:
                        #if the mouse stays on the same square:
                            if not click_move: #passing in click_move
                                click_move = True
                                move_f = False
                            else: #???
                                move_f = True
                                click_move = False
                                col_f = get_pos[0]
                                rank_f = get_pos[1]
                        else: #ending the move
                            move_f = True
                            click_move = False
                            col_f = get_pos[0]
                            rank_f = get_pos[1]
                    else:
                        move_f = False
                else: #aborting if mouse not in the screen
                    move_f = False
                    move_i = False

            if user_input[pg.K_LEFT]: leftarrow = True

            if user_input[pg.K_RIGHT]: rightarrow = True

            if user_input[pg.K_UP]: #last position of the list
                position = [rank[:] for rank in liste_position[-1]]
                pos_index = len(liste_position)-1
                move_i = False
                move_f = False
                click_move = False
                k_pos = {"w":find_piece("wK"), "b": find_piece("bK")}

                player = "w" if pos_index%2 == 0 else "b"

            if user_input[pg.K_DOWN]: #first position
                position = [rank[:] for rank in liste_position[0]]
                pos_index = 0
                move_i = False
                move_f = False
                click_move = False
                k_pos = {"w": (4, 7),"b": (4, 0)}

                player = "w"
        
        if leftarrow and pos_index > 0: #position before current displayed position
            position = [rank[:] for rank in liste_position[pos_index-1]]
            pos_index -= 1
            move_i = False
            move_f = False
            click_move = False
            k_pos = {"w":find_piece("wK"), "b": find_piece("bK")}

            player = "w" if player == "b" else "b"
            
        if rightarrow and pos_index < len(liste_position)-1: #position after current displayed position
            position = [rank[:] for rank in liste_position[pos_index+1]]
            pos_index += 1
            move_i = False
            move_f = False
            click_move = False
            k_pos = {"w":find_piece("wK"), "b": find_piece("bK")}

            player = "w" if player == "b" else "b"


        # if a move is played
        if move_i and move_f:
            # if it's not the same square
            if (col_i,rank_i) != (col_f,rank_f):
                # if the move is valid and if it's the right player's turn
                if is_valid_move(player, col_i, rank_i, col_f, rank_f) and get_color(col_i, rank_i) == player:
                    if pos_index < len(liste_position)-1: #if aborted moves
                        del liste_position[pos_index+1:], liste_last_moves[pos_index+1:] #delete end of the positions
                    last_move = liste_last_moves[pos_index]
                    piece = position[rank_i][col_i]
                    castle = False
                    #if a piece is captured
                    capture = True if (position[rank_f][col_f][0] != " " and  position[rank_f][col_f][0] != player) else False
                    en_passant = False
                    # if the king is moved
                    if piece[1] == "K":
                        k_move[player] = True
                        k_pos[player] = (col_f, rank_f)

                        # if short castle
                        if col_f == col_i + 2:
                            move(7, 5, rank_i, rank_f)
                            castle = "O-O"
                        # if long castle
                        elif col_f == col_i - 2:
                            move(0, 3, rank_i, rank_f)
                            castle = "O-O-O"

                    # if a rook is moved
                    elif piece[1] == "R":
                        if col_i == 0:
                            a_rook_move[player] = True
                        elif col_i == 7:
                            h_rook_move[player] = True

                    # if a pawn is moved
                    elif piece[1] == "P":
                        # if white promotes
                        if player == "w":
                            # if en passant IS PLAYED (which it is because en passant is always forced :))
                            if (last_move[0] == "bP"
                                    and last_move[3] == 1
                                    and last_move[4] == 3
                                    and rank_i == 3
                                    and col_f == last_move[1] ):
                                if col_i == last_move[2] + 1:
                                    position[3][col_i - 1] = " "
                                    en_passant = -1
                                elif col_i == last_move[2] - 1:
                                    position[3][col_i + 1] = " "
                                    en_passant = -1

                            # if promotes
                            if rank_f == 0:
                                pg.draw.rect(win, (255, 255, 255), (col_f*SQUARE, 0, SQUARE, 4*SQUARE))

                                list_pieces = ["wQ", "wR", "wN", "wB"]

                                for pieces in enumerate(list_pieces):
                                    win.blit(pg.transform.scale(pg.image.load(f"Pieces/{pieces[1]}.png"), (SQUARE, SQUARE)),
                                             (col_f * SQUARE, pieces[0]*SQUARE))

                                pg.display.update()

                                promote = True

                                while promote:
                                    mouse_pos = pg.mouse.get_pos()

                                    val, sq = mouse_to_pos(mouse_pos)

                                    for event in pg.event.get():
                                        if event.type == pg.MOUSEBUTTONDOWN:
                                            if val and 0 <= sq[1] <= 3 and sq[0] == col_f:
                                                position[1][col_i] = list_pieces[sq[1]]
                                                promote = False

                        else:
                            # if en passant is played
                            if (last_move[0] == "wP"
                                  and last_move[3] == 6
                                  and last_move[4] == 4
                                  and rank_i == 4
                                  and col_f == last_move[1] ):
                                if col_i == last_move[2] + 1:
                                    position[4][col_i - 1] = " "
                                    en_passant = 1
                                elif col_i == last_move[2] - 1:
                                    position[4][col_i + 1] = " "
                                    en_passant = 1

                            # if promotes
                            if rank_f == 7:
                                pg.draw.rect(win, (255, 255, 255), (col_f*SQUARE, HEIGHT-4*SQUARE, SQUARE, 4*SQUARE))

                                list_pieces = ["bQ", "bR", "bN", "bB"]

                                for pieces in enumerate(list_pieces):
                                    win.blit(pg.transform.scale(pg.image.load(f"Pieces/{pieces[1]}.png"), (SQUARE, SQUARE)),
                                             (col_f*SQUARE, HEIGHT-(pieces[0]+1)*SQUARE))

                                pg.display.update()

                                promote = True

                                while promote:
                                    mouse_pos = pg.mouse.get_pos()

                                    val, sq = mouse_to_pos(mouse_pos)

                                    for event in pg.event.get():
                                        if event.type == pg.MOUSEBUTTONDOWN:
                                            if val and 4 <= sq[1] <= 7 and sq[0] == col_f:
                                                position[6][col_i] = list_pieces[7-sq[1]]
                                                promote = False

                    move(col_i, col_f, rank_i, rank_f)
                    last_move = (piece, col_i, col_f, rank_i, rank_f)
                    liste_last_moves.append(last_move)

                    # checks if 3-fold repetition
                    if player == "b":
                        if liste_position.count(position) == 3:
                            print("3-fold repetition")

                    player = "w" if player == "b" else "b"
                    liste_position.append([rank[:] for rank in position])
                    pos_index += 1

                    piece = piece[1] if piece[1] != "P" else ""
                    capture = "x" if capture else ""
                    if castle:
                        moves = castle
                    else:
                        if en_passant:
                            moves = f"{coor_to_alpha[col_i]}x{coor_to_alpha[col_f]}{8-rank_f+en_passant}"
                            en_passant = False
                        elif capture and piece == "":
                            moves = f"{coor_to_alpha[col_i]}{capture}{coor_to_alpha[col_f]}{8-rank_f}"
                        else:
                            moves = f"{piece}{capture}{coor_to_alpha[col_f]}{8-rank_f}"

                    if checkmate(player):
                        moves += "#"
                    elif in_check(player, k_pos[player][0], k_pos[player][1]):
                        moves += "+"

                    liste_moves.append(moves)

            move_f = False
            move_i = False

        if checkmate(player) or stalemate(player):
            print("checkmate or stalemate")
            end=120
            running=False

        # draws the board and the pieces
        win.fill(GREY)
        draw_board()
        draw_pieces()
        if phone: draw_buttons(pos_index > 0, pos_index < len(liste_position)-1) #If phone, draws undo and redo buttons if available

        # draws who is playing
        t="White" if player == "w" else "Black"
        t += " is playing"
        police = pg.font.SysFont("Arial", int(SQUARE/3.5))
        texte = police.render(t, True, (255,255,255))
        win.blit(texte, (WIDTH + 30, 10))

        #if the player drags a piece
        if move_i:
            # empty the square where the piece comes from
            if (col_i + rank_i) % 2 == 0:
                if (clic and move_i) or move_f: # if the mouse is down: draws a normal square
                    pg.draw.rect(win, WHITE, (col_i * SQUARE, rank_i * SQUARE, SQUARE, SQUARE))
                else: #draws a different square
                    pg.draw.rect(win, dWHITE, (col_i * SQUARE, rank_i * SQUARE, SQUARE, SQUARE))
            else:
                if (clic and move_i) or move_f: # if the mouse is down: draws a normal square
                    pg.draw.rect(win, GREEN, (col_i * SQUARE, rank_i * SQUARE, SQUARE, SQUARE))
                else: #draws a different square
                    pg.draw.rect(win, dGREEN, (col_i * SQUARE, rank_i * SQUARE, SQUARE, SQUARE))


            # draws all the possible moves
            if position[rank_i][col_i][0] == player:
                blit_legal_moves(remove_illegal(player, col_i, rank_i, get_type(col_i, rank_i).legal_moves(col_i, rank_i)))

            if move_i and not move_f and clic and not click_move: # if the mouse is down: draws the piece where the mouse is
                win.blit(pg.transform.scale(pg.image.load(f"Pieces/{position[rank_i][col_i]}.png"),
                                            (SQUARE + 20, SQUARE + 20)),
                                            ((mouse_pos[0]-(SQUARE+20)//2, mouse_pos[1]-(SQUARE+20)//2)))
            else: # if the mouse is up: draws the piece at the initial place
                win.blit(pg.transform.scale(pg.image.load(f"Pieces/{position[rank_i][col_i]}.png"),
                                        (SQUARE, SQUARE)),
                                        (col_i*SQUARE,rank_i*SQUARE))



        pg.display.update()

    win.fill(GREY)
    draw_board()
    draw_pieces()
    pg.display.update()
    time.sleep(end)
    pg.quit()


if __name__ == "__main__":
    main()