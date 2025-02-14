import pygame

image_path = "images/"

def init_images():
    images = [
        pygame.image.load(image_path + "white_pawn.png").convert_alpha(),
        pygame.image.load(image_path + "black_pawn.png").convert_alpha(),
        pygame.image.load(image_path + "white_knight.png").convert_alpha(),
        pygame.image.load(image_path + "black_knight.png").convert_alpha(),
        pygame.image.load(image_path + "white_bishop.png").convert_alpha(),
        pygame.image.load(image_path + "black_bishop.png").convert_alpha(),
        pygame.image.load(image_path + "white_rook.png").convert_alpha(),
        pygame.image.load(image_path + "black_rook.png").convert_alpha(),
        pygame.image.load(image_path + "white_queen.png").convert_alpha(),
        pygame.image.load(image_path + "black_queen.png").convert_alpha(),
        pygame.image.load(image_path + "white_king.png").convert_alpha(),
        pygame.image.load(image_path + "black_king.png").convert_alpha(),
        pygame.image.load(image_path + "icon.png").convert_alpha()
    ]
    return images