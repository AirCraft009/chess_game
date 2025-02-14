from possible_moves import poss_moves

def check_check_white(board, board_pieces):
    black_moves = poss_moves(board, board_pieces, False)
    for x in black_moves:
        for y in board[x]:
            if board[y] == 64:
                return True
    return False

def check_check_black(board, board_pieces):
    white_moves = poss_moves(board, board_pieces, True)
    for x in white_moves:
        for y in white_moves[x]:
            if board[y] == 65:
                return True
    return False

def is_checked(board, board_pieces):
    white_checked = check_check_white(board, board_pieces)
    black_checked = check_check_black(board, board_pieces)
    return white_checked, black_checked

def eval_pos(board, material: tuple):
    white_mat = material[0]
    black_mat = material[1]
    eval_white = white_mat/black_mat
    eval_black = black_mat/white_mat
    return eval_white, eval_black

    
    