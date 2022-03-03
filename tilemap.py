import pygame as pg
from settings import *
import pytmx
from pytmx import load_pygame

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, "rt") as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

class TiledMap:
    def __init__(self, filename):
        tmx = pytmx.load_pygame(filename, pixelalpha = True)
        self.width = tmx.width * tmx.tilewidth
        self.height = tmx.height * tmx.tileheight
        self.tmxdata = tmx
    def render(self, surface):
        # the following command is used to find the image that goes with a certain tile in the tsx file
        t_i = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = t_i(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))
    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        # print("entity is:", entity.rect.move(self.camera.topleft))
        # print("camera.topleft is:", self.camera.topleft)
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)
        # print(x,y)
        # print("self.camera is", pg.Rect(x, y, self.width, self.height))
        # limit scrolling to the map size (we do not want to have areas that are not on the map to show up on our screen....CODE BELOW)
        x = min(0, x) # left
        y = min(0, y) # top
        # print(self.width, x, y)
        x = max(-(self.width - WIDTH), x) # right
        y = max(-(self.height - HEIGHT), y) # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)
