from possible_moves import *
from logic import *
from search_tree import Node, Tree
import random
from collections import Counter
from math import inf

def eval_pos(material: tuple, num_pieces, board, pieces, move, cap = 0):
    white_mat = material[0]
    black_mat = material[1]
    eval_white = white_mat/black_mat
    eval_black = black_mat/white_mat#
    center = 28
    white_pieces = {}
    black_pieces = {}
    enemy_targets = []
    for x in board:
        if board[x] == 0:
            continue
        elif board[x]%2 == 0:
            white_pieces[x] = board[x]
        elif board[x]%2 == 1:
            black_pieces[x] = board[x]
            
            
    white_moves = poss_moves_evaluation(board, True)
    for origin in white_moves:
        for dest in white_moves[origin]:
            enemy_targets.append(dest)

        
    if num_pieces > 20:

        for piece in black_pieces:
            if black_pieces[piece] == 65:

                eval_black += 6 if distance_bottom[piece] < 2 else -10
                # print(eval_black)
            elif black_pieces[piece] == 17:
                eval_black -= 5 if distance_left != 0 or distance_left[piece] != 7 else 0
            elif black_pieces[piece] == 5:
                eval_black += 5 if distance_bottom[center] +4 > distance_bottom[piece] else -3
                eval_black += 5 if distance_left != 0 and distance_left[piece] != 7 else -19
            elif black_pieces[piece] == 3:
                eval_black += 7 if distance_bottom[center] +1 > distance_bottom[piece] and distance_left[piece] > 4 and distance_right[piece] > 3 else -1.2
                eval_black += 3 if distance_bottom[center] +2 > distance_bottom[piece] and distance_left[piece] > 3 or distance_right[piece] < 2 else -1.3
                eval_black -= (piece_value[board[move[1]]] - piece_value[cap])*0.3 if distance_bottom[center] +3 < distance_bottom[piece] else +0.2
                if distance_left[piece] != 0 and distance_right[piece] != 0:
                    eval_black += 3 if board[piece +7] == 3 or board[piece + 9 ] == 3 else - 2
                    eval_black += 4 if board[piece - 7] == 3 or board[piece - 9] == 3 else -0.4
            elif black_pieces[piece] == 33:
                eval_black += 6 if distance_bottom[piece] > 4 else - 3
                queen_def = defending(get_diagonals(piece) + get_straights(piece), board, False)
                for defense in queen_def:
                    eval_black += 2
            else:
                eval_black += 7 if distance_bottom[center] +2 > distance_bottom[piece] else -5
                eval_black -= 6 if distance_bottom[piece] == 8 else - 3
            eval_black -= piece_value[board[piece]]*1.4 if piece in enemy_targets else - 1
                
    else:
        stage = 3
        
    if cap != 0:
        eval_black -= (piece_value[board[move[1]]] - piece_value[cap])*1.4 + piece_value[board[move[1]]] if move[1] in enemy_targets else -8
        # print(cap)
    else:
        eval_black -= piece_value[board[move[1]]]*1.4 if move[1] in enemy_targets else -1
            
    print(eval_black)
    return eval_white, eval_black

def calc_moves_ahead(depth, board, turn, color, pieces):
    if depth == 0:
        return 0
    best_move = None
    eval_after_move = {}
    line = []
    moves = final_moves(board, pieces, color)
    for o_space in moves:
        for dest in moves[o_space]:
            move = (o_space, dest)
            cap = play_move(move, board)
            white, black = eval_pos(calc_material(board), len(pieces), board, pieces, move, cap)
            eval_after_move[move] = black
            unplay_move(move, board, cap)
    best_eval = -inf
    equal_possess = []
    # print(mat_after_move)
    for move in eval_after_move:
        
        if round(eval_after_move[move], 3) > round(best_eval, 3):
            best_eval = eval_after_move[move]
            best_move = move
        elif round(eval_after_move[move], 3) == round(best_eval, 3):
            equal_possess.append(move)
    if len(equal_possess) > 1:
        rand_move = random.choice(equal_possess)
        if round(eval_after_move[rand_move], 3) == round(eval_after_move[best_move], 3):
            best_move = rand_move

    return best_move

def eval_all_moves(board, color, pieces, pos_board):
    eval_after_move = {}
    possible = final_moves(board, pieces, color)
    for o_space in possible:
        for dest in possible[o_space]:
            move = (o_space, dest)
            cap = play_move_piece(move, board, pieces, pos_board)
            evaluation = eval_pos(calc_material(board))
            unplay_move_piece(move, board, pieces, pos_board, cap)
            eval_after_move[move] = evaluation
    return eval_after_move

def analyze(board, turn, color, pieces, pos_board):
    eval_after_move = eval_all_moves(board, color, pieces, pos_board)
    

            

    
        
        
        

def read_position(depth, board, turn, color, pieces, pos_board):
    if depth == 0:
        return 0
    depth -= 1
    possible = final_moves(board, pieces, color)
    tree = {}
    for o_space in possible:
        tree[o_space] = {}
        for dest in possible[o_space]:
            move = (o_space, dest)
            cap = play_move_piece(move, board, pieces, pos_board)
            evaluation = eval_pos(calc_material(board))
            update_pieces(board, pieces, pos_board)
            s_line = (evaluation[1], move)
            response = final_moves(board, pieces, not color)
            for res in response:
                for dest in response[res]:
                    move = (res, dest)
                    cap = play_move_piece(move, board, pieces, pos_board)
                    evaluation = eval_pos(calc_material(board))
                    s_line = (move, evaluation[1])
                    unplay_move(move, board, cap)
                    update_pieces(board, pieces, pos_board)
            tree[o_space][dest] = s_line  
            unplay_move(move, board, cap)
            update_pieces(board, pieces, pos_board)
            
            
    best_move = max(tree, key=tree.get)
    return best_move 
                
            
            
        
    

    
    