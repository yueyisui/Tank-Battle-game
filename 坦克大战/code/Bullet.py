import pygame
# 子弹
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, tank):
        pygame.sprite.Sprite.__init__(self)
        # 获取子弹的图像
        self.image = pygame.image.load('../img/enemymissile.gif')
        # 获取子弹的大小
        self.rect = self.image.get_rect()
        # 设置子弹显示的初始化位置
        if tank.direction == 'U':
            self.rect.top = tank.rect.top - self.rect.height
            self.rect.left = tank.rect.left + tank.rect.width / 2.0 - self.rect.width / 2.0
        elif tank.direction == 'D':
            self.rect.top = tank.rect.top + tank.rect.height
            self.rect.left = tank.rect.left + tank.rect.width / 2.0 - self.rect.width / 2.0
        elif tank.direction == 'L':
            self.rect.top = tank.rect.top + tank.rect.height / 2.0 - self.rect.height / 2.0
            self.rect.left = tank.rect.left - self.rect.width
        elif tank.direction == 'R':
            self.rect.top = tank.rect.top + tank.rect.height / 2.0 - self.rect.height / 2.0
            self.rect.left = tank.rect.left + tank.rect.width
        # 初始化子弹的方向
        self.direction = tank.direction
        # 初始化子弹移动的速度
        self.speed = 5
        # 子弹的状态
        self.flag = 1

    # 显示
    def display_bullet(self, surface):
        # 将子弹显示在surface
        if self.flag:
            pygame.Surface.blit(surface, self.image, self.rect)

    # 移
    def move(self):
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                self.flag = 0  # 状态消失
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < 360:
                self.rect.top += self.speed
            else:
                self.flag = 0
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                self.flag = 0
        elif self.direction == 'R':
            if self.rect.left + self.rect.width < 640:
                self.rect.left += self.speed
            else:
                self.flag = 0
