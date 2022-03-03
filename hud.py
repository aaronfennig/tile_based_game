import pygame as pg
from sprites import *
from settings import *
from main import *

def draw_player_health(surface, x, y, pct_health):
    if pct_health < 0:
        pct_health = 0
    fill = pct_health * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct_health > 0.6:
        color = GREEN
    elif pct_health > 0.3:
        color = YELLOW
    else:
        color = RED
    pg.draw.rect(surface, color, fill_rect)
    pg.draw.rect(surface, WHITE, outline_rect, 2)



# FIGURE OUT WHAT I AM DOING WRONG TO TURN THIS INTO A CLASS, TO PUT ALL HUD ELEMENTS IN A TOP LAYER
class Hud:
    def __init__(self, game):
        self._layer = HUD_LAYER
        self.game = game
        self.image = game.item_images[game.player.weapon]
    
    def update(self):
        self.image = self.game.item_images[self.game.player.weapon]

    def draw_weapon(self):
        # print(f"#################{game.player.weapon}################")
        print(f"#################{self.image}################")
        self.game.screen.blit(self.image, (896, 10))
        pg.display.flip()
        # self.draw_text("PAUSED", self.main_font, 105, RED, WIDTH / 2, HEIGHT / 2, align = "center")