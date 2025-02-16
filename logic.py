import pygame

piece_value = {
    2: 1,
    3: 1,
    4: 3,
    5: 3,
    8: 5,
    9: 5,
    16: 5,
    17: 5,
    32: 9,
    33: 9,
    64: 18,
    65: 18
}

def draw_board(screen):
    for y in range(8):
        for x in range(8):
            pygame.draw.rect(screen, ("grey" if y % 2 - x % 2 == 0 else "teal"), (y*100 , x * 100,  100, 100))
            
def init_posboard():
    pos_board = {}
    for y in range(8):
        for x in range(8):
            pos_board[x + y*8] = (x*100, 700 - y * 100)
    return pos_board

def update_pieces(board, pieces, pos_board):
    for space in range(64):
        if board[space] == 0 and space not in pieces:
            continue
        pieces[space].x = pos_board[space][0]
        pieces[space].y = pos_board[space][1]
        pieces[space].space = space
        pieces[space].render()
        pieces
        
def check_promotion(board):
    for c in range(2):
        for x in range(8):
            if board[x + c*56] == 2 or board[x + c*56] == 3:
                return True, x + c * 56
    return False, None


def check_castle(king_square, color, board, pieces):
    castle_king = False
    castle_queen = False
    o = 0 if color else 1
    if pieces[king_square].moved:
        return False, False
    for side in range(2):
        if side == 0:
            if board[king_square + 3] == 16 + o:
                castle_king = True
            for x in range(1, 3):
                if board[king_square + x] != 0:
                    castle_king = False
                    break
        else:
            if board[king_square - 4] == 16 + o:
                castle_queen = True
            for x in range(1, 4):
                if board[king_square - x] != 0:
                    castle_queen = False
                    break
                
    return castle_king, castle_queen


def select_square(square, poss_moves, pos_board, screen, k_w, pieces, board):
    if square == k_w:
        ck, cq = check_castle(k_w, True, board, pieces)
        if not ck and not cq:
            ck = False
        elif ck and cq:
            pygame.draw.rect(screen, "red", (pos_board[k_w + 2][0], pos_board[k_w+2][1], 100, 100),5), 
            pygame.draw.rect(screen, "red", (pos_board[k_w - 2][0], pos_board[k_w-2][1], 100, 100),5), 
        elif cq:
            pygame.draw.rect(screen, "red", (pos_board[k_w + -2][0], pos_board[k_w-2][1], 100, 100),5), 
        else:
            pygame.draw.rect(screen, "red", (pos_board[k_w + 2][0], pos_board[k_w+2][1], 100, 100),5), 

        
    if square not in poss_moves:
        return False
    
    for space in poss_moves[square]:
        pygame.draw.rect(screen, "red", (pos_board[space][0], pos_board[space][1], 100, 100), 5)
    pygame.draw.rect(screen, "red", (pos_board[square][0], pos_board[square][1], 100, 100), 5)
    return True

def check_check(possible_enemy, king_square):
    for space in possible_enemy:
        for move in possible_enemy[space]:
            if move == king_square:
                return True
    return False

    
def render_pieces(pieces):
    for piece in pieces:
        pieces[piece].render()
        
def play_move(move, board):
    capt_piece = board[move[1]]
    board[move[1]] = board[move[0]]
    board[move[0]] = 0
    return capt_piece
    
def unplay_move(move, board, capture = 0):
    board[move[0]] = board[move[1]]
    board[move[1]] = 0
    if capture != 0:
        board[move[1]] = capture
        
def play_move_piece(move, board, pieces, pos_board):
    capt_piece = board[move[1]]
    if capt_piece != 0:
        cap = pieces.pop(move[1])
    else:
        cap = None
    pieces[move[0]].x = pos_board[move[1]][0]
    pieces[move[0]].y = pos_board[move[1]][1]
    pieces[move[0]].space = move[1]
    pieces[move[0]].moved = True
    pieces[move[1]] = pieces[move[0]]
    pieces.pop(move[0])
    board[move[1]] = board[move[0]]
    board[move[0]] = 0
    return capt_piece, cap

def unplay_move_piece(move, board,  pieces, pos_board, capture = 0, cap = None):

    piece_start = pieces[move[1]]
    if capture != 0:
        print(f"unplaying capture of {capture}")
        board[move[1]] = capture
        pieces[move[0]] = piece_start
        pieces[move[1]] = cap
        pieces[move[1]].x = pos_board[move[1]][0]
        pieces[move[1]].y = pos_board[move[1]][1]
        pieces[move[1]].space = move[1]
        pieces[move[1]].moved = True
    else:
        pieces[move[0]] = pieces[move[1]]
        pieces.pop(move[1])
        
    pieces[move[0]].x = pos_board[move[1]][0]
    pieces[move[0]].y = pos_board[move[1]][1]
    pieces[move[0]].space = move[0]
    pieces[move[0]].moved = True
    board[move[0]] = board[move[1]]
    board[move[1]] = 0 
    pygame.display.flip()   
    
        
def calc_material(board):
    white_mat = 0
    black_mat = 0
    for space in board:
        if board[space] == 0:
            continue
        if board[space]%2 == 0:
            white_mat += piece_value[board[space]]
        else:
            black_mat += piece_value[board[space]]
    return white_mat, black_mat
