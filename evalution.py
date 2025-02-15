from possible_moves import final_moves
from logic import play_move, unplay_move, calc_material 

def eval_pos(material: tuple):
    white_mat = material[0]
    black_mat = material[1]
    eval_white = white_mat/black_mat
    eval_black = black_mat/white_mat
    return eval_white, eval_black

def calc_moves_ahead(depth, board, turn, color, pieces, moves_prefv = None):
    if depth == 0:
        return 0
    cap_list = []
    if moves_prefv != None:
        for move in moves_prefv:
            prev_cap =play_move(move, board)
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
    print(mat_after_move)
    for move in mat_after_move:
        white, black = eval_pos(mat_after_move[move])
        if black > best_eval:
            best_eval = black
            best_move = move
    unplay_move(move, board, cap)
    return best_move
            
            
            
        
    

    
    