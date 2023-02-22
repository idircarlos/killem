import pygame
from util.settings import *

def degub_tiles(screen):
    surface = screen.convert_alpha()
    surface.fill([0,0,0,0])
    for x in range(0,SCREEN_WIDTH,TILE_SIZE):
        pygame.draw.line(surface,(255,255,255,32), (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0,SCREEN_HEIGHT,TILE_SIZE):
        pygame.draw.line(surface,(255,255,255,32), (0, y), (SCREEN_WIDTH, y))
    #pygame.draw.rect(screen,(255,0,0),self.rect,1)
    #pygame.draw.rect(screen,(0,255,0),self.hitbox,1)
    screen.blit(surface,(0,0))

def debug_fps(screen,clock,font):
    fps = str(int(clock.get_fps()))
    fps_t = font.render(fps , 1, pygame.Color("WHITE"))
    screen.blit(fps_t,(0,0))