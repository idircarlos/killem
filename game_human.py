import pygame, time

pygame.init()

from sys import exit
from util.util import *
from util.settings import *
from player import Player
from enemy import Enemy
from respawn import Spawn
from debug import degub_tiles, debug_fps
from rand import Rand
from manager import EntityManager


clock = pygame.time.Clock()
pygame.display.set_caption('Example')
screen = pygame.display.set_mode((BATTLE_SCREEN_WIDTH,BATTLE_SCREEN_HEIGHT))

entity_manager = EntityManager(screen,clock)
prev_time = time.time()

font = pygame.font.SysFont("Arial" , 18 , bold = True)

while True:
    # limit framerate
    clock.tick(FPS)
    #compute delta time
    now_time = time.time()
    dt = now_time - prev_time
    prev_time = now_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                entity_manager.player_attack()
            elif event.key == pygame.K_b:
                entity_manager.player_block()
            elif event.key == pygame.K_RIGHT:
                entity_manager.player_flip(RIGHT)
            elif event.key == pygame.K_LEFT:
                entity_manager.player_flip(LEFT)
            elif event.key == pygame.K_f:
                entity_manager.rotating = True
                entity_manager.flip_axis()
    screen.fill((30,30,30))
    degub_tiles(screen)
    debug_fps(screen,clock,font)
    #pygame.draw.rect(screen,(255,0,0),player.rect,1)
    #pygame.draw.rect(screen,(0,255,0),player.hitbox,1)
    entity_manager.update(dt)    
    pygame.display.flip()

    