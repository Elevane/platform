import pygame
import obo_game_values as obo_game_values

class Platform():
    
    def __init__(self, game, x, y , width, height,color, collidable=False) :
        self.game = game
        self.x = x
        self.y = y 
        self.width = width
        self.height = height
        self.color = color
        self.collidable=collidable
        self.rect = pygame.Rect(self.x - self.game.camera_x, self.y - self.game.camera_y, obo_game_values.BLOCK_SIZE, obo_game_values.BLOCK_SIZE)

    def draw(self):
        self.rect = pygame.Rect(self.x - self.game.camera_x, self.y - self.game.camera_y, obo_game_values.BLOCK_SIZE, obo_game_values.BLOCK_SIZE)
        pygame.draw.rect(self.game.screen, self.color, self.rect)