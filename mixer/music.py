import pygame.mixer
pygame.mixer.init()

class Music:
    
    def __init__(self,file_path,vol=1.0):
        pygame.mixer.music.load(file_path)
        self.vol = vol
        pygame.mixer.music.set_volume(vol)
        
    def play(self):
        pygame.mixer.music.play(-1,0)
    
    def pause(self):
        pygame.mixer.music.pause()
        
    def resume(self):
        pygame.mixer.music.unpause()
        
    def stop(self):
        pygame.mixer.music.stop()
        
    def mute(self):
        if pygame.mixer.music.get_volume() != 0:
            pygame.mixer.music.set_vol(self.vol)
        else:
            pygame.mixer.music.set_vol(0)