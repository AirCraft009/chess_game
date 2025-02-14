import pygame

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
        if board[space] == 0:
            continue
        pieces[space].x = pos_board[space][0]
        pieces[space].y = pos_board[space][1]
        pieces[space].space = space
        pieces[space].render()
        
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
    
def unplay_move(move, board, capture = None):
    board[move[0]] = board[move[1]]
    board[move[1]] = 0
    if capture != 0:
        board[move[1]] = capture