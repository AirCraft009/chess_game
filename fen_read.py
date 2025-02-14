#pieces encoded so that color is 0 or 1 based on %2 
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


def read_Fen(fen, board):
    """
    Takes a FEN string and a dictionary representing the board, and modifies the
    board dictionary to represent the position given by the FEN string. Returns
    the modified board.

    The FEN string is a string like "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
    which describes the chess board. The string is split into rows, and each row
    is processed one character at a time. If the character is a digit, the index
    is incremented by the digit. If the character is a letter, the board is
    modified to have the piece represented by that letter at the current index.
    The mapping of letters to pieces is given by the piece_map dictionary.

    :param fen: a string describing the chess board in FEN format
    :param board: a dictionary representing the chess board the keys are spces 0-63, the values are the pieces
    :return: the modified board
    """
    index = 63
    piece_map = {
        "P": Pawn, "B": Bishop, "R": Rook, "Q": Queen, "K": King, "N": Knight,
        "p": Pawnb, "b": Bishopb, "r": Rookb, "q": Queenb, "k": Kingb, "n": Knightb
    }
    
    for row in fen.split("/"):
        for char in row: 
            if char.isdigit():
                for x in range(int(char)):
                    board[index] = 0
                    index -= 1
            else:
                if char == "K":
                    king_square_white = index
                elif char == "k":
                    king_square_black = index
                board[index] = piece_map.get(char, 0)
                index -= 1
    return board, king_square_white, king_square_black