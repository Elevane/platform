import pygame
import game_values

class Platform():
    
    def __init__(self, game, x, y , width, height,color, collidable=False) :
        self.game = game
        self.x = x
        self.y = y 
        self.width = width
        self.height = height
        self.color = color
        self.collidable=collidable
        self.rect = pygame.Rect(self.x, self.y, game_values.BLOCK_SIZE, game_values.BLOCK_SIZE)

    def draw(self):   
        pygame.draw.rect(self.game.screen, self.color, self.rect)