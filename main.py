import pygame
from sys import exit
from util.util import *
from util.settings import *
from player import Player
from enemy import Enemy
from respawn import Spawn
from debug import degub_tiles
from rand import Rand
from manager import EntityManager

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Example')
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

entity_manager = EntityManager(screen,clock)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                entity_manager.player_attack()
            elif event.key == pygame.K_b:
                entity_manager.player_block()
            if event.key == pygame.K_RIGHT:
                entity_manager.player_flip(RIGHT)
            elif event.key == pygame.K_LEFT:
                entity_manager.player_flip(LEFT)
    screen.fill((30,30,30))
    degub_tiles(screen)
    #pygame.draw.rect(screen,(255,0,0),player.rect,1)
    #pygame.draw.rect(screen,(0,255,0),player.hitbox,1)
    entity_manager.update()    
    pygame.display.flip()
    clock.tick(144)
    