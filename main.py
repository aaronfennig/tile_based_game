# Video link: https://youtu.be/3UxnelT9aCo
import pygame as pg
import sys
from os import path
from settings import *
from sprites import *

class Game:
    def __init__(self):
        pg.init()
        self.screen =pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
    
    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        with open(path.join(game_folder, "map.txt")) as f:
            for line in f:
                self.map_data.append(line)
    
    def new(self):
        #initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()

        for row, tiles in enumerate(self.map_data):
            for column, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, column, row)
                if tile == 'p':
                    self.player = Player(self, column, row)

    def run(self):
        self.isRun = True
        while self.isRun:
            self.dt = self.clock.tick(FPS) / 1000
            # delta time is ~ 0.0165 at 60 fps  or   (16.5/1000)
            # print("delta time is:", self.dt)
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # updates a portion of the game loop
        self.all_sprites.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

gm = Game()
gm.show_start_screen
while True:
    gm.new()
    gm.run()
    gm.show_go_screen