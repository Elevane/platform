import pygame, math
from obo_player import *
from obo_wall import * 
import obo_game_values as obo_game_values
import obo_generator as obo_generator


def generate_sprites(game):
    sprite_map = []
    cave_generated = obo_generator.CaveGenerator(80,80).generate_cave()
    for i, row in enumerate(cave_generated):
        for y, cell in enumerate(row):
            if cell == obo_game_values.BLOCK_WALL:
                sprite_map.append(Platform(game, i *obo_game_values.BLOCK_SIZE , y* obo_game_values.BLOCK_SIZE, obo_game_values.BLOCK_SIZE, obo_game_values.BLOCK_SIZE, obo_game_values.BLACK_GREEN))
            else:
                sprite_map.append(Platform(game, i*obo_game_values.BLOCK_SIZE, y*obo_game_values.BLOCK_SIZE, obo_game_values.BLOCK_SIZE, obo_game_values.BLOCK_SIZE, obo_game_values.LIGHT_BLACK_GREEN))
    return sprite_map


class Game:

    def __init__(self, title = None, fps = 60):
        pygame.init()
        self.running = True
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.player = Player(self, 50, 50)
        self.camera_x = math.trunc(self.width /2)
        self.camera_y = math.trunc(self.width /2)
        self.clock = pygame.time.Clock()
        self.walls = generate_sprites(self)
        self.fps = fps     
        pygame.display.set_caption(title or "title")


 

    def events(self):
        for event in pygame.event.get():   
            if event.type == pygame.QUIT:
                self.running = False    
            if event.type == pygame.VIDEORESIZE:
            # There's some code to add back window content here.
                self.screen = pygame.display.set_mode((event.w, event.h),
                                              pygame.RESIZABLE)                 
        keys=pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.player.move(direction=obo_game_values.RIGHT)
        if keys[pygame.K_LEFT]:
            self.player.move(direction=obo_game_values.LEFT)
        if keys[pygame.K_UP]:
            self.player.move(direction=obo_game_values.UP)
        if keys[pygame.K_DOWN]:
            self.player.move(direction=obo_game_values.DOWN)
        

    def update(self):
        self.clock.tick(self.fps)
        pygame.display.update()


    def draw(self):
        self.screen.fill(obo_game_values.BLACK_GREEN)    
        for wall in self.walls:
            wall.draw()
        ##self.player.draw()


    def run(self):
        while self.running:         
            self.events()
            self.draw()
            self.update()


if __name__ == "__main__":
    game = Game("platformer")
    game.run()