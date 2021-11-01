import pygame


# 墙壁
class Wall:
    def __init__(self, left, top):
        self.image = pygame.image.load('../img/steels.gif')
        # 设置墙壁范围
        self.rect = self.image.get_rect()
        # 设置left top
        self.rect.left = left
        self.rect.top = top
        # 状态
        self.flag = 1
        # 生命值
        self.lives = 3

    # 显示
    def display_wall(self, surface):
        pygame.Surface.blit(surface, self.image, self.rect)
