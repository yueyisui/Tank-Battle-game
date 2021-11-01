import pygame


# 爆炸
class Explode:
    def __init__(self, tank):
        # 加载爆炸的图片
        self.images = [pygame.image.load('../img/blast0.gif'),
                       pygame.image.load('../img/blast1.gif'),
                       pygame.image.load('../img/blast2.gif'),
                       pygame.image.load('../img/blast3.gif'),
                       pygame.image.load('../img/blast4.gif')]
        self.image = self.images[0]
        self.image.get_width()
        # 获得位置和大小
        self.rect = tank.rect
        # 初始化
        self.step = 0
        # 状态
        self.flag = True

    # 展示爆炸效果
    def display_explode(self, surface):
        if self.step < len(self.images):
            self.image = self.images[self.step]
            pygame.Surface.blit(surface, self.image, self.rect)
            self.step += 1
        else:
            self.flag = False
            self.step = 0

