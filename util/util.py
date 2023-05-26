import pygame
from os import walk
from util.settings import *

class TerminalColor:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def import_folder(path,dimension,orientation=RIGHT):
    surface_list = []
    for _,__,image_files in walk(path):
        image_files.sort()
        for image in image_files:
            full_path = path + '/' + image
            image_surf = load_sprite(full_path,dimension,orientation)
            surface_list.append(image_surf)
    return surface_list
    
def load_sprite(path,dimension,orientation):
    return pygame.transform.flip(pygame.transform.scale(pygame.image.load(path).convert_alpha(),dimension),False if orientation is RIGHT else True, False)


def import_player_assets():
    animations = {'idle':[],'attack':[],'block':[],'dead':[]}
    for animation in animations.keys():
        full_path = SPRITES_PATH + "player/" + animation
        animations[animation] = import_folder(full_path,(PLAYER_SPRITE_SIZE_X*2,PLAYER_SPRITE_SIZE_Y*2))
    return animations
            
def import_enemy_skeleton_assets():
    animations = {'walk':[],'dead':[]}
    for animation in animations.keys():
        full_path = SPRITES_PATH + "enemy/skeleton/" + animation
        animations[animation] = import_folder(full_path,(ENEMY_SPRTE_SIZE_X*ENEMY_SPRITE_MULTIPLIER,ENEMY_SPRTE_SIZE_Y*ENEMY_SPRITE_MULTIPLIER))
    return animations

def import_enemy_undead_assets():
    animations = {'walk':[],'dead':[]}
    for animation in animations.keys():
        full_path = SPRITES_PATH + "enemy/undead/" + animation
        animations[animation] = import_folder(full_path,(ENEMY_SPRTE_SIZE_X*ENEMY_SPRITE_MULTIPLIER*3,ENEMY_SPRTE_SIZE_Y*ENEMY_SPRITE_MULTIPLIER*2))
    return animations
            
def import_bullet_assets():
    animations = {'icicle_start':[],'icicle':[]}
    for animation in animations.keys():
        full_path = SPRITES_PATH + "bullet/" + animation
        animations[animation] = import_folder(full_path, (BULLET_SPRITE_SIZE_X,BULLET_SPRITE_SIZE_Y))
    return animations

def import_shield_assets():
    animations = {'block':[]}
    for animation in animations.keys():
        full_path = SPRITES_PATH + animation
        animations[animation] = import_folder(full_path, (PLAYER_SPRITE_SIZE_X*2,PLAYER_SPRITE_SIZE_Y*2))
    return animations

def import_shoot_assets():
    animations = {'fire_01':[],'fire_02':[]}
    for animation in animations.keys():
        full_path = SPRITES_PATH + "shoot/" + animation
        animations[animation] = import_folder(full_path, (BULLET_SPRITE_SIZE_X,BULLET_SPRITE_SIZE_Y))
    return animations

def import_background_assets():
    animations = {'bg_01':[], 'bg_02': [], 'bg_03': []}
    for animation in animations.keys():
        full_path = BACKGROUND_PATH + animation
        animations[animation] = import_folder(full_path, (1218,768))
    return animations