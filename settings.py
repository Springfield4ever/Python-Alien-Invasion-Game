import json
class Settings():
    def __init__(self):
        '''初始化游戏的静态设置'''
        with open('settings.json') as file_object:
            settings=json.load(file_object)
        self.screen_width=settings['screen_width']
        self.screen_height=settings['screen_height']
        self.speedup_scale=settings['speedup_scale']
        self.ship_limit=settings['ship_limit']
        #屏幕设置
        #self.screen_width=1200
        #self.screen_height=800
        self.bg_color=(30,30,30)
        #飞船的设置
        #self.ship_limit=3
        #子弹设置
        self.bullet_width = 5
        self.bullet_height= 25
        self.bullet_color= 255,255,255
        self.bullets_allowed=3
        #外星人的设置
        self.fleet_drop_speed=10
        #以什么样的速度加快游戏节奏
        #self.speedup_scale=1.1
        #外星人点数提高速度
        self.score_scale=1.5
        self.initialize_dynamic_settings()
    
    def initialize_dynamic_settings(self):
        '''初始化随游戏进行而变化的设置'''
        self.ship_speed_factor=1.5
        self.bullet_speed_factor=3
        self.alien_speed_factor=1
        #fleet_direction为1表示向右，为-1表示向左
        self.fleet_direction=1
        #计分
        self.alien_points=50
    
    def increase_speed(self):
        '''提高速度的设置'''
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points=int(self.alien_points*self.score_scale)