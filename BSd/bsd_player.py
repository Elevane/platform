import pygame
import game_values

class Player():

    def __init__(self, game, x , y):
        self.color = (82, 183, 136)
        self.game = game
        self.x = x
        self.y = y
        self.jump_count = 10
        self.is_jumping = False

    def draw(self):
        self.update()
        self.rect = pygame.Rect(self.x, self.y, game_values.BLOCK_SIZE, game_values.BLOCK_SIZE)
        self.area_of_feet_collision = pygame.Rect(self.x - 3, (self.y -  3), game_values.BLOCK_SIZE + 6, game_values.BLOCK_SIZE + 6 )
        pygame.draw.rect(self.game.screen, self.color, self.rect)
        pygame.draw.rect(self.game.screen, (230,57, 70), self.area_of_feet_collision, 2)

    def update(self):       
        pass

    def collide(self, rect):
        return self.area_of_feet_collision.colliderect(rect)
    
    
    def move(self, direction):
        if direction == game_values.RIGHT:
            self.x += 5
        elif direction == game_values.LEFT:
            self.x -= 5
        elif direction == game_values.UP:
            self.y -= 5
        elif direction == game_values.DOWN:
            self.y += 5
    