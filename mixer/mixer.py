import pygame.mixer
pygame.mixer.init()
from util.settings import *
from mixer.sound import Sound
import random

SHOOT_SOUND = 0
ENEMY_DEATH_SOUND = 1
OPTION_CHANGE = 2
OPTION_SELECTED = 3
PAUSE_PRESSED = 4
UNPAUSE_PRESSED = 5
BACK_PRESSED = 6
SHOOT_BLOCKED_SOUND = 7
GAME_OVER_SOUND = 8

class Mixer:
    
    def __init__(self):
        self.menu_music = []
        self.bg_music = []
        self.sounds = {SHOOT_SOUND:[],ENEMY_DEATH_SOUND:[],OPTION_CHANGE:[],OPTION_SELECTED:[],PAUSE_PRESSED:[],UNPAUSE_PRESSED:[],BACK_PRESSED:[],SHOOT_BLOCKED_SOUND:[],GAME_OVER_SOUND:[]}
        self.current_music = 0
        self.vol = 0.10
        self.is_mute = False
    
    def _add_menu_music(self,menu_music_files):
        for menu_music in menu_music_files: 
            self.menu_music.append(menu_music)
        
    def _add_bg_music(self,bg_music_files):
        for bg_music in bg_music_files: 
            self.bg_music.append(bg_music)
    
    def _add_sound(self,key,sound_file,vol):
        sound = Sound(sound_file,vol)
        self.sounds[key].append(sound)
        
    def start_loop_menu_music(self):
        pygame.mixer.music.load(self.menu_music[0])
        pygame.mixer.music.set_volume(self.vol if not self.is_mute else 0)
        pygame.mixer.music.play()
        
    def start_loop_bg_music(self):
        pygame.mixer.music.load(self.bg_music[0])
        pygame.mixer.music.set_volume(self.vol if not self.is_mute else 0)
        pygame.mixer.music.play()
        
    def play_next_menu_music_if_needed(self):
        if not pygame.mixer.music.get_busy():
            # Actualizar el índice de canción actual y volver al principio de la lista si llegamos al final
            self.current_music = (self.current_music + 1) % len(self.menu_music)
            # Cargar y reproducir la siguiente canción en la lista
            pygame.mixer.music.load(self.menu_music[self.current_music])
            pygame.mixer.music.play()
        
    def play_next_bg_music_if_needed(self):
        if not pygame.mixer.music.get_busy():
            # Actualizar el índice de canción actual y volver al principio de la lista si llegamos al final
            self.current_music = (self.current_music + 1) % len(self.bg_music)
            # Cargar y reproducir la siguiente canción en la lista
            pygame.mixer.music.load(self.bg_music[self.current_music])
            pygame.mixer.music.play()
            
    def set_paused_vol(self,div_vol=5):
        if not self.is_mute:
            pygame.mixer.music.set_volume(self.vol/div_vol)
        
    def set_unpaused_vol(self):
        if not self.is_mute:
            pygame.mixer.music.set_volume(self.vol)

    def clear_queue(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        
    def mute(self):
        if not self.is_mute:
            pygame.mixer.music.set_volume(0)
        else:
            pygame.mixer.music.set_volume(self.vol)
        for list_sound in self.sounds.values():
                for sound in list_sound:
                    sound.mute()
        self.is_mute = not self.is_mute
        
    def play(self,key):
        sound = random.choice(self.sounds[key])
        sound.play()
        
        
def _create_mixer():
        mixer = Mixer()
        mixer._add_menu_music([BG_MUSIC_AUDIO_0])
        mixer._add_bg_music([BG_MUSIC_AUDIO_1,BG_MUSIC_AUDIO_2])
        
        mixer._add_sound(SHOOT_SOUND,SHOOT_PATH_1,0.05)
        mixer._add_sound(SHOOT_SOUND,SHOOT_PATH_2,0.05)
        mixer._add_sound(SHOOT_SOUND,SHOOT_PATH_3,0.05)
        mixer._add_sound(SHOOT_SOUND,SHOOT_PATH_4,0.05)
        
        mixer._add_sound(ENEMY_DEATH_SOUND,DEATH_PATH_1,0.15)
        mixer._add_sound(ENEMY_DEATH_SOUND,DEATH_PATH_2,0.15)
        mixer._add_sound(ENEMY_DEATH_SOUND,DEATH_PATH_3,0.15)
        mixer._add_sound(ENEMY_DEATH_SOUND,DEATH_PATH_4,0.15)
        
        mixer._add_sound(SHOOT_BLOCKED_SOUND,SHOOT_BLOCKED_PATH_1,0.10)
        mixer._add_sound(SHOOT_BLOCKED_SOUND,SHOOT_BLOCKED_PATH_2,0.10)
        mixer._add_sound(SHOOT_BLOCKED_SOUND,SHOOT_BLOCKED_PATH_3,0.10)
        
        mixer._add_sound(OPTION_CHANGE,OPTION_CHANGE_PATH_1,0.3)
        
        mixer._add_sound(OPTION_SELECTED,OPTION_SELECTED_PATH_1,0.4)
        
        mixer._add_sound(BACK_PRESSED,BACK_PATH_1,0.4)
        
        mixer._add_sound(PAUSE_PRESSED,PAUSE_PATH_1,0.4)
        
        mixer._add_sound(UNPAUSE_PRESSED,UNPAUSE_PATH_1,0.4)
        
        mixer._add_sound(GAME_OVER_SOUND,GAME_OVER_PATH_1,0.2)
        return mixer

GLOBAL_MIXER = _create_mixer()