import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    '''表示单个外星人的类'''
    def __init__(self,ai_settings,screen):
        '''初始化外星人并设置其起始位置'''
        super(Alien,self).__init__()
        self.screen=screen
        self.ai_settings=ai_settings
        
        #加载外星人图像，并设置其rect属性
        self.images=[]
        self.images.append(pygame.image.load('.\\images\\frame_apngframe1.png'))
        self.images.append(pygame.image.load('.\\images\\frame_apngframe2.png'))
        self.images.append(pygame.image.load('.\\images\\frame_apngframe3.png'))
        self.images.append(pygame.image.load('.\\images\\frame_apngframe4.png'))
        self.images.append(pygame.image.load('.\\images\\frame_apngframe5.png'))
        self.images.append(pygame.image.load('.\\images\\frame_apngframe6.png'))
        self.index=0
        self.image=self.images[self.index]
        self.rect=self.image.get_rect()
        #每个外星人最初都在屏幕左上角附近
        self.rect.x=self.rect.width
        self.rect.y=self.rect.height
        
        #存储外星人的准确位置
        self.x=float(self.rect.x)
    """    
    def blitme(self):
        '''在指定位置绘制外星人'''
        for frame in self.frames:
            self.screen.blit(self.images[frame],self.rect)
    """
    def play_animation(self):
        self.index+=1
        if self.index>=len(self.images):
            self.index=0
        self.image=self.images[self.index]
    def update(self):
        '''向右移动外星人'''
        self.x += (self.ai_settings.alien_speed_factor*self.ai_settings.fleet_direction)
        self.rect.x=self.x
    
    def check_edges(self):
        '''如果外星人位于屏幕边缘，就返回True'''
        screen_rect=self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True