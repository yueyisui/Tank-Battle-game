'''
需求
1，坦克类
显示
移动
射击

2，子弹
显示
移动


3，墙壁
属性：是否可以通过

4，爆炸
展示

5，声音
播放音乐

6，主类
开始游戏
结束游戏

'''
import pygame
import time
import random

from Tank import Tank, EnemyTank
from Bullet import Bullet
from Explode import Explode
from Wall import Wall
from Music import Music

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 360
BG_COLOR = (0, 0, 0)
FONT_COLOR = (255, 0, 0)


# 主类
class MainGame:
    def __init__(self):
        pass
        # 设置窗口大小,MainGame.window是surface类型
        self.window = None
        # 我方坦克
        self.my_tank = None
        # 我方坦克子弹
        self.my_tank_bullets = []
        # 敌方坦克
        self.enemy_tanks = []
        # 敌方子弹
        self.enemy_tanks_bullets = []
        # 初始化敌方坦克的数量
        self.enemy_tanks_num = 5
        # 死亡次数
        self.game_num = 0
        # 爆炸
        self.explodes = []
        # 墙壁
        self.walls = []
        # 加载音乐
        self.music = Music()


    # 开始游戏
    def start_game(self):
        # 初始化窗口
        pygame.display.init()
        # 设置窗口大小,MainGame.window是surface类型
        self.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        # 设置标题
        pygame.display.set_caption("坦克大战1.0")
        # 加载我方坦克
        self.my_tank = Tank(0, 0)
        # 开始音效
        self.music.start_music.play()
        # 加载敌方坦克
        self.get_enemy_tanks(self.enemy_tanks_num)
        # 加载墙壁
        self.create_walls()
        # 刷新显示
        while True:
            time.sleep(0.02)  # 0.02s刷新一下
            # 填充颜色
            pygame.Surface.fill(self.window, BG_COLOR)
            # 显示字,blit是在一个surface上绘制另一个surface
            self.window.blit(self.set_text_suface("敌方坦克数量：%d" % self.enemy_tanks_num), dest=[10, 10])
            self.window.blit(self.set_text_suface("死亡次数：%d" % self.game_num), dest=[10, 30])
            # 获取响应事件
            self.get_event()
            # 移动
            if not self.my_tank.stop:
                self.my_tank.move()
            # 显示我的坦克
            if self.my_tank.flag:
                self.my_tank.display_tank(self.window)
            # 遍历显示我方子弹
            self.blit_my_tank_bullet()
            # 遍历显示敌方坦克
            self.blit_enemy_tanks()
            # 遍历显示敌方坦克子弹
            self.blit_enemy_tanks_bullets()
            # 遍历显示爆炸
            self.blit_explodes()
            # 遍历显示墙壁
            self.blit_walls()
            # 检测
            self.enemy_and_my()
            # 刷新
            pygame.display.update()

    # 结束游戏
    def end_game(self):
        print("Game Over")
        exit()

    # 设置文字
    def set_text_suface(self, text):
        # 初始化字体
        pygame.font.init()
        # 设置字体,font是surface类型
        font = pygame.font.SysFont("kaiti", 18)
        # 绘制字体
        text_surface = font.render(text, True, FONT_COLOR)

        return text_surface

    # 显示子弹
    def blit_my_tank_bullet(self):
        for bullet in self.my_tank_bullets:
            if bullet.flag:  # 判断子弹的状态
                # 显示
                bullet.display_bullet(self.window)
                # 移动
                bullet.move()
            else:
                self.my_tank_bullets.remove(bullet)

    # 加载敌方坦克
    def get_enemy_tanks(self, num):
        for i in range(num):
            # 随机生成坦克的位置
            left = random.randint(50, SCREEN_WIDTH - 30)
            top = random.randint(50, SCREEN_HEIGHT - 30)
            enemy = EnemyTank(left, top, 2)
            self.enemy_tanks.append(enemy)

    # 遍历显示敌方坦克
    def blit_enemy_tanks(self):
        for tank in self.enemy_tanks:
            # 显示敌方坦克
            tank.display_tank(self.window)
            # 随机化移动
            tank.random_move()
            # 子弹
            enemy_bullet = tank.shot(tank)
            if enemy_bullet:  # 判断状态
                self.enemy_tanks_bullets.append(enemy_bullet)

    # 遍历显示敌方坦克的子弹
    def blit_enemy_tanks_bullets(self):
        for i, bullet in enumerate(self.enemy_tanks_bullets):
            if bullet.flag:  # 判断状态
                bullet.display_bullet(self.window)
                # 移动
                bullet.move()
                # self.enemy_bullets_and_my_tank()
            else:  # 删除没有用的子弹
                self.enemy_tanks_bullets.remove(self.enemy_tanks_bullets[i])

    # 遍历显示爆炸效果
    def blit_explodes(self):
        for i, explode in enumerate(self.explodes):
            if explode.flag:  # 存在显示
                explode.display_explode(self.window)
            else:  # 不存在删除
                self.explodes.remove(self.explodes[i])

    # 创建墙壁
    def create_walls(self):
        for i in range(1, SCREEN_WIDTH, 150):
            wall = Wall(i, SCREEN_HEIGHT / 2.)
            self.walls.append(wall)

    # 遍历显示墙壁
    def blit_walls(self):
        for j, wall in enumerate(self.walls):
            if wall.lives > 0:
                wall.display_wall(self.window)
            else:
                self.walls.remove(self.walls[j])

    # 检测
    def enemy_and_my(self):
        # 敌方坦克和我方子弹的碰撞检测
        for enemy in self.enemy_tanks:
            for i, my_bullet in enumerate(self.my_tank_bullets):
                if pygame.sprite.collide_rect(enemy, my_bullet):  # 判断是否碰撞
                    # 添加爆炸效果
                    explode = Explode(enemy)
                    self.explodes.append(explode)
                    # hit音效
                    self.music.hit_music.play()
                    # 删除敌方坦克
                    self.enemy_tanks.remove(enemy)
                    self.enemy_tanks_num -= 1  # 数量－1
                    # 删除碰撞之后的子弹
                    self.my_tank_bullets.remove(self.my_tank_bullets[i])

        # 检测两个敌方坦克是相撞
        for i, enemy1 in enumerate(self.enemy_tanks):
            for j, enemy2 in enumerate(self.enemy_tanks):
                if enemy1 != enemy2:
                    if pygame.sprite.collide_rect(enemy1, enemy2):
                        self.enemy_tanks[i].direction = self.enemy_tanks[i].f_direction(self.enemy_tanks[i].direction)

        # 检测我方坦克和敌方坦克
        for enemy in self.enemy_tanks:
            if pygame.sprite.collide_rect(enemy, self.my_tank):  # 判断是否碰撞
                self.my_tank.flag = 0
                # 添加爆炸效果
                explode = Explode(self.my_tank)
                self.explodes.append(explode)
                # hit音效
                self.music.hit_music.play()
                self.my_tank = Tank(0, 0)  # 复活
                self.game_num += 1

        # 检测敌方子弹和我方坦克
        # def enemy_bullets_and_my_tank(self):
        for i, enemy_bullet in enumerate(self.enemy_tanks_bullets):
            if pygame.sprite.collide_rect(self.my_tank, enemy_bullet):  # 判断是否碰撞
                self.my_tank.flag = 0
                self.enemy_tanks_bullets[i].flag = 0
                self.enemy_tanks_bullets.remove(self.enemy_tanks_bullets[i])
                # 添加爆炸效果
                explode = Explode(self.my_tank)
                self.explodes.append(explode)
                self.my_tank = Tank(0, 0)  # 复活
                self.game_num += 1

        # 检测敌方子弹和墙
        for i, enemy_bullet in enumerate(self.enemy_tanks_bullets):
            for j, wall in enumerate(self.walls):
                if pygame.sprite.collide_rect(wall, enemy_bullet):  # 判断是否碰撞
                    self.enemy_tanks_bullets[i].flag = 0
                    self.walls[j].lives -= 1  # 生命减去1

        # 检测我方子弹和墙
        for i, bullet in enumerate(self.my_tank_bullets):
            for j, wall in enumerate(self.walls):
                if pygame.sprite.collide_rect(wall, bullet):  # 判断是否碰撞
                    self.my_tank_bullets[i].flag = 0
                    self.walls[j].lives -= 1  # 生命减去1

        # 检测墙和坦克们
        for wall in self.walls:
            # 我方坦克
            if pygame.sprite.collide_rect(wall, self.my_tank):  # 判断是否碰撞
                # 回到上一步的位置
                self.my_tank.stay()
                # 敌方坦克
            for i, enemy in enumerate(self.enemy_tanks):
                if pygame.sprite.collide_rect(wall, enemy):  # 判断是否碰撞
                    self.enemy_tanks[i].stay()

    # 获取事件
    def get_event(self):
        # 获取所有事件
        event_list = pygame.event.get()
        # 遍历所有事件
        for event in event_list:
            # 关闭
            if event.type == pygame.QUIT:
                self.end_game()
            # 按键按下
            if event.type == pygame.KEYDOWN:
                # 判断按下的是上、下、左、右
                if event.key == pygame.K_LEFT:
                    print('按下左键，坦克向左移动')
                    self.my_tank.direction = 'L'
                    self.my_tank.stop = False
                elif event.key == pygame.K_RIGHT:
                    print('按下右键，坦克向右移动')
                    self.my_tank.direction = 'R'
                    self.my_tank.stop = False
                elif event.key == pygame.K_UP:
                    print('按下上键，坦克向上移动')
                    self.my_tank.direction = 'U'
                    self.my_tank.stop = False
                elif event.key == pygame.K_DOWN:
                    print('按下上键，坦克向下移动')
                    self.my_tank.direction = 'D'
                    self.my_tank.stop = False
                elif event.key == pygame.K_SPACE:
                    # 射击
                    print("发射子弹")
                    # 创建子弹
                    my_bullet = self.my_tank.shot(self.my_tank)

                    # 添加
                    if len(self.my_tank_bullets) < 4:  # 最多添加4个子弹
                        self.my_tank_bullets.append(my_bullet)
                        # fire音效
                        self.music.fire_music.play()

            # 按键抬起
            elif event.type == pygame.KEYUP:  # 按键抬起
                # 只有是方向键抬起时才停止移动
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN \
                        or event.key == pygame.K_UP:
                    self.my_tank.stop = True  # 停止移动


if __name__ == '__main__':
    my_game = MainGame()
    my_game.start_game()
