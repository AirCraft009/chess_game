from random import choice
from piece_board import piece_board
from logic import check_check, play_move, unplay_move

Pawn = 2
Pawnb = 3
Knight = 4
Knightb = 5
Bishop = 8
Bishopb = 9
Rook = 16
Rookb = 17
Queen = 32
Queenb = 33
King = 64
Kingb = 65

straight_sliding = [Rook, Rookb, Queen, Queenb]
diagonal_sliding = [Bishop, Bishopb, Queen, Queenb]

offsets = {
    "up": 8,
    "down": -8,
    "left": -1,
    "right": 1,
    "dia_r_up": 9,
    "dia_r_down": -7,
    "dia_l_up": 7,
    "dia_l_down": -9
}

left_edge = [0, 8, 16, 24, 32, 40, 48, 56]
bootom = [0, 1, 2, 3, 4, 5, 6, 7]
distance_top = {}
distance_left = {}
distance_right = {}
distance_bottom = {}


white_pieces = {}
black_pieces = {}
for x in range(64):
    distance_left[x] = x % 8
    distance_right[x] = 7 - (x % 8)
    for i in left_edge:
        if x >= i and x < i + 8:
            distance_bottom[x] = i//8
    distance_top[x] = 7 - distance_bottom[x]


def knight_moves(space):
    knight_moves = [
            (-17, space % 8 != 0 and space > 16),
            (-15, space % 8 != 7 and space > 16),
            (-10, space % 8 > 1 and space > 8),
            (-6, space % 8 < 6 and space > 8),
            (6, space % 8 > 1 and space < 56),
            (10, space % 8 < 6 and space < 56),
            (15, space % 8 != 0 and space < 48),
            (17, space % 8 != 7 and space < 48)
        ]
    l1 = [space + move for move, condition in knight_moves if condition]
    l2 = [[x] for x in l1]
    return l2
    
def king_moves(space):
    king_moves = [
            (-9, space % 8 != 0 and space > 8),
            (-8,space > 8),
            (-7, space % 8 != 7 and space > 8),
            (-1, space % 8 != 0 and space > 0),
            (8, space < 56),
            (9, space % 8 != 7 and space < 56),
            (7, space % 8 != 0 and space < 56),
            (1, space % 8 != 7 and space < 63)
    ]
    
    l1 = [space + move for move, condition in king_moves if condition]
    l2 = [[x] for x in l1]
    return l2

def get_straights(space):
    u = []
    r = []
    d = []
    l = []
    straights = []
    for x in range(4):
        for y in range(1, 9):
            if x == 0:
                up = (space + offsets["up"]*y)
                if up <= 63:
                    u.append(up)
            elif x == 1:
                right = (space + offsets["right"]*y)
                if right%8 <= 7 and right // 8 == space // 8:
                    r.append(right)
            elif x == 2:
                down = (space + offsets["down"]*y)
                if down >= 0:
                    d.append(down)
            else:
                left = (space + offsets["left"]*y)
                if left%8 >= 0 and left // 8 == space // 8:
                    l.append(left)
    
    straights = [u, r, d, l]
    return straights

def get_diagonals(space):
    dl = distance_left[space]
    dr = distance_right[space]
    dru = []
    drd = []
    dlu = []
    dld = []
    for x in range(4):
        if x == 0:
            for y in range(1,dl+1):
                lu = space + offsets["dia_l_up"]*y
                if lu <= 63:
                    dlu.append(lu)
        elif x == 1:
            for y in range(1, dr+1):
                ru = space + offsets["dia_r_up"]*y
                if ru <= 63:
                    dru.append(ru)      
        elif x == 2:
            for y in range(1, dr+1):
                rd = space + offsets["dia_r_down"]*y
                if rd >= 0:
                    drd.append(rd)
        else:
            for y in range(1, dl+1):
                ld = space + offsets["dia_l_down"]*y
                if ld >= 0:
                    dld.append(ld)
    
    diagonals = [dld, dlu, drd, dru]
    return diagonals
    # print(diagonals)
                
            
                 
def get_pawns(space, pawn, color, board):
    o = 0 if color else 1

    pawn_moves = []
    if color:
        if space > 56:
            return []
        if board[space + 8] != 0:
            pawn_moves = []
        else:
            if pawn.moved:
                pawn_moves = [space + 8]
            else:
                if board[space + 16] != 0:
                    pawn_moves = [space + 8]
                else:
                    pawn_moves = [space + 8,space + 16 if space < 56 else 0]
                
        if space%8 != 7 and board[space + 9] != 0:
            pawn_moves.append(space + 9)
        if space%8 != 0 and board[space + 7] != 0:
            pawn_moves.append(space + 7)
            

            
    else:
        if space < 8:
            return []
        if board[space - 8] != 0:
            pawn_moves = []
        else:
            if pawn.moved:
                pawn_moves = [space - 8 if space > 7 else 0]
            else:
                if board[space - 16] != 0:
                    pawn_moves = [space - 8 if space > 7 else 0]
                else:
                    pawn_moves = [space - 8 if space > 7 else 0, space - 16 if space > 15 else 0]
                    
        if space%8 != 0 and board[space - 9] != 0:
            pawn_moves.append(space - 9)
        if space%8 != 7 and board[space - 7] != 0:
            pawn_moves.append(space - 7)
    # print(pawn_moves)
    return [[x] for x in pawn_moves]
                
        
   
   
   
def legal_move(moves, board, color):
    """
    This function takes a dictionary of possible moves, a list representing the board, and a boolean indicating the color of the player.
    It returns a dictionary of legal moves, where the keys are the origin spaces and the values are lists of destination spaces.
    """
    legal_moves = {}
    under_moves = []
    o = 0 if color else 1
    for origin_space in moves:
        for direction in moves[origin_space]:
            for destination_space in direction:
                if board[destination_space] == 0:
                    under_moves.append(destination_space)
                elif board[destination_space] % 2 == o:
                    break
                else:
                    under_moves.append(destination_space)
                    break
        legal_moves[origin_space] = under_moves.copy()
        under_moves.clear()
    return legal_moves
                    
             
                
    
def castle(king_square, color, side, board):
    o = 0 if color else 1
    if side == 0:
        for x in range(1, 3):
            if board[king_square + x] != 0:
                return False, king_square
        if board[king_square + 3] == 16 + o:
            board[king_square] = 0
            board[king_square + 2] = 64+o
            board[king_square+3] = 0
            board[king_square+1] = 16 + o
            return True, king_square + 2
    else:
        for x in range(1, 4):
            if board[king_square - x] != 0:
                return False
        if board[king_square - 4] == 16 + o:
            board[king_square] = 0
            board[king_square - 2] = 64+o
            board[king_square-4] = 0
            board[king_square-1] = 16 + o
            return True, king_square - 2
    return False, king_square

                    
    

def check_less_moves(king_square, moves, board, color, pieces):
    global real_king 
    real_king = king_square
    f_moves = []
    for o_space in moves:
        f_moves.clear()
        for dest in moves[o_space]:
            if o_space == real_king:
                king_square = dest
            move = (o_space, dest)
            cap = play_move(move, board)
            enemy_moves = poss_moves(board, pieces, not color)
            # print(enemy_moves)
            if check_check(enemy_moves, king_square):
                unplay_move(move, board, cap)
                continue
            f_moves.append(dest)
            unplay_move(move, board, cap)
            king_square = real_king
        moves[o_space] = f_moves.copy()
    return moves
                

def poss_moves(board, pieces, color):
    global king_square
    moves = {}
    o = 0 if color else 1
    for x in board:
        if board[x] != 0:
            if board[x] % 2 == o:
                if board[x] == 2+o:
                    moves[x] = get_pawns(x, pieces[x], color, board)
                    # pieces[x].moved = True
                elif board[x] == 4+o:
                    moves[x] = knight_moves(x)
                elif board[x] == 8+o:
                    moves[x] = get_diagonals(x)
                elif board[x] == 16+o:
                    moves[x] = get_straights(x)
                elif board[x] == 32+o:
                    moves[x] = get_straights(x)  +  get_diagonals(x)
                elif board[x] == 64+o:
                    king_square = x
                    moves[x] = king_moves(x) 
    legal = legal_move(moves, board, color)
    return legal

def final_moves(board, pieces, color):
    moves = poss_moves(board, pieces, color)
    print(king_square)
    return check_less_moves(king_square, moves, board, color, pieces)



"""
def generate_moves(board_pieces, board, depth):
    moves_white = poss_moves(board, board_pieces, True)
    moves_black = poss_moves(board, board_pieces, False)
    test_board = board.copy()
    while depth > 0:
        white_moves = choice(list(moves_white.keys()))
        black_moves = choice(list(moves_black.keys()))
        move_white = moves_white[white_moves]
        test_board[move_white] = board[white_moves]
        test_board[] = 0
        """#
        

        
        
    


    
            
    

                           
if __name__ == "__main__":                        
    # print(get_diagonals(5))         
    # print(get_straights(57))        
    # print(get_pawns(57, False, False))
    print(king_moves(31))
    print(31%8)
    # print(knight_moves(1))
