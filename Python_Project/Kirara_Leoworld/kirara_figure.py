'''
Author = Leo
Date = 19.10.04
Subscription = to store class
'''
import pygame

# 作品集，程序设定
class Work():
    def __init__(self, name, year, company):
        self.name = name
        self.year = year
        self.producer = company

class Figure():
    # to initialize girls
    def __init__(self, name, root, grade, level, weapon, sound, skilllevel,
                 love, eyecolor, haircolor):
        self.name = name
        self.root = root
        self.grade = grade
        self.level = level
        self.weapon = weapon
        self.sound = sound
        self.skilllevel = skilllevel
        self.love = love
        self.eyecolor = eyecolor
        self.haircolor = haircolor

    # level up one
    def level_up(self):
        self.level += 1

    # love up one & multi
    def love_up_one(self):
        self.love += 1

    def love_up_multi(self, diff):
        self.love += diff

'''
    # output the girl's short info
    def output_figure_info_short(self):
        print("姓名: " + str(self.name))
        print("等级: " + str(self.level))
        print("星级: " + str(self.grade))

    # output the girl's basic info
    def output_figure_info_basic(self):
        print("姓名: " + str(self.name))
        print("来源: " + str(self.root))
        print("等级: " + str(self.level))
        print("星级: " + str(self.grade))
        print("武器: " + str(self.weapon))
        print("技能等级: " + str(self.skilllevel))

    # output the girl's full info
    def output_figure_info_full(self):
        print("姓名: " + str(self.name))
        print("来源: " + str(self.root))
        print("等级: " + str(self.level))
        print("星级: " + str(self.grade))
        print("武器: " + str(self.weapon))
        print("声优: " + str(self.sound))
        print("技能等级: " + str(self.skilllevel))
        print("眼睛颜色: " + str(self.eyecolor))
        print("头发颜色: " + str(self.haircolor))
'''

# 武器
class Weapon():
    # to initialize weapons,level means its level limit
    def __init__(self, name, level, skill):
        self.name = name
        self.level = level
        self.skill = skill

    # output the weapon's info
    def output_weapon_info(self):
        print("武器名: " + str(self.name))
        print("等级限制: " + str(self.level))
        print("技能: " + str(self.level))



# 创建按钮类
class Button():
    def __init__(self, width, height, screen, msg, positionX, positionY):
        # 初始化按钮属性
        self.screen = screen
        self.screen_rect = screen.get_rect()
        # 设置按钮长宽
        self.width, self.height = width, height
        self.button_color = (205,133,63)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont('KaiTi', 58)
        '''
            宋体：simsunnsimsun 
            黑体：SimHei
            仿宋：FangSong
            楷体：KaiTi
        '''
        # 创建按钮rect对象
        self.rect = pygame.Rect(positionX, positionY, self.width, self.height)
        # 按钮标签
        self.prep_msg(msg)

    # Button类函数，将标签渲染为图像并居中
    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    # 绘制按钮
    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

# 存储游戏设置
class Settings():
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255,222,173)

# 显示基础文字块类，左一右二
class TextBasic():
    def __init__(self, width, height, screen, positionX, positionY, msg1='',
                 msg2='', msg3=''):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width, self.height = width, height
        self.bg_color = (240,128,128)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont('KaiTi', 20)
        self.positionX = positionX
        self.positionY = positionY
        self.rect = pygame.Rect(positionX, positionY, self.width, self.height)
        self.msg1 = msg1
        self.msg2 = msg2
        self.msg3 = msg3

        # 文字标签
        self.prep_msg()


    # 将标签渲染为图像
    def prep_msg(self):
        self.msg1_image = self.font.render(self.msg1, True, self.text_color,
                                          self.bg_color)
        self.msg1_image_rect = pygame.Rect(self.positionX + 20,
                                           self.positionY + 20, 200, 50)

        self.msg2_image = self.font.render(self.msg2, True, self.text_color,
                                           self.bg_color)
        self.msg2_image_rect = pygame.Rect(self.positionX + 240,
                                           self.positionY + 20, 50, 50)

        self.msg3_image = self.font.render(self.msg3, True, self.text_color,
                                           self.bg_color)
        self.msg3_image_rect = pygame.Rect(self.positionX + 240,
                                           self.positionY + 60, 100, 50)

    # 绘制基础文字块
    def draw_textbasic(self):
        self.screen.fill(self.bg_color, self.rect)
        self.screen.blit(self.msg1_image, self.msg1_image_rect)
        self.screen.blit(self.msg2_image, self.msg2_image_rect)
        self.screen.blit(self.msg3_image, self.msg3_image_rect)

# 显示基础女孩类，左一右二
class GirlBasic():
    def __init__(self, width, height, screen, positionX, positionY, girl):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width, self.height = width, height
        self.bg_color = (240,128,128)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont('KaiTi', 20)
        self.positionX = positionX
        self.positionY = positionY
        self.rect = pygame.Rect(positionX, positionY, self.width, self.height)
        self.girl = girl

        # 文字标签
        self.prep_msg()

    # 将标签渲染为图像
    def prep_msg(self):
        self.msg1_image = self.font.render(self.girl.name, True, self.text_color,
                                          self.bg_color)
        self.msg1_image_rect = pygame.Rect(self.positionX + 20,
                                           self.positionY + 20, 120, 50)

        self.msg2_image = self.font.render('等级: ' + str(self.girl.level),
                                           True, self.text_color, self.bg_color)
        self.msg2_image_rect = pygame.Rect(self.positionX + 140,
                                           self.positionY + 20, 50, 50)

        self.msg3_image = self.font.render('星级: ' + self.girl.grade,
                                           True, self.text_color, self.bg_color)
        self.msg3_image_rect = pygame.Rect(self.positionX + 140,
                                           self.positionY + 60, 100, 50)

    # 绘制基础文字块
    def draw_textbasic(self):
        self.screen.fill(self.bg_color, self.rect)
        self.screen.blit(self.msg1_image, self.msg1_image_rect)
        self.screen.blit(self.msg2_image, self.msg2_image_rect)
        self.screen.blit(self.msg3_image, self.msg3_image_rect)