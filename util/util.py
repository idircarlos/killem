import pygame
from os import walk
from util.settings import *
from math import atan2, pi, sin, cos, radians

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

from enemy import Enemy



def _translate_point(point, center):
    print("PUNTO_INICIAL:",point, "CENTER:", center)
    x, y = point
    x = int(x)
    y = int(y)
    cx, cy = center
    angle = radians(1)
    new_x = int(cx + (x - cx) * cos(angle) - (y - cy) * sin(angle))
    new_y = int(cy + (x - cx) * sin(angle) + (y - cy) * cos(angle))
    print("PUNTO_FINAL:",(new_x,new_y), "CENTER:", center)
    return new_x, new_y