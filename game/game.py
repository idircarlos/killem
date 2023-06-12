import pygame, time
from game.button import Button
pygame.init()
from util.settings import *
from util.util import import_player_assets, import_enemy_skeleton_assets, import_bullet_assets
from entities.manager import EntityManager
import sys
from util.debug import *
from entities.characters.player import *
from mixer.mixer import GLOBAL_MIXER, OPTION_SELECTED, PAUSE_PRESSED, UNPAUSE_PRESSED, BACK_PRESSED, GAME_OVER_SOUND
import random as rand

PLAYER_DEAD = 0
ENEMY_DEAD  = 1
SHOOT_BLOCKED = 2


class Game():
    def __init__(self,agent=None):
        self.clock = pygame.time.Clock()
        pygame.display.set_icon(pygame.image.load('./resources/icons/skull.png'))
        pygame.display.set_caption('Killem')
        
        self.window = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.SCALED)
        pygame.display.toggle_fullscreen()
        self.screen = pygame.Surface((BATTLE_SCREEN_WIDTH,BATTLE_SCREEN_HEIGHT),pygame.SRCALPHA,32) # SRCALPHA, 32 transparent background surface
        self.screen = self.screen.convert_alpha()
        
        
        self.entity_manager = None
        self.prev_time = time.time()
        self.font = pygame.font.SysFont("Arial" , 18 , bold = True)
        self.score_font = pygame.font.Font("./resources/fonts/ARCADE_N.ttf" , 100 , bold = True)
        self.score_font_1 = pygame.font.Font("./resources/fonts/ARCADE_N.ttf" , 100 , bold = True)
        player_assets = import_player_assets()
        enemy_skeleton_assets  = import_enemy_skeleton_assets()
        enemy_nightborne_assets  = import_enemy_undead_assets()
        bullet_assets = import_bullet_assets()
        shield_assets = import_shield_assets()
        shoot_assets  = import_shoot_assets()
        self.assets = {"player":player_assets,"enemy_skeleton":enemy_skeleton_assets,"enemy_undead":enemy_nightborne_assets,"bullet":bullet_assets,"block":shield_assets,"shoot":shoot_assets}
        self.agent = agent
        self.gamepad = None
        self.scan_gamepad()
        pygame.mouse.set_cursor(pygame.cursors.broken_x)
        self.background_assets = import_background_assets()
        self.bg = rand.choice(list(self.background_assets))
        self.current_bg_sprite = 0
        self.n_sprites_bg = len(self.background_assets[self.bg])
        self.background = self.background_assets[self.bg][self.current_bg_sprite]
        self.zone = MENU
        self.paused = [False]
        self.who_plays = PLAYER
        self.using_mouse = True
        self.show_fps = False
        self.reset()
        
        
    def reset(self):
        if self.entity_manager is not None:
            self.entity_manager.free()
        self.entity_manager = EntityManager(self.paused,self.screen,self.clock,self.assets)
        self.frame = 0
        self.score = 0
        self.paused = [False]
        GLOBAL_MIXER.set_unpaused_vol()
        self.prev_time = time.time()
        GLOBAL_MIXER.clear_queue()
        GLOBAL_MIXER.start_loop_bg_music()
    
    def start(self):
        while True:
            if self.zone == MENU:
                GLOBAL_MIXER.clear_queue()
                GLOBAL_MIXER.start_loop_menu_music()
                self.menu()
                GLOBAL_MIXER.clear_queue()
                GLOBAL_MIXER.start_loop_bg_music()
            if self.zone == GAME:
                self.play()
            if self.zone == PAUSE:
                self.pause()
            if self.zone == GAME_OVER:
                self.game_over()
        
    def spawn_enemy(self):
        self.entity_manager.try_spawn()
        
    def play(self):
        while self.zone == GAME:
            if self.who_plays == PLAYER:
                self.play_step([0,0,0,0,0])
            elif self.who_plays == AGENT:
                if LEARNING:
                    self.train_agent()
                else:
                    self.play_agent()
        
    def play_step(self,action):
        self.frame += 1
        self.scan_gamepad()
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    action[SHOOT_RIGHT] = 1
                elif event.key == pygame.K_LEFT:
                    action[SHOOT_LEFT] = 1
                elif event.key == pygame.K_d:
                    action[BLOCK_RIGHT] = 1
                elif event.key == pygame.K_a:
                    action[BLOCK_LEFT] = 1
                elif event.key == pygame.K_m:
                    GLOBAL_MIXER.mute()
                elif event.key == pygame.K_F4:
                    pygame.display.toggle_fullscreen()
                elif event.key == pygame.K_F3:
                    self.show_fps = not self.show_fps
                elif event.key == pygame.K_s:
                    if self.agent != None:
                        self.agent.save_checkpoint(False, "./model/manual", "./model/best2")
                elif event.key == pygame.K_ESCAPE:
                    self.paused[0] = not self.paused[0]
                    if not self.paused[0]:
                        GLOBAL_MIXER.play(UNPAUSE_PRESSED)
                        GLOBAL_MIXER.set_unpaused_vol()
                        self.zone = GAME
                    else:
                        GLOBAL_MIXER.play(PAUSE_PRESSED)
                        GLOBAL_MIXER.set_paused_vol()
                        self.zone = PAUSE              
            
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == pygame.CONTROLLER_AXIS_TRIGGERLEFT:
                    action[4] = 1
                if event.button == pygame.CONTROLLER_AXIS_TRIGGERRIGHT:
                    action[3] = 1
                if pygame.joystick.Joystick(0).get_button(7):
                    self.paused[0] = not self.paused[0]
                    if not self.paused[0]:
                        GLOBAL_MIXER.play(UNPAUSE_PRESSED)
                        GLOBAL_MIXER.set_unpaused_vol()
                        self.zone = GAME
                    else:
                        GLOBAL_MIXER.play(PAUSE_PRESSED)
                        GLOBAL_MIXER.set_paused_vol()
                        self.zone = PAUSE      
                if event.button == pygame.CONTROLLER_BUTTON_X:
                     action[1] = 1
                if event.button == pygame.CONTROLLER_BUTTON_B:
                     action[2] = 1       
                    
            if event.type == pygame.JOYHATMOTION:
                if event.value == (1,0):
                    action[2] = 1
                if event.value == (-1,0):
                    action[1] = 1

        
        shoot_ready = self.entity_manager.player.skill_ready(SHOOT)
        block_ready = self.entity_manager.player.skill_ready(BLOCK)
        
        shoot_left, shoot_right = self.entity_manager.get_bullets_positions()
        n_shoots_left, n_shoots_right = self.entity_manager.get_n_shoots()
        n_enemies_left, n_enemies_right = self.entity_manager.get_n_enemies()
        enemy_shoot_left, enemy_shoot_right = self.entity_manager.get_shoots_danger()
        
        
        # 2. action
        self.entity_manager.player_action(action)
        
        selected = max(action)
        action_index = action.index(selected)
        
        # 3. check if game over
        reward = 0
        game_over = False
        collision, danger_zone = self.entity_manager.check_collisions() 
        if collision == PLAYER_DEAD:
            game_over = True
            reward = -500
            if self.who_plays == PLAYER or (self.who_plays == AGENT and not LEARNING):
                self.zone = GAME_OVER
            return reward, game_over, self.score

        # 4. create a new enemy
        if self.frame % 1 == 0:
            pass
            #self.spawn_enemy()
            
        shield = None
        for shield_i in self.entity_manager.shield_group:
            shield = shield_i
        
        # 5a. check if the player will kill an enemy
        danger_zone_left, danger_zone_right = self.entity_manager.check_positions()
        if action_index == SHOOT_LEFT and shoot_ready:
            if danger_zone_left == DANGER_ZONE_LEFT_0:
                reward = 10
            elif danger_zone_left == DANGER_ZONE_LEFT_1:
                reward = 10
            elif danger_zone_left == DANGER_ZONE_LEFT_2:
                reward = 10
            elif danger_zone_left == DANGER_ZONE_LEFT_3:
                reward = 50
            elif danger_zone_left == DANGER_ZONE_LEFT_4:
                reward = 50
            else:
                reward = 5
        elif action_index == SHOOT_RIGHT and shoot_ready:
            if danger_zone_right == DANGER_ZONE_RIGHT_0:
                reward = 10
            elif danger_zone_right == DANGER_ZONE_RIGHT_1:
                reward = 10
            elif danger_zone_right == DANGER_ZONE_RIGHT_2:
                reward = 10
            elif danger_zone_right == DANGER_ZONE_RIGHT_3:
                reward = 50
            elif danger_zone_right == DANGER_ZONE_RIGHT_4:
                reward = 50
            else:
                reward = 5
        if action_index == SHOOT_LEFT and shoot_ready and danger_zone_left > danger_zone_right:
            if n_shoots_left < n_enemies_left:
                reward = 30
            if n_shoots_left > n_enemies_left:
                reward = -30
        elif action_index == SHOOT_LEFT and shoot_ready and danger_zone_left < danger_zone_right:
            if n_shoots_right >= n_enemies_right:
                reward = 30
            else:
                reward = -60
        if action_index == SHOOT_RIGHT and shoot_ready and  danger_zone_right > danger_zone_left:
            if n_shoots_right < n_enemies_right:
                reward = 30
            if n_shoots_right > n_enemies_right:
                reward = -30
        elif action_index == SHOOT_RIGHT and shoot_ready and danger_zone_right < danger_zone_left:
            if n_shoots_left >= n_enemies_left:
                reward = 30
            else:
                reward = -60
        if collision == ENEMY_DEAD:
            self.score += 1
        
            
        if action_index == BLOCK_LEFT and block_ready and enemy_shoot_left[DANGER_SHOOT_LEFT]:
            reward = 40
        if action_index == BLOCK_RIGHT and block_ready and enemy_shoot_right[DANGER_SHOOT_RIGHT]:
            reward = 40
            
        # 5b. check if the player has blocked a shoot
        if collision == SHOOT_BLOCKED:
            self.score += 1
            shield.blocked = True
                
        # 6a. check if the player shots without enemy
        if action_index == SHOOT_LEFT or action_index == SHOOT_RIGHT:
            if not shoot_ready:
                reward += -10
        
        # 6b. check if the player blocks without enemy shoots
        if action_index == BLOCK_LEFT or action_index == BLOCK_RIGHT:
            if not block_ready and shield != None and shield.blocked == False:
                reward = -10
            else:
                if shield != None and collision != SHOOT_BLOCKED:
                    shoot_danger_left,shoot_danger_right = self.entity_manager.get_shoots_danger()
                    if shoot_danger_left[DANGER_SHOOT_LEFT] == False and shoot_danger_right[DANGER_SHOOT_RIGHT] == False and shield.blocked == False:
                        reward = -50
                    elif shoot_danger_right[DANGER_SHOOT_RIGHT] == True and shield.orientation == LEFT and shield.blocked == False:
                        reward = -50
                    elif shoot_danger_left[DANGER_SHOOT_LEFT] == True and shield.orientation == RIGHT and shield.blocked == False:
                        reward = -50
                    else:
                        reward += 0
                        
        # 8. update ui and clock
        self._update_ui()
        self.clock.tick(FPS)
        
        # 9. return game over and score
        return reward, game_over, self.score
    
    def _update_ui(self):
        self.window.fill((40,40,40))
        self.window.blit(self.background,(0,0))
        self.screen.fill((255,255,255,0))   #clear the transparent background surface
        debug_fps(self.window,self.clock,self.font,self.show_fps)
        self.show_score()
        # compute delta time
        self.now_time = time.time()
        self.dt = self.now_time - self.prev_time
        self.prev_time = self.now_time
        self.entity_manager.update(self.dt)
        self.window.blit(self.screen,(0,80))
        if not self.paused[0]:
            self.background = self.background_assets[self.bg][int(self.current_bg_sprite)%self.n_sprites_bg]
            self.current_bg_sprite += 15*self.dt
        pygame.display.flip()
        GLOBAL_MIXER.play_next_bg_music_if_needed()
        
    def show_score(self):
        score = str(self.score)
        score_f = self.score_font.render(score, 1, pygame.Color("WHITE"))
        text_rect = score_f.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/4))
        
        score_f_1 = self.score_font_1.render(score, 1, pygame.Color("#536878"))
        score_f_rect_1 = score_f_1.get_rect(center=(SCREEN_WIDTH/2 + 5, SCREEN_HEIGHT/4 + 5))
        
        self.window.blit(score_f_1,score_f_rect_1)
        self.window.blit(score_f,text_rect)
        
        
    def toggle_mute(self):
        pass
    
    def scan_gamepad(self):
        if self.gamepad != None:
            return
        for i in range(pygame.joystick.get_count()):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            print("Gamepad detected! -->", joystick.get_name())
            self.gamepad = joystick
    
    def menu(self):
        mouse_pos = pygame.mouse.get_pos()
        last_mouse_pos = mouse_pos
        options = ["HUMAN","AGENT","X"]
        index_option_selected = 0 # "HUMAN"
        title = self.score_font.render("Killem", 1, pygame.Color("WHITE"))
        title_rect = title.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/4))
        
        title_1 = self.score_font.render("Killem", 1, pygame.Color("#536878"))
        title_rect_1 = title.get_rect(center=(SCREEN_WIDTH/2 + 5, SCREEN_HEIGHT/4 + 5))
        
        menu_button_font = pygame.font.Font("./resources/fonts/ARCADE_N.ttf" , 30 , bold = True)
        or_font = pygame.font.Font("./resources/fonts/ARCADE_N.ttf" , 15 , bold = True)
        or_label = or_font.render("or", 1, pygame.Color("WHITE"))
        or_label_rect = or_label.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT - SCREEN_HEIGHT/11 - 2))
        close_font = pygame.font.Font("./resources/fonts/ARCADE_N.ttf" , 50 , bold = True)
        PLAY_BUTTON = Button(image=None, pos=(SCREEN_WIDTH/4 + SCREEN_WIDTH/8, SCREEN_HEIGHT - SCREEN_HEIGHT/10), 
                            text_input="HUMAN", font=menu_button_font, base_color="White", hovering_color="#90b9d4")
        IA_BUTTON = Button(image=None, pos=(SCREEN_WIDTH/4 + SCREEN_WIDTH/8 + SCREEN_WIDTH/4, SCREEN_HEIGHT - SCREEN_HEIGHT/10), 
                            text_input="AGENT", font=menu_button_font, base_color="White", hovering_color="#fcf39f")
        QUIT_BUTTON = Button(image=None, pos=(1160, 730), 
                            text_input="X", font=close_font, base_color="White", hovering_color="#bd2f2f")
        
        select_first_option = True
        play_sound = False
        while self.zone == MENU:
            self.scan_gamepad()
            self.window.fill((40,40,40))
            self.window.blit(self.background,(0,0))
            self.screen.fill((255,255,255,0))   #clear the transparent background surface
            
            self.now_time = time.time()
            self.dt = self.now_time - self.prev_time
            self.prev_time = self.now_time
            
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos != last_mouse_pos:
                self.using_mouse = True
                index_option_selected = 0
                pygame.mouse.set_visible(True)
                select_first_option = False
            last_mouse_pos = mouse_pos
            
            self.window.blit(title_1, title_rect_1)
            self.window.blit(title, title_rect)
            self.window.blit(or_label, or_label_rect)
            

            for button in [PLAY_BUTTON, IA_BUTTON, QUIT_BUTTON]:
                button.change_color(mouse_pos,options[index_option_selected],self.using_mouse and not select_first_option,play_sound=play_sound)
                button.update(self.window)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.check_for_input(mouse_pos):
                        GLOBAL_MIXER.play(OPTION_SELECTED)
                        self.zone = GAME
                        self.who_plays = PLAYER
                    elif IA_BUTTON.check_for_input(mouse_pos):
                        GLOBAL_MIXER.play(OPTION_SELECTED)
                        self.zone = GAME
                        self.who_plays = AGENT
                    elif QUIT_BUTTON.check_for_input(mouse_pos):
                        pygame.quit()
                        sys.exit()
                        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        GLOBAL_MIXER.mute()
                    elif event.key == pygame.K_F4:
                        pygame.display.toggle_fullscreen()
                    elif event.key == pygame.K_F3:
                        self.show_fps = not self.show_fps    
                
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        if self.using_mouse == True:
                            self.using_mouse = False
                        pygame.mouse.set_visible(False)
                        if options[index_option_selected] == "HUMAN":
                            GLOBAL_MIXER.play(OPTION_SELECTED)
                            self.zone = GAME
                            self.who_plays = PLAYER
                        elif options[index_option_selected] == "AGENT":
                            GLOBAL_MIXER.play(OPTION_SELECTED)
                            self.zone = GAME
                            self.who_plays = AGENT
                        elif options[index_option_selected] == "X":
                            pygame.quit()
                            sys.exit()
                    elif event.key == pygame.K_RIGHT:
                        if self.using_mouse == True:
                            self.using_mouse = False
                        else:
                            index_option_selected = (index_option_selected + 1) % len(options)
                    elif event.key == pygame.K_LEFT:
                        if self.using_mouse == True:
                            self.using_mouse = False
                        else:
                            index_option_selected = (index_option_selected - 1) % len(options) 
                        
                if event.type == pygame.JOYBUTTONDOWN:
                    if self.using_mouse == True:
                        self.using_mouse = False
                        pygame.mouse.set_visible(False)
                    elif event.button == pygame.CONTROLLER_BUTTON_A:
                        if options[index_option_selected] == "HUMAN":
                            GLOBAL_MIXER.play(OPTION_SELECTED)
                            self.zone = GAME
                            self.who_plays = PLAYER
                        if options[index_option_selected] == "AGENT":
                            GLOBAL_MIXER.play(OPTION_SELECTED)
                            self.zone = GAME
                            self.who_plays = AGENT
                        if options[index_option_selected] == "X":
                            pygame.quit()
                            sys.exit()
                        
                if event.type == pygame.JOYHATMOTION:
                    pygame.mouse.set_visible(False)
                    if event.value == (1,0):
                        if self.using_mouse == True:
                            self.using_mouse = False
                        else:
                            index_option_selected = (index_option_selected + 1) % len(options)
                    if event.value == (-1,0):
                        if self.using_mouse == True:
                            self.using_mouse = False
                        else:
                            index_option_selected = (index_option_selected - 1) % len(options) 
            play_sound = True
            self.entity_manager.update(self.dt,MENU)
            self.window.blit(self.screen,(0,80))
            debug_fps(self.window,self.clock,self.font,self.show_fps)
            self.background = self.background_assets[self.bg][int(self.current_bg_sprite)%self.n_sprites_bg]
            self.current_bg_sprite += 15*self.dt
            GLOBAL_MIXER.play_next_menu_music_if_needed()
            pygame.display.flip()
            self.clock.tick(FPS)
    
    def pause(self):
        mouse_pos = pygame.mouse.get_pos()
        last_mouse_pos = mouse_pos
        options = ["RESUME","RESTART","FINISH"]
        index_option_selected = 0 # "RESUME"
        title = self.score_font.render("Killem", 1, pygame.Color("WHITE"))
        title_rect = title.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/4))
        menu_button_font = pygame.font.Font("./resources/fonts/ARCADE_N.ttf" , 30 , bold = True)
        RESUME_BUTTON = Button(image=None, pos=(SCREEN_WIDTH/4, SCREEN_HEIGHT - SCREEN_HEIGHT/10), 
                            text_input="RESUME", font=menu_button_font, base_color="White", hovering_color="#90b9d4")
        RESTART_BUTTON = Button(image=None, pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT - SCREEN_HEIGHT/10), 
                            text_input="RESTART", font=menu_button_font, base_color="White", hovering_color="#bb9dd4")
        FINISH_BUTTON = Button(image=None, pos=(SCREEN_WIDTH/2 + SCREEN_WIDTH/4, SCREEN_HEIGHT - SCREEN_HEIGHT/10), 
                            text_input="FINISH", font=menu_button_font, base_color="White", hovering_color="#e66a6a")
        play_sound = False 
        select_first_option = True
        while self.zone == PAUSE:
            self.scan_gamepad()
            self.window.fill((40,40,40))
            self.window.blit(self.background,(0,0))
            self.screen.fill((255,255,255,0))   #clear the transparent background surface
            
            self.now_time = time.time()
            self.dt = self.now_time - self.prev_time
            self.prev_time = self.now_time
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos != last_mouse_pos:
                self.using_mouse = True
                index_option_selected = 0
                pygame.mouse.set_visible(True)
                select_first_option = False
            last_mouse_pos = mouse_pos

            self.show_score()

            for button in [RESUME_BUTTON, RESTART_BUTTON, FINISH_BUTTON]:
                button.change_color(mouse_pos,options[index_option_selected],self.using_mouse and not select_first_option,play_sound=play_sound)
                button.update(self.window)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if RESUME_BUTTON.check_for_input(mouse_pos):
                        self.paused[0] = not self.paused[0]
                        GLOBAL_MIXER.set_unpaused_vol()
                        GLOBAL_MIXER.play(UNPAUSE_PRESSED)
                        self.zone = GAME
                    elif RESTART_BUTTON.check_for_input(mouse_pos):
                        self.reset()
                        self.zone = GAME
                        GLOBAL_MIXER.play(OPTION_SELECTED)
                    elif FINISH_BUTTON.check_for_input(mouse_pos):
                        self.reset()
                        self.zone = MENU
                        GLOBAL_MIXER.play(BACK_PRESSED)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        GLOBAL_MIXER.mute()
                    elif event.key == pygame.K_F4:
                        pygame.display.toggle_fullscreen()
                    elif event.key == pygame.K_F3:
                        self.show_fps = not self.show_fps
                    elif event.key == pygame.K_ESCAPE:
                        self.paused[0] = not self.paused[0]
                        if not self.paused[0]:
                            GLOBAL_MIXER.set_unpaused_vol()
                            GLOBAL_MIXER.play(UNPAUSE_PRESSED)
                            self.zone = GAME
                        else:
                            GLOBAL_MIXER.set_paused_vol()
                            GLOBAL_MIXER.play(PAUSE_PRESSED)
                            self.zone = PAUSE
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        pygame.mouse.set_visible(False)
                        if self.using_mouse == True:
                            self.using_mouse = False
                        if options[index_option_selected] == "RESUME":
                            self.paused[0] = not self.paused[0]
                            GLOBAL_MIXER.play(UNPAUSE_PRESSED)
                            GLOBAL_MIXER.set_unpaused_vol()
                            self.zone = GAME
                        elif options[index_option_selected] == "RESTART":
                            GLOBAL_MIXER.play(OPTION_SELECTED)
                            self.reset()
                            self.zone = GAME
                        elif options[index_option_selected] == "FINISH":
                            GLOBAL_MIXER.play(BACK_PRESSED)
                            self.reset()
                            self.zone = MENU
                    elif event.key == pygame.K_RIGHT:
                        if self.using_mouse == True:
                            self.using_mouse = False
                        else:
                            index_option_selected = (index_option_selected + 1) % len(options)
                    elif event.key == pygame.K_LEFT:
                        if self.using_mouse == True:
                            self.using_mouse = False
                        else:
                            index_option_selected = (index_option_selected - 1) % len(options)
                
                if event.type == pygame.JOYBUTTONDOWN:
                    pygame.mouse.set_visible(False)
                    if self.using_mouse == True:
                        self.using_mouse = False
                    if pygame.joystick.Joystick(0).get_button(7):
                        self.paused[0] = not self.paused[0]
                        if not self.paused[0]:
                            GLOBAL_MIXER.set_unpaused_vol()
                            GLOBAL_MIXER.play(UNPAUSE_PRESSED)
                            self.zone = GAME
                        else:
                            GLOBAL_MIXER.set_paused_vol()
                            GLOBAL_MIXER.play(PAUSE_PRESSED)
                            self.zone = PAUSE
                                    
                    if event.button == pygame.CONTROLLER_BUTTON_A:
                        if options[index_option_selected] == "RESUME":
                            self.paused[0] = not self.paused[0]
                            GLOBAL_MIXER.play(UNPAUSE_PRESSED)
                            GLOBAL_MIXER.set_unpaused_vol()
                            self.zone = GAME
                        if options[index_option_selected] == "RESTART":
                            GLOBAL_MIXER.play(OPTION_SELECTED)
                            self.reset()
                            self.zone = GAME
                        if options[index_option_selected] == "FINISH":
                            GLOBAL_MIXER.play(BACK_PRESSED)
                            self.reset()
                            self.zone = MENU
                    if event.button == pygame.CONTROLLER_BUTTON_B:
                        self.paused[0] = not self.paused[0]
                        GLOBAL_MIXER.play(UNPAUSE_PRESSED)
                        GLOBAL_MIXER.set_unpaused_vol()
                        self.zone = GAME
                if event.type == pygame.JOYHATMOTION:
                    pygame.mouse.set_visible(False)
                    if event.value == (1,0):
                        if self.using_mouse == True:
                            self.using_mouse = False
                            index_option_selected = 0
                        else:
                            index_option_selected = (index_option_selected + 1) % len(options)
                    if event.value == (-1,0):
                        if self.using_mouse == True:
                            self.using_mouse = False
                            index_option_selected = 0
                        else:
                            index_option_selected = (index_option_selected - 1) % len(options)   
                        
            play_sound = True
            
            self.entity_manager.update(self.dt,PAUSE)
            self.window.blit(self.screen,(0,80))
            debug_fps(self.window,self.clock,self.font,self.show_fps)
            GLOBAL_MIXER.play_next_bg_music_if_needed()
            pygame.display.flip()
            self.clock.tick(FPS)
            
    def game_over(self):
        mouse_pos = pygame.mouse.get_pos()
        last_mouse_pos = mouse_pos
        GLOBAL_MIXER.play(GAME_OVER_SOUND)
        GLOBAL_MIXER.set_paused_vol(7)
        options = ["RESTART","MENU"]
        index_option_selected = 0 # "RESTART"
        title = self.score_font.render("Killem", 1, pygame.Color("WHITE"))
        title_rect = title.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/4))
        menu_button_font = pygame.font.Font("./resources/fonts/ARCADE_N.ttf" , 30 , bold = True)
        game_over_font = pygame.font.Font("./resources/fonts/ARCADE_N.ttf" , 80 , bold = True)
        game_over_font_label = game_over_font.render("GAME OVER", 1, pygame.Color("WHITE"))
        game_over_font_rect = game_over_font_label.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        game_over_font_1 = pygame.font.Font("./resources/fonts/ARCADE_N.ttf" , 80 , bold = True)
        game_over_font_label_1 = game_over_font_1.render("GAME OVER", 1, pygame.Color("#536878"))
        game_over_font_rect_1 = game_over_font_label_1.get_rect(center=(SCREEN_WIDTH/2 + 5, SCREEN_HEIGHT/2 + 5))
        
        PLAY_AGAIN_BUTTON = Button(image=None, pos=(SCREEN_WIDTH/4 + SCREEN_WIDTH/8 , SCREEN_HEIGHT - SCREEN_HEIGHT/10), 
                            text_input="RESTART", font=menu_button_font, base_color="White", hovering_color="#b690d4")
        
        MENU_BUTTON = Button(image=None, pos=(SCREEN_WIDTH/2 + SCREEN_WIDTH/4 - SCREEN_WIDTH/8, SCREEN_HEIGHT - SCREEN_HEIGHT/10), 
                            text_input="MENU", font=menu_button_font, base_color="White", hovering_color="#e66a6a")
        select_first_option = True
        play_sound = False
        while self.zone == GAME_OVER:
            debug_fps(self.window,self.clock,self.font,self.show_fps)
            self.scan_gamepad()
            self.window.fill((40,40,40))
            self.window.blit(self.background,(0,0))
            self.screen.fill((255,255,255,0))   #clear the transparent background surface
            
            self.now_time = time.time()
            self.dt = self.now_time - self.prev_time
            self.prev_time = self.now_time
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos != last_mouse_pos:
                self.using_mouse = True
                index_option_selected = 0
                pygame.mouse.set_visible(True)
                select_first_option = False
            last_mouse_pos = mouse_pos

            self.show_score()
            
            
            for button in [MENU_BUTTON, PLAY_AGAIN_BUTTON]:
                button.change_color(mouse_pos,options[index_option_selected],self.using_mouse and not select_first_option,play_sound=play_sound)
                button.update(self.window)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_AGAIN_BUTTON.check_for_input(mouse_pos):
                        GLOBAL_MIXER.play(OPTION_SELECTED)
                        self.reset()
                        self.zone = GAME
                    elif MENU_BUTTON.check_for_input(mouse_pos):
                        GLOBAL_MIXER.play(BACK_PRESSED)
                        self.reset()
                        self.zone = MENU

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        GLOBAL_MIXER.mute()
                    if event.key == pygame.K_F4:
                        pygame.display.toggle_fullscreen()
                    elif event.key == pygame.K_F3:
                        self.show_fps = not self.show_fps

                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        pygame.mouse.set_visible(False)
                        if self.using_mouse == True:
                            self.using_mouse = False
                        elif options[index_option_selected] == "RESTART":
                            GLOBAL_MIXER.play(OPTION_SELECTED)
                            self.reset()
                            self.zone = GAME
                        elif options[index_option_selected] == "MENU":
                            GLOBAL_MIXER.play(BACK_PRESSED)
                            self.reset()
                            self.zone = MENU
                    elif event.key == pygame.K_RIGHT:
                        if self.using_mouse == True:
                            self.using_mouse = False
                        else:
                            index_option_selected = (index_option_selected + 1) % len(options)
                    elif event.key == pygame.K_LEFT:
                        if self.using_mouse == True:
                            self.using_mouse = False
                        else:
                            index_option_selected = (index_option_selected - 1) % len(options)
                    
                if event.type == pygame.JOYBUTTONDOWN:
                    pygame.mouse.set_visible(False)
                    if self.using_mouse == True:
                        self.using_mouse = False
                    if event.button == pygame.CONTROLLER_BUTTON_A:
                            if options[index_option_selected] == "RESTART":
                                GLOBAL_MIXER.play(OPTION_SELECTED)
                                self.reset()
                                self.zone = GAME
                            if options[index_option_selected] == "MENU":
                                GLOBAL_MIXER.play(BACK_PRESSED)
                                self.reset()
                                self.zone = MENU
                if event.type == pygame.JOYHATMOTION:
                    pygame.mouse.set_visible(False)
                    if event.value == (1,0):
                        if self.using_mouse == True:
                            self.using_mouse = False
                            index_option_selected = 0
                        else:
                            index_option_selected = (index_option_selected + 1) % len(options)
                    if event.value == (-1,0):
                        if self.using_mouse == True:
                            self.using_mouse = False
                            index_option_selected = 0
                        else:
                            index_option_selected = (index_option_selected - 1) % len(options)     
            
            play_sound = True
            self.entity_manager.update(self.dt,GAME_OVER)
            self.window.blit(self.screen,(0,80))
            self.window.blit(game_over_font_label_1, game_over_font_rect_1)
            self.window.blit(game_over_font_label, game_over_font_rect)
            debug_fps(self.window,self.clock,self.font,self.show_fps)
            GLOBAL_MIXER.play_next_bg_music_if_needed()
            pygame.display.flip()
            self.clock.tick(FPS)
    
    def play_agent(self):
        self.agent = Agent()
        self.agent.n_games, self.agent.record, self.agent.total_score = self.agent.load_checkpoint("./model/manual/checkpoint.pth",self.agent.model,self.agent.trainer.optimizer)
        while self.zone == GAME:
            self.scan_gamepad()
            # get old state
            state_old = self.agent.get_state(self)

            # get move  
            final_move = self.agent.get_action(state_old)

            # perform move and get new state
            reward, done, score = self.play_step(final_move) 
    
    def train_agent(self):
        plot_scores = []
        plot_mean_scores = []
        total_score = 0
        self.agent = Agent()
        self.agent.n_games, self.agent.record, self.agent.total_score = self.agent.load_checkpoint("./model/manual/checkpoint.pth",self.agent.model,self.agent.trainer.optimizer)
        
        while True:
            # get old state
            state_old = self.agent.get_state(self)

            # get move  
            final_move = self.agent.get_action(state_old)

            # perform move and get new state
            reward, done, score = self.play_step(final_move)
            state_new = self.agent.get_state(self)
            
            if reward != 0 and reward != -1 and reward != -10:
                pass
                print(reward)
            

            if LEARNING:
                # train short memory
                self.agent.train_short_memory(state_old, final_move, reward, state_new, done)

                # remember
                self.agent.remember(state_old, final_move, reward, state_new, done)

            if done:
                # train long memory, plot result
                self.reset()
                if LEARNING:
                    self.agent.n_games += 1
                    self.agent.train_long_memory()

                    if score > self.agent.record:
                        self.agent.record = score
                        self.agent.save_checkpoint(True, "./model", "./model/best")

                    print('Game', self.agent.n_games, 'Score', score, 'Record:', self.agent.record)
                    print()

                    plot_scores.append(score)
                    total_score += score
                    mean_score = total_score / self.agent.n_games
                    plot_mean_scores.append(mean_score)
from agent.agent import Agent