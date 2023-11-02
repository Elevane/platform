import pygame
from BSd.bsd_player import *
from BSd.bsd_wall import * 
import game_values
import BSd.bsd_generator as bsd_generator

class Game:

    def __init__(self, title = None, fps = 60):
        pygame.init()
        self.running = True
        self.width, self.height = 1200, 900
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.player = Player(self, 50, 50)
        self.clock = pygame.time.Clock()
        self.walls = bsd_generator.Map(60,60)
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
        if keys[pygame.K_RIGHT] and checkCollision():
            self.player.move(direction=game_values.RIGHT)
        if keys[pygame.K_LEFT]:
            self.player.move(direction=game_values.LEFT)
        if keys[pygame.K_UP]:
            self.player.move(direction=game_values.UP)
        if keys[pygame.K_DOWN]:
            self.player.move(direction=game_values.DOWN)
        

    def update(self):
        self.clock.tick(self.fps)
        pygame.display.update()


    def draw(self):
        self.screen.fill((216,243,220))    
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