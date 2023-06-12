import pygame
from util.settings import *

def degub_tiles(screen):
    surface = screen.convert_alpha()
    surface.fill([0,0,0,0])
    for x in range(0,BATTLE_SCREEN_WIDTH,TILE_SIZE):
        pygame.draw.line(surface,(255,255,255,32), (x, 0), (x, BATTLE_SCREEN_HEIGHT))
    for y in range(0,BATTLE_SCREEN_HEIGHT,TILE_SIZE):
        pygame.draw.line(surface,(255,255,255,32), (0, y), (BATTLE_SCREEN_WIDTH, y))
    screen.blit(surface,(0,0))

def debug_fps(screen,clock,font,show_fps):
    if not show_fps:
        return
    fps = str(int(clock.get_fps()))
    fps_f = font.render(fps , 1, pygame.Color("WHITE"))
    screen.blit(fps_f,(SCREEN_WIDTH-30,0))
    
def debug_time(screen,time,font):
    record_text = font.render("Time: " +str(round(time,5)), False, (255,255,255))
    screen.blit(record_text, (0,100))