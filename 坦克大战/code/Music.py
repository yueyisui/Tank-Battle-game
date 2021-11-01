import pygame


# 音乐
class Music:
    def __init__(self):
        # 初始化播放器
        pygame.mixer.init()
        # 加载音效
        self.start_music = pygame.mixer.Sound('../img/start.wav')
        self.fire_music = pygame.mixer.Sound('../img/fire.wav')
        self.hit_music = pygame.mixer.Sound('../img/hit.wav')

    # # 播放音乐
    # def play(self):
    #     pygame.mixer.music.play()
