# Video link: https://youtu.be/3UxnelT9aCo
# Sounds (c) by Michel Baradari apollo-music.de
import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *
from hud import *
from random import choice

class Game:
    def __init__(self):
        # tweek these settings to adjust the sound buffer...must be in increments of 1028
        # pg.mixer.pre_init(44100, -16, 1, 2048)
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def draw_text(self, text, font_name, size, color, x, y, align = "nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_data(self):

        # game folders
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, "imgs\PNG")
        # map folder has to be attached to the game class, because we dont load the map in the load_data function, but in the new function
        self.map_folder = path.join(game_folder, "maps")
        items_folder = path.join(game_folder, "imgs\PNG\items")
        sounds_folder = path.join(game_folder, "sounds")
        music_folder = path.join(game_folder, "music")
        blood_anim_folder = path.join(game_folder, "imgs/PNG/blood_anim")
        fonts_folder = path.join(game_folder, "fonts")

        # load menu assets
        self.main_font = path.join(fonts_folder, FONT)
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))

        # TXT MAP LOAD
        # self.map = Map(f"{game_folder}\maps\map3.txt")

        # load images
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.player_img = pg.transform.scale(self.player_img, (48,56))

        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))

        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.mob_img = pg.transform.scale(self.mob_img, (48, 56))

        self.bullet_imgs = {}
        self.bullet_imgs["base"] = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.bullet_imgs['lg'] = pg.transform.scale(self.bullet_imgs['base'], (10, 10))
        self.bullet_imgs['sm'] = pg.transform.scale(self.bullet_imgs['lg'], (6, 6))

        self.blood_splatter =[]
        for img in BLOOD_POOL:
            bs = pg.image.load(path.join(img_folder, img)).convert_alpha()
            self.blood_splatter.append(bs)

        self.gun_flashes = []
        for x in range(len(MUZZLE_FLASHES)):
            self.gun_flashes.append(pg.image.load(path.join(img_folder, MUZZLE_FLASHES[x])).convert_alpha())

        self.item_images = {}
        for item in ITEM_IMAGES:
            it = self.item_images[item] = pg.image.load(path.join(items_folder, ITEM_IMAGES[item])).convert_alpha()
            print(self.item_images[item])
            print(self.item_images[item].get_size())

        # load animation
        self.blood_anim = []
        for img in BLOOD_ANIMATION:
            ba = pg.image.load(path.join(blood_anim_folder, img)).convert_alpha()
            ba = pg.transform.scale(ba, (128, 128))
            self.blood_anim.append(ba)

        # night mode and lighting effects for night mode
        self.fog = pg.Surface((WIDTH, HEIGHT))
        self.fog.fill(NIGHT_COLOR)

        self.light_mask = pg.image.load(path.join(img_folder, LIGHT_MASK)).convert_alpha()
        self.light_mask = pg.transform.scale(self.light_mask, LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()

        # sound loading
        # load BG music
        pg.mixer.music.load(path.join(music_folder, BG_MUSIC))

        # load all sound effects
        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
            self.effects_sounds[type] = pg.mixer.Sound(path.join(sounds_folder, EFFECTS_SOUNDS[type]))
            if type == "level_start":
                self.effects_sounds[type].set_volume(0.3)
            if type == "health_up":
                self.effects_sounds[type].set_volume(0.4)
            if type == "shotgun_pickup":
                self.effects_sounds[type].set_volume(0.4)

        self.weapon_shot_sounds = {}
        for weapon in WEAPON_SOUNDS:
            self.weapon_shot_sounds[weapon] = []
            for snd in WEAPON_SOUNDS[weapon]:
                s = pg.mixer.Sound(path.join(sounds_folder, snd))
                if snd == 'pistol':
                    s.set_volume(0.2)
                self.weapon_shot_sounds[weapon].append(s)

        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            phs = pg.mixer.Sound(path.join(sounds_folder, snd))
            phs.set_volume(0.2)
            self.player_hit_sounds.append(phs)

        self.zombie_hit_sounds = []
        for snd in ZOMBIE_HIT_SOUNDS:
            zhs = pg.mixer.Sound(path.join(sounds_folder, snd))
            zhs.set_volume(0.2)
            self.zombie_hit_sounds.append(zhs)

        self.zombie_moan_sounds = []
        for snd in ZOMBIE_MOAN_SOUNDS:
            zms = pg.mixer.Sound(path.join(sounds_folder, snd))
            zms.set_volume(0.3)
            self.zombie_moan_sounds.append(zms)

    def new(self):
        #initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()

        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.effects = pg.sprite.Group()

        # TMX MAP LOAD
        self.map = TiledMap(path.join(self.map_folder, "test_run.tmx"))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        # OLD CODE TO LOAD TXT MAPS, INSTEAD OF TMX MAPS
        # for row, tiles in enumerate(self.map.data):
        #     for column, tile in enumerate(tiles):
        #         if tile == '1':
        #             Wall(self, column, row)
        #         if tile == 'm':
        #             self.mob = Mob(self, column, row)
        #         if tile == 'p':
        #             self.player = Player(self, column, row)

        for tile_object in self.map.tmxdata.objects:
            obj_center = vect(tile_object.x + tile_object.width / 2,
                                tile_object.y + tile_object.height / 2)
            # print(tile_object)
            if tile_object.name == "player":
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == "wall":
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == "zombie":
                Mob(self, obj_center.x, obj_center.y)
            if tile_object.name in ['health', 'shotgun']:
                Item(self, obj_center, tile_object.name)

        self.camera = Camera(self.map.width, self.map.height)
        self.effects_sounds["level_start"].play()
        self.is_draw_debug = False
        self.isPause = False
        self.isNight = True

    def run(self):
        self.isRun = True
        pg.mixer.music.play(loops = -1)
        pg.mixer.music.set_volume(0.4)
        while self.isRun:
            self.dt = self.clock.tick(FPS) / 1000
            # delta time is ~ 0.0165 at 60 fps  or   (16.5/1000)...so, the change in time(delta time) is 16.5 milliseconds/frame. (16.5 milliseconds * 60 frames ~ 1 second)
            # print("delta time is:", self.dt)
            self.events()
            if not self.isPause:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # this line runs the update function for all sprites in a loop
        self.all_sprites.update()
        # updates the camera, so the player is at the center of the screen and all sprites spawn at the correct location relative to player position... updates every frame
        self.camera.update(self.player)

        if len(self.mobs) == 0:
            self.isRun = False

        # player hits item
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == "health" and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.player.add_health(HEALTH_PACK_AMOUNT)
                self.effects_sounds["health_up"].play()
            if hit.type == "shotgun":
                hit.kill()
                self.player.weapons.append("shotgun")
                print(self.player.weapons)
                self.effects_sounds["shotgun_pickup"].play()

        # player runs into mob
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            self.player.health -= MOB_DMG
            hit.vel = vect(0, 0)
            if self.player.health <= 0:
                self.isRun = False
        if hits:
            self.player.hit()
            self.player.pos += vect(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
            choice(self.player_hit_sounds).play()

        # bullet hits mob
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        # hit represents an individual zombie being hit
        for hit in hits:

            BloodAnimation(self, hit.pos)

            # below is the first method for doling out damage, which is no longer accurate now that there is more htna one weapon in play
            # hit.health -= WEAPONS[self.player.weapon]['damage'] * len(hits[hit])

            # bullet represents an individual bullet hitting an individual zombie. this is the updated method for doling out damage that takes into account a weapon swap while ammo is in motion
            for bullet in hits[hit]:
                hit.health -= bullet.damage
                print(f"damage before correction reguarding the switching of weapons:   {WEAPONS[self.player.weapon]['damage']}    vs correct damage for bullet:   {bullet.damage}")

            # this stops the zombie in its tracks momentarily for evewry bullet that hits it
            hit.vel = vect(0, 0)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def render_fog(self):
        self.light_rect.center = self.camera.apply(self.player).center
        self.fog.blit(self.light_mask, self.light_rect)
        self.screen.blit(self.fog, (0, 0), special_flags = pg.BLEND_MULT)

    def draw(self):
        pg.display.set_caption("FPS: {:.2f}".format(self.clock.get_fps()))
        # self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        weap_wid = self.item_images[self.player.weapon].get_size()
        self.screen.blit(self.item_images[self.player.weapon], (960 - weap_wid[0]/2, 10))

        # self.draw_grid()

        # ATTEMPT TO GET A WORKING HUD CLASS.NOT GOING SO WELL...
        # hud = Hud(self)
        # hud.update()
        # hud.draw_weapon()

        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()

            self.screen.blit(sprite.image, self.camera.apply(sprite))
            
            if self.is_draw_debug and not self.effects:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)

        if self.is_draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)

        if self.isNight:
            self.render_fog()

        draw_player_health(self.screen, 10, 20, self.player.health / PLAYER_HEALTH)

        self.draw_text("Zombies Remaining", self.main_font, 30, WHITE, WIDTH / 2, 30, align = "center")
        self.draw_text("{}".format(len(self.mobs)), self.main_font, 30, RED, WIDTH / 2 + 180, 30, align = "center")
        
        if self.isPause:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("PAUSED", self.main_font, 105, RED, WIDTH / 2, HEIGHT / 2, align = "center")

        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.is_draw_debug = not self.is_draw_debug
                if event.key == pg.K_p:
                    self.isPause = not self.isPause
                    if self.isPause == True:
                        print("GAME IS PAUSED")
                    if self.isPause == False:
                        print("PLAYER UNPAUSED THE GAME")
                if event.key == pg.K_n:
                    self.isNight = not self.isNight
                    print(f"night mode is {self.isNight}")

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        self.screen.fill(BLACK)
        if len(self.mobs) > 0:
            self.effects_sounds["game_over"].play()
            self.draw_text("GAME OVER", self.main_font, 100, RED, WIDTH / 2, HEIGHT / 3, align = "center")
        else:
            self.effects_sounds["win"].play()
            self.draw_text("YOU WON!", self.main_font, 100, GREEN, WIDTH / 2, HEIGHT / 3, align = "center")
        self.draw_text("Press a key to restart", self.main_font, 75, WHITE, WIDTH / 2, HEIGHT * 3 / 4, align = "center")
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

if __name__ == "__main__":
    gm = Game()
    gm.show_start_screen
    while True:
        gm.new()
        gm.run()
        gm.show_go_screen()