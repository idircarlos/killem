import pygame
from util.settings import *

def import_folder(path,dimension,orientation=RIGHT):
        from os import walk
        surface_list = []

        for _,__,image_files in walk(path):
            for image in image_files:
                full_path = path + '/' + image
                image_surf = load_sprite(full_path,dimension,orientation)
                surface_list.append(image_surf)

        return surface_list
    
def load_sprite(path,dimension,orientation):
    return pygame.transform.flip(pygame.transform.scale(pygame.image.load(path).convert_alpha(),dimension),False if orientation is RIGHT else True, False)