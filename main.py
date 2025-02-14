import pygame
import logic
import init_image
from fen_read import read_Fen
from piece_board import piece_board
from possible_moves import poss_moves, castle, check_castle

fen = "rnbkqbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBKQBNR"
clicked = False
turn = True
selected = None
board, k_w, k_b = read_Fen(fen, {})
pos_board = logic.init_posboard()
k_w_castle_k = k_w +2
k_w_castle_q = k_w - 2
k_b_castle = True

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Chess_Bot")
images = init_image.init_images()
pygame.display.set_icon(images[12])
# castle(k_b, False, 0, board)
pieces = piece_board(board, pos_board, screen, images)
print(check_castle(k_w, True, board, pieces))

def handle_click(square):
    global k_w, pieces
    if not clicked:
        logic.draw_board(screen)
        logic.render_pieces(pieces)
        if logic.select_square(square, possible, pos_board, screen, k_w, pieces, board):
            return square, True
        else:
            return None, False
    
    ck, cq = check_castle(k_w, True, board, pieces)
    if selected == k_w:
        if ck:
            possible[k_w].append(k_w+2)
        if cq:
            possible[k_w].append(k_w-2)
        if square == k_w_castle_k and ck:
            castle(k_w, True, 0, board)
            pieces = piece_board(board, pos_board, screen, images)
            logic.update_pieces(board, pieces, pos_board)
            logic.draw_board(screen)
            logic.render_pieces(pieces)
            k_w = k_w + 2
            return None, False
        if square == k_w_castle_q and cq:
            castle(k_w, True, 1, board)
            pieces = piece_board(board, pos_board, screen, images)
            logic.update_pieces(board, pieces, pos_board)
            logic.draw_board(screen)
            logic.render_pieces(pieces)
            k_w = k_w - 2
            return None, False
          
    if square not in possible[selected]:
        logic.draw_board(screen)
        logic.render_pieces(pieces)
        return None, False, 
    
    piece_val = board[selected]
    board[selected] = 0
    board[square] = piece_val
    pieces[selected].x = pos_board[square][0]
    pieces[selected].y = pos_board[square][1]
    pieces[selected].space = square
    pieces[square] = pieces[selected]
    pieces[square].moved = True
    if piece_val == 64:
        k_w = square
    pieces.pop(selected)
    logic.draw_board(screen)
    logic.render_pieces(pieces)
    return None, False

logic.draw_board(screen)
logic.render_pieces(pieces)
possible = poss_moves(board, pieces, True)
# logic.select_square(0, possible, pos_board, screen)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            # logic.draw_board(screen)
            # logic.render_pieces(pieces)
            pos = pygame.mouse.get_pos()
            posx = pos[0] // 100
            posy = 7 - pos[1] // 100
            square = posx + posy * 8
            print(square)
            selected, clicked = handle_click(square)
            possible = poss_moves(board, pieces, True)
            
    
    pygame.display.flip()