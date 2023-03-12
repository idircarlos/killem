import pygame, time
pygame.init()
from util.settings import *
from util.util import import_player_assets, import_enemy_assets, import_bullet_assets
from manager import EntityManager
import sys
from debug import *
from player import *
from mixer import GLOBAL_MIXER

PLAYER_DEAD = 0
ENEMY_DEAD  = 1

class Game():
    def __init__(self,agent=None):
        self.clock = pygame.time.Clock()
        self.screen = pygame.Surface((BATTLE_SCREEN_WIDTH,BATTLE_SCREEN_HEIGHT))
        self.window = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SCALED)
        pygame.display.set_caption('Killem')
        self.entity_manager = None
        self.prev_time = time.time()
        self.font = pygame.font.SysFont("Arial" , 18 , bold = True)
        player_assets = import_player_assets()
        enemy_assets  = import_enemy_assets()
        bullet_assets = import_bullet_assets()
        self.assets = {"player":player_assets,"enemy":enemy_assets,"bullet":bullet_assets}
        self.agent = agent
        self.gamepad = self.scan_gamepad()
        self.reset()
        
        
    def reset(self):
        if self.entity_manager is not None:
            self.entity_manager.free()
        self.entity_manager = EntityManager(self.screen,self.clock,self.assets)
        self.frame = 0
        self.score = 0
        self.prev_time = time.time()
        GLOBAL_MIXER.clear_queue()
        GLOBAL_MIXER.start_loop_bg_music()
        
    def spawn_enemy(self):
        self.entity_manager.try_spawn()
        
    def play_step(self,action):
        #print(self.gamepad.get_button(0))
        self.frame += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.button == 0:
                    action[1] = 1
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    action[2] = 1
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    action[3] = 1
                elif event.key == pygame.K_f:
                    action[4] = 1
                elif event.key == pygame.K_m:
                    GLOBAL_MIXER.mute()
                elif event.key == pygame.K_o:
                    pygame.display.toggle_fullscreen()
                    pass
                elif event.key == pygame.K_s:
                    if self.agent != None:
                        self.agent.save_checkpoint(False, "./model/manual", "./model/best2")
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == pygame.CONTROLLER_BUTTON_A:
                    action[1] = 1
            if event.type == pygame.JOYHATMOTION:
                if event.value == (1,0):
                    action[2] = 1
                if event.value == (-1,0):
                    action[3] = 1
                

                
                    
        shoot_ready = self.entity_manager.player.skill_ready(SHOOT)
        
        # 2. action
        self.entity_manager.player_action(action)
        
        # 3. check if game over
        reward = 0
        game_over = False
        collision, danger_zone = self.entity_manager.check_collisions() 
        if collision == PLAYER_DEAD:
            game_over = True
            reward = -100
            return reward, game_over, self.score

        # 4. create a new enemy
        if self.frame % 1 == 0:
            self.spawn_enemy()
        
        # 5. check if the player has killed an enemy
        if collision == ENEMY_DEAD:
            self.score += 1
            if danger_zone == DANGER_ZONE_LEFT_0 or danger_zone == DANGER_ZONE_RIGHT_0:
                reward = 10
            elif danger_zone == DANGER_ZONE_LEFT_1 or danger_zone == DANGER_ZONE_RIGHT_1:
                reward = 11
            elif danger_zone == DANGER_ZONE_LEFT_2 or danger_zone == DANGER_ZONE_RIGHT_2:
                reward = 12
            elif danger_zone == DANGER_ZONE_LEFT_3 or danger_zone == DANGER_ZONE_RIGHT_3:
                reward = 14
            elif danger_zone == DANGER_ZONE_LEFT_4 or danger_zone == DANGER_ZONE_RIGHT_4:
                reward = 20
                
        # 6. check if the player shots without enemy
        selected = max(action)
        action_index = action.index(selected)
        if action_index == SHOOT:
            if not shoot_ready:
                reward = -1
            else:
                left,right = self.entity_manager.get_enemies_positions()
                if (self.entity_manager.player.orientation == LEFT and left == False and right == True) or (self.entity_manager.player.orientation == RIGHT and right == False and left == True):
                    reward = -20
                else:
                    reward += 10
        # 8. update ui and clock
        self._update_ui()
        self.clock.tick(FPS)
        
        # 9. return game over and score
        return reward, game_over, self.score
    
    def _update_ui(self):
        self.window.fill((40,40,40))
        self.screen.fill((30,30,30))
        degub_tiles(self.screen)
        debug_fps(self.window,self.clock,self.font)
        
        self.show_score()
        
        #pygame.draw.rect(screen,(255,0,0),player.rect,1)
        #pygame.draw.rect(screen,(0,255,0),player.hitbox,1)
        # limit framerate
        self.clock.tick(FPS)
        #compute delta time
        self.now_time = time.time()
        dt = self.now_time - self.prev_time
        self.prev_time = self.now_time
        self.entity_manager.update(dt)
        self.window.blit(self.screen,((SCREEN_WIDTH - BATTLE_SCREEN_WIDTH)/2,(SCREEN_HEIGHT - BATTLE_SCREEN_HEIGHT)/2))
        pygame.display.flip()
        GLOBAL_MIXER.play_next_bg_music_if_needed()
        
    def show_score(self):
        score = str(self.score)
        score_f = self.font.render(score, 1, pygame.Color("WHITE"))
        self.window.blit(score_f,(0,0))
        
    def toggle_mute(self):
        pass
    
    def scan_gamepad(self):
        for i in range(pygame.joystick.get_count()):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            print("Gamepad detected! -->", joystick.get_name())
            return joystick
    

        
        

    