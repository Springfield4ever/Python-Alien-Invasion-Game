import pygame

class Sound():
    '''添加游戏中的各种音效'''
    def __init__(self):
        self.main_title= '.\sounds\main_title.mp3'
        self.laser= pygame.mixer.Sound('.\sounds\laser.wav')
        self.score= pygame.mixer.Sound('.\\sounds\score.wav')
        self.level_up= pygame.mixer.Sound(".\\sounds\level_up.wav")
        self.fail=pygame.mixer.Sound('.\\sounds\\fail.wav')
    def play_main_title(self):
        pygame.mixer.music.load(self.main_title)
        pygame.mixer.music.play(-1)

    def pause_main_title(self):
        pygame.mixer.music.pause()
    
    def unpause_main_title(self):
        pygame.mixer.music.unpause()
    
    def play_laser(self):
        self.laser.play()
    
    def play_score(self):
        self.score.play()
    
    def play_level_up(self):
        self.level_up.play()
    
    def play_fail(self):
        self.fail.play()