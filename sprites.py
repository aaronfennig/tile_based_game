import pygame as pg
from  itertools import chain
from random import random, uniform, choice, randint
from settings import *
from tilemap import collide_hit_rect
# for easing functions. in this case used to make the health pack bob up and down
import pytweening as tween
vect = pg.math.Vector2

def colide_with_walls(sprite, group, dir):
    if dir == "x":
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left -sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == "y":
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top -sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        # print(self.rect.center)
        self.rect.center = (x, y)
        # print(self.rect.center)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vect(0, 0)
        self.pos = vect(x, y) #MUST MULTILPLY BY TILESIZE IF USING TXT MAP
        self.rot = 0
        self.last_shot = 0
        self.health = PLAYER_HEALTH
        # self.weapon = ["pistol", "shotgun"]
        self.weapons = ["pistol"]
        self.weapon = "pistol"
        self.swap_buffer = 0
        self.damaged = False

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vect(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vect(PLAYER_SPEED, 0).rotate(-self.rot)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vect(-PLAYER_SPEED / 2, 0).rotate(-self.rot)
        # the below code was no longer needed once we switched to rotating our character vs moving up, down, left, right normally
        # if self.vel.x != 0 and self.vel.y != 0:
        #     self.vel *= 0.7071
        if keys[pg.K_SPACE]:
            self.shoot()
        if keys[pg.K_z] or keys[pg.K_TAB]:
            self.swap_weapon()

    # AT SOME POINT TRY TO MAKE THIS WORK WITH ITERTOOLS IMPORT (itertools.cycle(self.weapons)) TO SEE IF IT IS MORE EFFICIENT THAN THE MANUAL SOLUTION CURRENTLY IMPLEMENTED
    def swap_weapon(self):
        restart = False
        now = pg.time.get_ticks()
        if now - self.swap_buffer > 500:
            self.swap_buffer = now
            for idx in range(len(self.weapons)):
                print("idx pos is:", idx, ", wepons in inventory are:", self.weapons)
                if self.weapons[idx] == self.weapon:
                    try:
                        self.weapon = self.weapons[idx + 1]
                        break
                    except IndexError:
                        restart = True
                    if restart == True:
                        self.weapon = self.weapons[0]
            print(self.weapon, "is equipped")

    def hit(self):
        self.damaged = True
        self.damage_alpha = chain(DAMAGE_ALPHA * NUM_FLASHES)

    def shoot(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_z]:
            print("exit function to prioritize weapon swap")
            return None
        now = pg.time.get_ticks()
        if now - self.last_shot >= WEAPONS[self.weapon]['rate']:
            self.last_shot = now
            dir = vect(1, 0).rotate(-self.rot)
            pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
            self.vel = vect(-WEAPONS[self.weapon]['kickback'], 0).rotate(-self.rot)
            keys = pg.key.get_pressed()
            if keys[pg.K_UP]:
                pos = self.pos + BARREL_OFFSET_2.rotate(-self.rot)
            for i in range(WEAPONS[self.weapon]['count']):
                spread = uniform(-WEAPONS[self.weapon]['spread'], WEAPONS[self.weapon]['spread'])
                Bullet(self.game, pos, dir.rotate(spread), WEAPONS[self.weapon]["damage"])
            MuzzleFlash(self.game, pos)
            sound = choice(self.game.weapon_shot_sounds[self.weapon])
            # if sound.get_num_channels() > 2:
            #     sound.stop()
            sound.play()

    def add_health(self, amount):
        self.health += amount
        if self.health > PLAYER_HEALTH:
            self.health = PLAYER_HEALTH

    def update(self):
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        # print(self.rot)
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        # only ran when self.damaged flag is raised via self.hit function
        if self.damaged:
            print("*********************DAMAGED**************")
            try:
                print([DAMAGE_ALPHA])
                self.image.fill((255, 0, 0, next(self.damage_alpha)), special_flags = pg.BLEND_RGBA_MULT)
            except:
                self.damaged = False

        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        # code is using self.y (and self.x) instead of self.rect.y because .rect stores intigers only, and being as that these will be floating points, we would lose alot of information, so this value will be passed to self.rect.y in another step below
        self.hit_rect.centerx = self.pos.x
        colide_with_walls(self, self.game.walls, "x")
        self.hit_rect.centery = self.pos.y
        colide_with_walls(self, self.game.walls, "y")
        self.rect.center = self.hit_rect.center

# OLD WALLS CODE USED FOR MAP TXT FILES, NOT TMX FILES
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = WALL_LAYER
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# CODE FOR WALLS (AND OTHER OBSTACLES) USING TMX MAPS
class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = MOB_HIT_RECT.copy() # so each member of the mob gets a hit rect
        self.hit_rect.center = self.rect.center
        self.pos = vect(x, y) #IF USING TXT MAP POS MUST BE MULTIPLIED BY TILESIZE
        self.vel = vect(0, 0)
        self.acc = vect(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = MOB_HEALTH
        self.speed = choice(MOB_SPEEDS)
        self.target = game.player

    def draw_health(self):
        if self.health > 60:
            color = GREEN
        elif self.health > 30:
            color = YELLOW
        else:
            color = RED
        width = int(self.rect.width * self.health / MOB_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < MOB_HEALTH:
            pg.draw.rect(self.image, color, self.health_bar)
        
    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def update(self):
        target_distance =  self.target.pos - self.pos
        if target_distance.length_squared() < DETECT_RADIUS **2:
            if random() < 0.002:
                choice(self.game.zombie_moan_sounds).play()
            self.rot = (target_distance).angle_to(vect(1, 0))
            self.image = pg.transform.rotate(self.game.mob_img, self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.acc = vect(1, 0).rotate(-self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(self.speed)
            self.acc += self.vel * -1 # adds friction to zombie movement
            # print(self.acc)
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 *self.acc *self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            colide_with_walls(self, self.game.walls, "x")
            self.hit_rect.centery = self.pos.y
            colide_with_walls(self, self.game.walls, "y")
        if self.health <= 0:
            choice(self.game.zombie_hit_sounds).play()
            BloodPool(self.game, self.pos)
            self.kill()

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, damage):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_imgs[WEAPONS[self.game.player.weapon]['size']]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect.copy()
        self.pos = vect(pos)
        self.rect.center = pos
        self.vel = dir * WEAPONS[self.game.player.weapon]['speed'] * uniform(0.9, 1.1)
        self.spawn_time = pg.time.get_ticks()
        self.damage = damage

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > WEAPONS[self.game.player.weapon]['lifetime']:
            self.kill()

class MuzzleFlash(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites, game.effects
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        size = randint(20, 50)
        self.image = pg.transform.scale(choice(game.gun_flashes), (size, size))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > FLASH_DURATION:
            self.kill()

class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        self._layer = ITEMS_LAYER
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = type
        self.image = game.item_images[type]
        if self.type == "health":
            self.image = pg.transform.scale(game.item_images[type], (32, 32))
        if self.type == "shotgun":
            self.image = pg.transform.scale(game.item_images[type], (64, 32))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.hit_rect = pg.Rect(0, 0, 24, 24)
        self.hit_rect.center = self.rect.center
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1

    def update(self):
        # bobbing motion
        offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step = 0
            self.dir *= -1

class BloodAnimation(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites, game.effects
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.size = randint(80, 200)
        self.angle = randint(0,359)
        self.image = self.game.blood_anim[0].copy()
        self.image = pg.transform.scale(self.image, (self.size,self.size))
        self.image = pg.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()
    def update(self):
        time = pg.time.get_ticks() - self.spawn_time
        if time > BLOOD_FRAME_DURATION and time < BLOOD_FRAME_DURATION * 2:
            self.image = self.game.blood_anim[1].copy()
            self.image = pg.transform.scale(self.image, (self.size, self.size))
            self.image = pg.transform.rotate(self.image, self.angle)
            # print(time)
        elif time > BLOOD_FRAME_DURATION * 2 and time < BLOOD_FRAME_DURATION * 3:
            self.image = self.game.blood_anim[2].copy()
            self.image = pg.transform.scale(self.image, (self.size,self.size))
            self.image = pg.transform.rotate(self.image, self.angle)
            # print(time)
        elif time > BLOOD_FRAME_DURATION *3:
            # print(time)
            self.kill()

class BloodPool(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = ITEMS_LAYER
        self.groups = game.all_sprites, game.effects
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        size = randint(40, 120)
        angle = randint(0,359)
        self.image = choice(game.blood_splatter).copy()
        self.image = pg.transform.scale(self.image, (size, size))
        self.image = pg.transform.rotate(self.image, (angle))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()
    # used to make blood disapear after a set amount of time
    # def update(self):
    #     time = pg.time.get_ticks() - self.spawn_time
    #     if time > BLOOD_POOL_DURATION:
    #         self.kill()