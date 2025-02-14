from fen_read import read_Fen
from piece_board import *
from evalution import *
from possible_moves import poss_moves
import random
import pygame
poss_board = {}

turn = 0
global board_pieces, white_moves, black_moves, k_w, k_b


fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
board, k_w, k_b = read_Fen(fen, {})

def init_sub():
    pieces = get_pieces() 
    return pieces

def play_move(move: tuple[int, int]):
    piece_val = board[move[0]]
    if piece_val == 64:
        k_w = move[1]
    elif piece_val == 65:
        k_b = move[1]
    board[move[0]] = 0
    board[move[1]] = piece_val
    turn == 0 if turn == 1 else 1
    
    
def set_board(board1):
    board = board1
    
def draw_board(screen):
    for y in range(8):
        for x in range(8):
            pygame.draw.rect(screen, ("grey" if y % 2 - x % 2 == 0 else "teal"), (y*100 , x * 100,  100, 100))
            poss_board[x + y * 8] = ((x*100 ,700-y * 100))
    return poss_board
    
def get_board():
    return board

def render_pieces(board_pieces, screen):
    draw_board(screen)
    for piece in board_pieces:
        board_pieces[piece].render()

def update_board(screen, move: tuple[int, int], pos_board: dict, images: list, board_pieces):
    play_move(move)    
    pieces = piece_board(board, pos_board, screen, images)
    pieces[move[0]].move(move, poss_board)
    render_pieces(pieces, screen)
    return
    
    
def get_rand_dict_item(dic: dict):
    rand_item = random.choice(list(dic.items()))
    return rand_item
        
def get_moves(pos_board, screen, images):
    board_pieces = piece_board(board, pos_board, screen, images)
    if turn == 0:
        white_moves = poss_moves(board, board_pieces, True)
        return white_moves
    else:
        black_moves = poss_moves(board, board_pieces, False)
        return black_moves

def play_random(screen, images):
    pos_board = draw_board(screen)
    rand_square, poss_squares = get_rand_dict_item(get_moves(pos_board, screen, images))
    poss_square = random.choice(poss_squares)
    pos_board = draw_board(screen)
    update_board(screen, (rand_square, poss_square), pos_board, images, pieces)
        # turn == 0 if turn == 1 else 1
    return pos_board

        
def unmake_move(move: tuple[int, int]): 
    board[move[0]] = board[move[1]]
    board[move[1]] = 0 
    turn == 0 if turn == 1 else 1 
    
def pseudo_to_legal(moves, board, screen, images):
    for space in moves:
            for dest_space in moves[space]:
                play_move((space, dest_space))
                black_moves = poss_moves(board, get_pieces(poss_board, screen, images), False)
                for move in black_moves:
                    for dest in black_moves[move]:
                            if dest == k_w:
                                print("illegal move detected")
                                unmake_move((space, dest_space))
                                moves[space].remove(dest_space)
    return moves
                



    

    

    
    
    
    
