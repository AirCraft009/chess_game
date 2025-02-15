from possible_moves import final_moves
from logic import play_move, play_move_piece, unplay_move, calc_material, update_pieces
from search_tree import Node, Tree

def eval_pos(material: tuple):
    white_mat = material[0]
    black_mat = material[1]
    eval_white = white_mat/black_mat
    eval_black = black_mat/white_mat
    
    return eval_white, eval_black

def calc_moves_ahead(depth, board, turn, color, pieces):
    if depth == 0:
        return 0
    best_move = None
    mat_after_move = {}
    line = []
    moves = final_moves(board, pieces, color)
    for o_space in moves:
        for dest in moves[o_space]:
            move = (o_space, dest)
            cap = play_move(move, board)
            mat_after_move[move] = calc_material(board)
            unplay_move(move, board, cap)
    best_eval = 0
    # print(mat_after_move)
    for move in mat_after_move:
        white, black = eval_pos(mat_after_move[move])
        if black > best_eval:
            best_eval = black
            best_move = move
    return best_move

def 3_moves_ahead(depth, board, turn, color, pieces):

    
        
        
        

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
                
            
            
        
    

    
    