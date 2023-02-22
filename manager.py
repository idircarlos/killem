import pygame
from player import *
from enemy  import *
from bullet import *
from respawn import *
from rand import Rand
import math

PLAYER_DEAD = 0
ENEMY_DEAD  = 1

class EntityManager:
    def __init__(self,screen,clock):
        self.screen = screen
        self.rand = Rand()
        self.player = Player()
        self.player_group = pygame.sprite.Group()
        self.player_group.add(self.player)
        self.bullet_group = pygame.sprite.Group()
        self.left_respawn  = Spawn(LEFT,clock,self.rand)
        self.right_respawn  = Spawn(RIGHT,clock,self.rand)
        self.top_respawn  = Spawn(TOP,clock,self.rand)
        self.bottom_respawn  = Spawn(BOTTOM,clock,self.rand)
        self.enemy_group = pygame.sprite.Group()
        self.clock = clock
        
    def flip_axis(self):
        for enemy in self.enemy_group:
            enemy.radius = int(sqrt(pow(abs(CENTER_X - (enemy.rect.x + enemy.rect.width/2)),2) + pow(abs(CENTER_Y - (enemy.rect.y + enemy.rect.height/2)),2)))
            enemy.rotating = True
        
    def player_action(self,action_list):
        selected = max(action_list)
        action = action_list.index(selected)
        if action == FLIP_RIGHT:
            self.player_flip(RIGHT)
        if action == FLIP_LEFT:
            self.player_flip(LEFT)
        elif action == ATTACK:
            self.player_attack()
        elif action == BLOCK:
            self.player_block()
        
    def player_attack(self):
        can_attack = self.player.attack()
        if can_attack:
            self.bullet_group.add(Bullet(self.player.hitbox,self.player.orientation))
            
    def player_block(self):
        if not self.player.is_animating:
            self.player.block()
        
    def player_flip(self,dir):
        self.player.flip(dir)
            
    def try_spawn(self):
        if self.left_respawn.try_spawn():
            self.enemy_group.add(Enemy((self.left_respawn.x,self.left_respawn.y),(0,0,0,0),LEFT))
        if self.right_respawn.try_spawn():
            self.enemy_group.add(Enemy((self.right_respawn.x,self.right_respawn.y),(0,0,0,0),RIGHT))
        if self.top_respawn.try_spawn():
            self.enemy_group.add(Enemy((self.top_respawn.x,self.top_respawn.y),(0,0,0,0),TOP))
        if self.bottom_respawn.try_spawn():
            self.enemy_group.add(Enemy((self.bottom_respawn.x,self.bottom_respawn.y),(0,0,0,0),BOTTOM))
            
    def check_collisions(self):
        for bullet in self.bullet_group:
            for enemy in self.enemy_group:
                if enemy.orientation == LEFT:
                    if pygame.Rect.colliderect(bullet.rect,enemy.rect) and bullet.rect.x + bullet.rect.width >= enemy.rect.x + int(enemy.rect.width/2 + 25) and (enemy.spawn != TOP and enemy.spawn != BOTTOM) and enemy.alive:
                        print("arriba",bullet.rect.x, enemy.rect.x)
                        enemy.alive = False
                        #enemy.kill()
                        #self.enemy_group.remove(enemy)
                        enemy.animate("dead")
                        bullet.kill()
                        return ENEMY_DEAD
                else:
                    if pygame.Rect.colliderect(bullet.rect,enemy.rect) and bullet.rect.x <= enemy.rect.x + int(enemy.rect.width/2 - 25) and (enemy.spawn != TOP and enemy.spawn != BOTTOM) and enemy.alive:
                        print("abajo",bullet.rect.x, enemy.rect.x)
                        enemy.alive = False
                        #enemy.kill()
                        enemy.animate("dead")
                        bullet.kill()
                        return ENEMY_DEAD
        for enemy in self.enemy_group:
            if enemy.rect.x == self.player.rect.x and enemy.rect.y == self.player.rect.y:
                print("GAME OVER")
                self.player.kill()
                return PLAYER_DEAD
            
    def update(self,dt):
        self.check_collisions()
        self.player_group.draw(self.screen)
        self.player_group.update(dt)
        self.enemy_group.draw(self.screen)
        self.enemy_group.update(dt)
        self.bullet_group.draw(self.screen)
        self.bullet_group.update(dt)
        self.try_spawn()
        #pygame.draw.rect(self.screen,(0,255,0),self.player.hitbox,1)
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