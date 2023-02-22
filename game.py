import pygame, time
from util.settings import *
from manager import EntityManager
import sys
from debug import *

PLAYER_DEAD = 0
ENEMY_DEAD  = 1

class Game():
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        pygame.display.set_caption('Killem')
        self.entity_manager = None
        self.prev_time = time.time()
        self.font = pygame.font.SysFont("Arial" , 18 , bold = True)
        self.reset()
        
    def reset(self):
        if self.entity_manager is not None:
            self.entity_manager.free()
        self.entity_manager = EntityManager(self.screen,self.clock)
        self.frame = 0
        self.score = 0
        self.prev_time = time.time()
        
    def spawn_enemy(self):
        self.entity_manager.try_spawn()
        
    def play_step(self,action):
        self.frame += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # 2. action
        self.entity_manager.player_action(action)
        
        # 3. check if game over
        reward = 0
        game_over = False
        collision = self.entity_manager.check_collisions() 
        if collision == PLAYER_DEAD:
            game_over = True
            reward = -10
            print(reward,game_over,self.score)
            return reward, game_over, self.score

        # 4. create a new enemy
        if self.frame % 30 == 0:
            self.spawn_enemy()
        
        # 5. check if the player has killed an enemy
        if collision == ENEMY_DEAD:
            self.score += 1
            reward = 10
            
        # 6. update ui and clock
        self._update_ui()
        self.clock.tick(FPS)
        
        # 7. return game over and score
        return reward, game_over, self.score
    
    def _update_ui(self):
        self.screen.fill((30,30,30))
        degub_tiles(self.screen)
        debug_fps(self.screen,self.clock,self.font)
        #pygame.draw.rect(screen,(255,0,0),player.rect,1)
        #pygame.draw.rect(screen,(0,255,0),player.hitbox,1)
        # limit framerate
        self.clock.tick(FPS)
        #compute delta time
        self.now_time = time.time()
        dt = self.now_time - self.prev_time
        self.prev_time = self.now_time
        self.entity_manager.update(dt)    
        pygame.display.flip()


    