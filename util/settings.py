TILE_SIZE = 52
SPRITE_SIZE = 104
SCALE = 16
BATTLE_SCREEN_WIDTH = 1198
BATTLE_SCREEN_HEIGHT = 1000
DIAMETER = BATTLE_SCREEN_WIDTH
CENTER_X = BATTLE_SCREEN_WIDTH/2
CENTER_Y = BATTLE_SCREEN_HEIGHT/2

#SCREEN_WIDTH = 900
#SCREEN_HEIGHT = 900

SCREEN_WIDTH = 1198
SCREEN_HEIGHT = 768 

PLAYER_SPRITE_SIZE_X = 288
PLAYER_SPRITE_SIZE_Y = 128

BULLET_SPRITE_SIZE_X = 48
BULLET_SPRITE_SIZE_Y = 32

ENEMY_SPRTE_SIZE_X = 24
ENEMY_SPRTE_SIZE_Y = 32

ENEMY_SPRITE_MULTIPLIER = 3.3

RIGHT = 0
LEFT = 1
TOP = 2
BOTTOM = 3


# Resources
RESOURCE_PATH = "./resources/"
SPRITES_PATH = RESOURCE_PATH + "sprites/"
MIXER_PATH = RESOURCE_PATH + "mixer/"
MUSIC_PATH = MIXER_PATH + "music/"
SOUND_PATH = MIXER_PATH + "sound/"
BACKGROUND_PATH = RESOURCE_PATH + "background/"


SHOOT_PATH_1 = SOUND_PATH + "laser_018.wav"
SHOOT_PATH_2 = SOUND_PATH + "laser_022.wav"
SHOOT_PATH_3 = SOUND_PATH + "laser_045.wav"
SHOOT_PATH_4 = SOUND_PATH + "laser_050.wav"

DEATH_PATH_1 = SOUND_PATH + "hurt_016.wav"
DEATH_PATH_2 = SOUND_PATH + "hurt_020.wav"
DEATH_PATH_3 = SOUND_PATH + "hurt_006.wav"
DEATH_PATH_4 = SOUND_PATH + "hurt_007.wav"

SHOOT_BLOCKED_PATH_1 = SOUND_PATH + "hit_029.wav"
SHOOT_BLOCKED_PATH_2 = SOUND_PATH + "hit_040.wav"
SHOOT_BLOCKED_PATH_3 = SOUND_PATH + "hit_066.wav"

OPTION_CHANGE_PATH_1 = SOUND_PATH + "menu_001.wav"

OPTION_SELECTED_PATH_1 = SOUND_PATH + "menu_062.wav"

BACK_PATH_1 = SOUND_PATH + "menu_118.wav"

PAUSE_PATH_1 = SOUND_PATH + "pause.wav"

UNPAUSE_PATH_1 = SOUND_PATH + "unpause.wav"

GAME_OVER_PATH_1 = SOUND_PATH + "game_over.wav"


BG_MUSIC_AUDIO_0 = MUSIC_PATH + "spells.ogg"
BG_MUSIC_AUDIO_1 = MUSIC_PATH + "8bit.ogg"
BG_MUSIC_AUDIO_2 = MUSIC_PATH + "night.ogg"

PLAYER_CENTER = (BATTLE_SCREEN_WIDTH/2,BATTLE_SCREEN_HEIGHT/2 - (TILE_SIZE + TILE_SIZE/2) + 4)
PLAYER_HITBOX = (250,175,-500,-175)

SHIELD_CENTER_LEFT = (BATTLE_SCREEN_WIDTH/2 - 5,BATTLE_SCREEN_HEIGHT/2 - (TILE_SIZE + TILE_SIZE/2) + 4)
SHIELD_CENTER_RIGHT = (BATTLE_SCREEN_WIDTH/2 + 5,BATTLE_SCREEN_HEIGHT/2 - (TILE_SIZE + TILE_SIZE/2) + 4)
SHIELD_HITBOX_RIGHT = (300,155,-500,-155)
SHIELD_HITBOX_LEFT = (200,155,-500,-155)

RESPAWN_COOLDOWN = 1000
SHOOT_RESPAWN_COOLDOWN = 750
RESPAWN_PROB = 0.1
ENEMY_VELOCITY = 2.75
BULLET_VELOCITY = 5
ROTATE_VELOCITY = 2
SHOOT_VELOCITY = 6.5

SHOOT_COOLDOWN = 0.75
ROTATE_COOLDOWN = 2
BLOCK_COOLDOWN = 0.8

MAX_ENEMIES = 4

TRAINING = False
LEARNING = False

SPEED = 1000

CURRENT_BACKGROUND = 'bg_01'

DEBUG_MODE = False

# DANGER ZONES

DANGER_ZONE_LEFT_0 = 0
DANGER_ZONE_RIGHT_0 = BATTLE_SCREEN_WIDTH

DANGER_ZONE_LEFT_1 = BATTLE_SCREEN_WIDTH/16 + TILE_SIZE*0
DANGER_ZONE_RIGHT_1 = BATTLE_SCREEN_WIDTH - BATTLE_SCREEN_WIDTH/16 - TILE_SIZE*0

DANGER_ZONE_LEFT_2 = BATTLE_SCREEN_WIDTH/16 + TILE_SIZE*2
DANGER_ZONE_RIGHT_2 = BATTLE_SCREEN_WIDTH - BATTLE_SCREEN_WIDTH/16 - TILE_SIZE*2

DANGER_ZONE_LEFT_3 = BATTLE_SCREEN_WIDTH/16 + TILE_SIZE*4
DANGER_ZONE_RIGHT_3 = BATTLE_SCREEN_WIDTH - BATTLE_SCREEN_WIDTH/16 - TILE_SIZE*4

DANGER_ZONE_LEFT_4 = BATTLE_SCREEN_WIDTH/16 + TILE_SIZE*6
DANGER_ZONE_RIGHT_4 = BATTLE_SCREEN_WIDTH - BATTLE_SCREEN_WIDTH/16 - TILE_SIZE*6

DANGER_SHOOT_LEFT = BATTLE_SCREEN_WIDTH/16 + TILE_SIZE*7
DANGER_SHOOT_RIGHT = BATTLE_SCREEN_WIDTH - BATTLE_SCREEN_WIDTH/16 - TILE_SIZE*7

FPS = 60
TARGET_FPS = 60

MUTE = True



MENU = 0
GAME = 1
PAUSE = 2
GAME_OVER = 3

# who plays
PLAYER = 0
AGENT = 1

