import pygame
from player import *
from enemy  import *
from bullet import *
from respawn import *
from rand import Rand
from debug import *
from mixer import GLOBAL_MIXER, SHOOT_SOUND, ENEMY_DEATH_SOUND

PLAYER_DEAD = 0
ENEMY_DEAD  = 1

class EntityManager:
    def __init__(self,screen,clock,assets):
        self.screen = screen
        self.rand = Rand()
        self.player = Player(assets["player"])
        self.player_group = pygame.sprite.Group()
        self.player_group.add(self.player)
        self.bullet_group = pygame.sprite.Group()
        self.left_respawn  = Spawn(LEFT,clock,self.rand)
        self.right_respawn  = Spawn(RIGHT,clock,self.rand)
        self.top_respawn  = Spawn(TOP,clock,self.rand)
        self.bottom_respawn  = Spawn(BOTTOM,clock,self.rand)
        self.enemy_group = pygame.sprite.Group()
        self.clock = clock
        self.font = pygame.font.SysFont("Arial" , 18 , bold = True)
        self.assets = assets
        
    def flip_axis(self):
        for enemy in self.enemy_group:
            enemy.rotate()
        
    def player_action(self,action_list):
        selected = max(action_list)
        action = action_list.index(selected)
        if action == SHOOT:
            if self.player.skill_ready(SHOOT):
                self.player.use_skill(SHOOT)
                self.player_attack()
        elif action == FLIP_LEFT:
            self.player_flip(LEFT)
        elif action == FLIP_RIGHT:
            self.player_flip(RIGHT)
        elif action == ROTATE:
            if self.player.skill_ready(ROTATE):
                self.player.use_skill(ROTATE)
                self.flip_axis()
        elif action == BLOCK:
            self.player_block()
        
    def player_attack(self):
        can_attack = self.player.attack()
        if can_attack:
            self.bullet_group.add(Bullet(self.player.hitbox,self.player.orientation,self.assets["bullet"]))
            GLOBAL_MIXER.play(SHOOT_SOUND)
            
    def player_block(self):
        if not self.player.is_animating:
            self.player.block()
        
    def player_flip(self,dir):
        self.player.flip(dir)
            
    def try_spawn(self):
        if self.left_respawn.try_spawn():
            self.enemy_group.add(Enemy((self.left_respawn.x,self.left_respawn.y),(0,0,0,0),self.assets["enemy"],LEFT))
        if self.right_respawn.try_spawn():
            self.enemy_group.add(Enemy((self.right_respawn.x,self.right_respawn.y),(0,0,0,0),self.assets["enemy"],RIGHT))
        if self.top_respawn.try_spawn():
            self.enemy_group.add(Enemy((self.top_respawn.x,self.top_respawn.y),(0,0,0,0),self.assets["enemy"],TOP))
        if self.bottom_respawn.try_spawn():
            self.enemy_group.add(Enemy((self.bottom_respawn.x,self.bottom_respawn.y),(0,0,0,0),self.assets["enemy"],BOTTOM))
    
    def get_enemies_positions(self):
        left  = False
        right = False
        for enemy in self.enemy_group:
            if enemy.spawn == RIGHT and enemy.rect.x <= SCREEN_WIDTH - 1 and enemy.alive:
                right = True
            elif enemy.spawn == LEFT and enemy.rect.x + enemy.rect.width >= 1 and enemy.alive:
                left = True
        return left, right
    
    def get_bullets_positions(self):
        left  = False
        right = False
        for bullet in self.bullet_group:
            if bullet.orientation == RIGHT:
                right = True
            else:
                left = True
        return left, right
            
    def check_collisions(self):
        for bullet in self.bullet_group:
            for enemy in self.enemy_group:
                if enemy.spawn == RIGHT:
                    if pygame.Rect.colliderect(bullet.rect,enemy.rect) and bullet.rect.x + bullet.rect.width >= enemy.rect.x + int(enemy.rect.width/2 + 25) and (enemy.spawn != TOP and enemy.spawn != BOTTOM) and enemy.alive:
                        danger_zone = 0
                        if self.enemy_in_danger_zone(enemy,DANGER_ZONE_RIGHT_4):
                            danger_zone = DANGER_ZONE_RIGHT_4
                        elif self.enemy_in_danger_zone(enemy,DANGER_ZONE_RIGHT_3):
                            danger_zone = DANGER_ZONE_RIGHT_3
                        elif self.enemy_in_danger_zone(enemy,DANGER_ZONE_RIGHT_2):
                            danger_zone = DANGER_ZONE_RIGHT_2
                        elif self.enemy_in_danger_zone(enemy,DANGER_ZONE_RIGHT_1):
                            danger_zone = DANGER_ZONE_RIGHT_1
                        elif self.enemy_in_danger_zone(enemy,DANGER_ZONE_RIGHT_0):
                            danger_zone = DANGER_ZONE_RIGHT_0
                        enemy.alive = False
                        GLOBAL_MIXER.play(ENEMY_DEATH_SOUND)
                        #enemy.kill()
                        #self.enemy_group.remove(enemy)
                        enemy.animate("dead")
                        bullet.kill()
                        #print(str(round(bullet.timer,5)))
                        return ENEMY_DEAD, danger_zone
                else:
                    if pygame.Rect.colliderect(bullet.rect,enemy.rect) and bullet.rect.x <= enemy.rect.x + int(enemy.rect.width/2 - 25) and (enemy.spawn != TOP and enemy.spawn != BOTTOM) and enemy.alive:
                        danger_zone = 0
                        if self.enemy_in_danger_zone(enemy,DANGER_ZONE_LEFT_4):
                            danger_zone = DANGER_ZONE_LEFT_4
                        elif self.enemy_in_danger_zone(enemy,DANGER_ZONE_LEFT_3):
                            danger_zone = DANGER_ZONE_LEFT_3
                        elif self.enemy_in_danger_zone(enemy,DANGER_ZONE_LEFT_2):
                            danger_zone = DANGER_ZONE_LEFT_2
                        elif self.enemy_in_danger_zone(enemy,DANGER_ZONE_LEFT_1):
                            danger_zone = DANGER_ZONE_LEFT_1
                        elif self.enemy_in_danger_zone(enemy,DANGER_ZONE_LEFT_0):
                            danger_zone = DANGER_ZONE_LEFT_0
                        enemy.alive = False
                        GLOBAL_MIXER.play(ENEMY_DEATH_SOUND)
                        #enemy.kill()
                        enemy.animate("dead")
                        bullet.kill()
                        #print(str(round(bullet.timer,5)))
                        return ENEMY_DEAD, danger_zone
        for enemy in self.enemy_group:
            if pygame.Rect.colliderect(self.player.hitbox,enemy.rect):
                print("GAME OVER")
                self.player.kill()
                return PLAYER_DEAD, -1
        return None, -1
            
    def enemy_in_danger_zone(self,enemy,danger_zone):
        spawn = enemy.spawn
        if spawn == RIGHT:
            if enemy.rect.x <= danger_zone:
                return True
        elif spawn == LEFT:
            if enemy.rect.x + enemy.rect.width >= danger_zone:
                return True
        return False
            
    def get_enemies_danger(self):
        danger_left  = {DANGER_ZONE_LEFT_0:False,DANGER_ZONE_LEFT_1:False,DANGER_ZONE_LEFT_2:False,DANGER_ZONE_LEFT_3:False,DANGER_ZONE_LEFT_4:False}
        danger_right = {DANGER_ZONE_RIGHT_0:False,DANGER_ZONE_RIGHT_1:False,DANGER_ZONE_RIGHT_2:False,DANGER_ZONE_RIGHT_3:False,DANGER_ZONE_RIGHT_4:False}
        for enemy in self.enemy_group:
            if enemy.spawn == RIGHT and enemy.alive:
                if self.enemy_in_danger_zone(enemy,DANGER_ZONE_RIGHT_4):
                    danger_right[DANGER_ZONE_RIGHT_4] = True
                elif self.enemy_in_danger_zone(enemy,DANGER_ZONE_RIGHT_3):
                    danger_right[DANGER_ZONE_RIGHT_3] = True
                elif self.enemy_in_danger_zone(enemy,DANGER_ZONE_RIGHT_2):
                    danger_right[DANGER_ZONE_RIGHT_2] = True
                elif self.enemy_in_danger_zone(enemy,DANGER_ZONE_RIGHT_1):
                    danger_right[DANGER_ZONE_RIGHT_1] = True
                elif self.enemy_in_danger_zone(enemy,DANGER_ZONE_RIGHT_0):
                    danger_right[DANGER_ZONE_RIGHT_0] = True
            elif enemy.spawn == LEFT and enemy.alive:
                if self.enemy_in_danger_zone(enemy,DANGER_ZONE_LEFT_4):
                    danger_left[DANGER_ZONE_LEFT_4] = True
                elif self.enemy_in_danger_zone(enemy,DANGER_ZONE_LEFT_3):
                    danger_left[DANGER_ZONE_LEFT_3] = True
                elif self.enemy_in_danger_zone(enemy,DANGER_ZONE_LEFT_2):
                    danger_left[DANGER_ZONE_LEFT_2] = True
                elif self.enemy_in_danger_zone(enemy,DANGER_ZONE_LEFT_1):
                    danger_left[DANGER_ZONE_LEFT_1] = True
                elif self.enemy_in_danger_zone(enemy,DANGER_ZONE_LEFT_0):
                    danger_left[DANGER_ZONE_LEFT_0] = True
        return danger_left, danger_right
            
    def update(self,dt):
        if TRAINING:
            dt = 1
        self.check_collisions()
        self.player_group.draw(self.screen)
        self.player_group.update(dt)
        self.enemy_group.draw(self.screen)
        self.enemy_group.update(dt)
        self.bullet_group.draw(self.screen)
        self.bullet_group.update(dt)
        self.try_spawn()
        #pygame.draw.rect(self.screen,(0,255,0),self.player.rect,1)
        pygame.draw.line(self.screen,(255,255,255),(DANGER_ZONE_LEFT_0,0),(DANGER_ZONE_LEFT_0,SCREEN_HEIGHT),1)
        pygame.draw.line(self.screen,(255,255,255),(DANGER_ZONE_RIGHT_0-1,0),(DANGER_ZONE_RIGHT_0-1,SCREEN_HEIGHT),1)
        pygame.draw.line(self.screen,(0,255,255),(DANGER_ZONE_RIGHT_1,0),(DANGER_ZONE_RIGHT_1,SCREEN_HEIGHT),1)
        pygame.draw.line(self.screen,(0,255,255),(DANGER_ZONE_LEFT_1,0),(DANGER_ZONE_LEFT_1,SCREEN_HEIGHT),1)
        pygame.draw.line(self.screen,(0,255,255),(DANGER_ZONE_RIGHT_1,0),(DANGER_ZONE_RIGHT_1,SCREEN_HEIGHT),1)
        pygame.draw.line(self.screen,(0,255,0),(DANGER_ZONE_LEFT_2,0),(DANGER_ZONE_LEFT_2,SCREEN_HEIGHT),1)
        pygame.draw.line(self.screen,(0,255,0),(DANGER_ZONE_RIGHT_2,0),(DANGER_ZONE_RIGHT_2,SCREEN_HEIGHT),1)
        pygame.draw.line(self.screen,(255,255,0),(DANGER_ZONE_LEFT_3,0),(DANGER_ZONE_LEFT_3,SCREEN_HEIGHT),1)
        pygame.draw.line(self.screen,(255,255,0),(DANGER_ZONE_RIGHT_3,0),(DANGER_ZONE_RIGHT_3,SCREEN_HEIGHT),1)
        pygame.draw.line(self.screen,(255,0,0),(DANGER_ZONE_LEFT_4,0),(DANGER_ZONE_LEFT_4,SCREEN_HEIGHT),1)
        pygame.draw.line(self.screen,(255,0,0),(DANGER_ZONE_RIGHT_4,0),(DANGER_ZONE_RIGHT_4,SCREEN_HEIGHT),1)
        for enemy in self.enemy_group:
            #pygame.draw.rect(self.screen,(255,0,0),enemy.rect,1)
            #pygame.draw.circle(self.screen,(0,0,255),(enemy.rect.x,enemy.rect.y),10,20)
            #pygame.draw.line(self.screen,(0,255,255),(CENTER_X,CENTER_Y),(SCREEN_WIDTH,SCREEN_HEIGHT))
            #pygame.draw.line(self.screen,(0,255,255),(CENTER_X,CENTER_Y),(SCREEN_WIDTH/2,SCREEN_HEIGHT))
            #pygame.draw.line(self.screen,(0,255,255),(CENTER_X,CENTER_Y),(SCREEN_WIDTH,SCREEN_HEIGHT/2))
            pass
        #pygame.draw.circle(self.screen,(0,0,255),(CENTER_X,CENTER_Y),10,20)
        
    def free(self):
        for sprite in self.player_group:
            sprite.kill()
        for sprite in self.enemy_group:
            sprite.kill()
        for sprite in self.bullet_group:
            sprite.kill()
            print(str(round(sprite.timer,5)))