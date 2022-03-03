import pygame as pg
vect = pg.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 5)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)

# game
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = BROWN

FONT = "ZOMBIE.ttf"

# walls
TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WALL_IMG = "Tiles/tile_367.png"

# player
PLAYER_SPEED = 300 #pixels per second, so 100 pps would take 10 seconds to cross a 1000 px screen
PLAYER_HEALTH = 100
PLAYER_IMG = "Man Blue/manBlue_gun.png"
PLAYER_ROT_SPEED = 250
PLAYER_HIT_RECT = pg.Rect(0, 0, 48, 48)
BARREL_OFFSET = vect(17, 12)
BARREL_OFFSET_2 = vect(37, 12)

# mob
MOB_IMG = "Zombie 1\zoimbie1_hold.png"
MOB_SPEEDS = [150, 100, 50, 125, 75, 25, 150]
MOB_HIT_RECT = pg.Rect(0, 0, 48, 48)
MOB_HEALTH = 100
MOB_DMG = 10
MOB_KNOCKBACK = 20
AVOID_RADIUS = 50
DETECT_RADIUS = 400

# weapon settings
BULLET_IMG = "bullet_02.png"

WEAPONS ={}

WEAPONS['pistol'] = {'speed': 500,
                    'lifetime': 1000,
                    'rate': 350,
                    'kickback': 200,
                    'spread': 5,
                    'damage': 10,
                    'size': 'lg',
                    'count': 1}

WEAPONS['shotgun'] = {'speed': 400,
                    'lifetime': 500,
                    'rate': 900,
                    'kickback': 300,
                    'spread': 30,
                    'damage': 5,
                    'size': 'sm',
                    'count': 12}

# effects
MUZZLE_FLASHES = ["muzzle_anim/flash_01.png",
                "muzzle_anim/flash_02.png",
                "muzzle_anim/flash_03.png",
                "muzzle_anim/flash_04.png",
                "muzzle_anim/flash_05.png",
                "muzzle_anim/flash_06.png"]
FLASH_DURATION = 40

BLOOD_ANIMATION = ["blood01.png",
                "blood02.png",
                "blood03.png"]
BLOOD_FRAME_DURATION = 25

BLOOD_POOL = ["blood_splatter.png",
            "blood_splatter4.png"]
BLOOD_POOL_DURATION = 10000

DAMAGE_ALPHA = [i for i in range(0, 255, 50)]
NUM_FLASHES = 4

NIGHT_COLOR = (20, 20, 20)
LIGHT_RADIUS = (500, 500)
LIGHT_MASK = "light_mask.png"

# hud
BAR_LENGTH = 100
BAR_HEIGHT = 20

# layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1
HUD_LAYER = 5

# items
ITEM_IMAGES = {'health': 'health_kit.png',
                'shotgun': 'shotgun.png',
                'pistol': 'pistol.png'}

HEALTH_PACK_AMOUNT = 20
BOB_RANGE = 15
BOB_SPEED = 0.5

# ------------------------------SOUNDS------------------------------------------
BG_MUSIC = "bg_music.mp3"

PLAYER_HIT_SOUNDS = ["pain1.wav",
                    "pain2.wav",
                    "pain3.wav",
                    "pain4.wav",
                    "pain5.wav",
                    "pain6.wav"]

ZOMBIE_MOAN_SOUNDS = ["monster-1.wav",
                    "monster-2.wav",
                    "monster-3.wav",
                    "monster-4.wav",
                    "monster-5.wav",
                    "monster-6.wav",
                    "monster-7.wav",
                    "monster-8.wav",
                    "monster-9.wav",
                    "monster-10.wav"]

ZOMBIE_HIT_SOUNDS = ["flyswatter.wav",
                    "flyswatter2.wav",
                    "flyswatter3.wav",
                    "flyswatter4.wav"]

EFFECTS_SOUNDS = {"level_start": "level_begin.wav",
                "health_up": "Replenish.wav",
                "game_over": "game-over-2.wav",
                "shotgun_pickup": "shotgun_pickup.wav",
                "win": "you_win.wav"}

WEAPON_SOUNDS = {'pistol': ['pistol.wav'],
                'shotgun': ['shotgun.wav']}