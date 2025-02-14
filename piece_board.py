import pygame
pieces = {}
            

class Piece(object):
    def __init__(self, x, y, color, type, step, value, image, space, screen):
        self.x = x
        self.y = y
        self.color = color
        self.type = type
        self.step = step
        self.value = value
        self.image = image
        self.space = space
        self.selected = False
        self.screen = screen
        self.moved = False
    
    def render(self, depth = 1):
        	
        self.screen.blit(self.image, (self.x, self.y))
        if self.selected:
            pygame.draw.rect(self.screen, ("red"), (self.x, self.y, 100, 100), 5)
            pygame.display.update()
            
    def move(self, move: tuple[int, int], pos_board):
        dest_space = move[1]
        pos = pos_board[dest_space]
        self.x = pos[0]
        self.y = pos[1]
        self.render()
        self.moved = True
        
def get_pieces():
    return pieces
        

def piece_board(board: dict, pos_board, screen, images):
    """
    Populates the allocated_board dictionary with Piece objects, given a board and piece images.
    using th piece_map dictionary and because it is a O(1) operation to look up a value 
    it is very efficient

    Parameters:
        board (dict): A dictionary representing the chess board, with keys as the space number and values as the piece that is on that space.
        allocated_board (dict): An empty dictionary to store the created Piece objects.

    Returns:
        allocated_board (dict): The populated allocated_board dictionary.
    """
    pieces.clear()

    piece_map = {
        2:  ("white", 1, 1, images[0]),
        3:  ("black", 1, 1, images[1]),
        4:  ("white", 2, 2, images[2]),
        5:  ("black", 2, 2, images[3]),
        8:  ("white", 3, 3, images[4]),
        9:  ("black", 3, 3, images[5]),
        16: ("white", 4, 4, images[6]),
        17: ("black", 4, 4, images[7]),
        32: ("white", 5, 5, images[8]),
        33: ("black", 5, 5, images[9]),
        64: ("white", 6, 6, images[10]),
        65: ("black", 6, 6, images[11]),
    }
    
    for x, piece in board.items():
        if piece in piece_map:
            color, value1, value2, image = piece_map[piece]
            pieces[x] = Piece(pos_board[x][0], pos_board[x][1], color, piece, value1, value2, image, x, screen)
    return pieces
    