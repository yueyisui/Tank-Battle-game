import pygame
from pygame.sprite import Sprite

from Bullet import Bullet
import random


# 坦克
class Tank(Sprite):
    def __init__(self, left, top):
        pygame.sprite.Sprite.__init__(self)
        # 加载所有的图像，上下左右四张
        self.images = {
            'U': pygame.image.load('../img/p1tankU.gif'),
            'D': pygame.image.load('../img/p1tankD.gif'),
            'L': pygame.image.load('../img/p1tankL.gif'),
            'R': pygame.image.load('../img/p1tankR.gif')
        }
        # 初始化坦克的方向
        self.direction = 'U'
        self.image = self.images[self.direction]  # 相当于一个surface
        # 根据图片获取大小
        self.rect = self.image.get_rect()
        # 设置坦克默认位置
        self.rect.left = left
        self.rect.top = top
        # 设置初始速度
        self.speed = 3
        # 是否停止
        self.stop = True
        # 状态
        self.flag = 1
        # 保存原来的位置
        self.old_left = self.rect.left
        self.old_top = self.rect.top

    # 显示
    def display_tank(self, surface):
        if self.flag:
            # 获取对象
            self.image = self.images[self.direction]
            # 展示
            pygame.Surface.blit(surface, self.image, self.rect)
            # SCREEN_WIDTH = surface.get_width()
            # SCREEN_HEIGHT = surface.get_height()

    # 移动
    def move(self):
        # 保存原来的位置
        self.old_left = self.rect.left
        self.old_top = self.rect.top
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
        elif self.direction == 'D':
            if self.rect.top < 360 - self.image.get_size()[0]:
                self.rect.top += self.speed
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
        elif self.direction == 'R':
            if self.rect.left < 640 - self.image.get_size()[1]:
                self.rect.left += self.speed

    # 射击
    def shot(self, tank):
        print("发射子弹")
        # 子弹
        return Bullet(tank)

    # 回到之前的位置
    def stay(self):
        self.rect.top = self.old_top
        self.rect.left = self.old_left


# 敌方坦克
class EnemyTank(Tank):
    def __init__(self, left, top, speed):
        super(EnemyTank, self).__init__(left, top)
        self.images = {'U': pygame.image.load('../img/enemy1U.gif'),
                       'D': pygame.image.load('../img/enemy1D.gif'),
                       'L': pygame.image.load('../img/enemy1L.gif'),
                       'R': pygame.image.load('../img/enemy1R.gif')}
        # 随机初始化方向
        self.direction = self.random_direction()
        # 获得方向对应的图像
        self.image = self.images[self.direction]
        # 获得范围
        self.rect = self.image.get_rect()
        self.rect.top = top
        self.rect.left = left
        # 速度
        self.speed = speed
        # 移动的步数
        self.step = random.randint(5, 100)

    # 随机生成方向
    def random_direction(self):
        num = random.randint(1, 4)
        if num == 1:
            return 'U'
        elif num == 2:
            return 'D'
        elif num == 3:
            return 'L'
        elif num == 4:
            return 'R'

    # 相反方向
    def f_direction(self, old_d):
        if old_d == 'U':
            self.step = 30
            return 'D'
        elif old_d == 'D':
            self.step = 30
            return 'U'
        elif old_d == 'R':
            self.step = 30
            return 'L'
        elif old_d == 'L':
            self.step = 30
            return 'R'

    # 随机移动
    def random_move(self):
        if self.step > 0:
            self.step -= 1
            self.move()
        else:
            self.step = random.randint(5, 30)
            self.direction = self.random_direction()

    # 重写shot
    def shot(self, tank):
        num = random.randint(0, 200)
        if num < 5:
            return Bullet(tank)
