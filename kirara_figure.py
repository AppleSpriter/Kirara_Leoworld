'''
Author = Leo
Date = 19.10.04
Subscription = to store class
'''
import pygame
import time
import sys
import datetime

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

# 绘制抽卡块
class LotteryBasic():
    def __init__(self, screen, lottery_times):
        self.screen = screen
        # 剩余次数提示
        self.bg_color = (240,128,128)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont('KaiTi', 20)
        self.tip_rect = pygame.Rect(400, 40, 160, 25)
        self.msg1 = "剩余抽奖次数：" + str(lottery_times)
        self.msg2 = "剩余抽奖次数：" + str(lottery_times - 1)
        # 卡背
        self.bg_image = pygame.image.load(r"image//back.png")
        self.bgbig_image = pygame.image.load(r"image//back_big.png")
        self.back_positionX = 150
        self.back_positionY = 130
        self.back_width = 300
        self.back_height = 400
        self.back_rect = pygame.Rect(self.back_positionX, self.back_positionY, 
                                     self.back_width, self.back_height)
        self.backbig_rect = pygame.Rect(self.back_positionX - 30, self.back_positionY - 40, 
                                     self.back_width, self.back_height)
        # 奖励参数
        self.reward_font = pygame.font.SysFont('KaiTi', 40)
        self.reward_color = (255, 255, 255)
        # 声音参数
        self.unopen_sound = pygame.mixer.Sound("sound//unopened_pack.ogg")
        self.card_sound = pygame.mixer.Sound("sound//rare.ogg")
        self.over_sound = pygame.mixer.Sound("sound//card_over_rare.ogg")
        # 文字、卡背标签
        self.prep_msg()

    # 渲染剩余次数为图像
    def prep_msg(self):
        self.msg1_image = self.font.render(self.msg1, True, self.text_color,
                                          self.bg_color)
        self.msg2_image = self.font.render(self.msg2, True, self.text_color,
                                          self.bg_color)
        self.msg_image_rect = pygame.Rect(400, 40, 200, 50)

    # 绘制卡背
    def draw_lotteryback(self):
        # 绘制剩余次数
        self.screen.fill(self.bg_color, self.tip_rect)
        self.screen.blit(self.msg1_image, self.msg_image_rect)
        # 绘制卡背位图
        self.screen.blit(self.bg_image, self.back_rect)

    # 鼠标悬停离开点击效果
    def draw_mouseeffect(self, mouse, reward="", color=0, golden=0):
        # Mouse 0 无效果. 1 悬停效果. 2 离开效果. 3 点击效果
        if mouse == 1:
            # 图像向外扩大
            # 绘制卡背位图
            self.screen.blit(self.bgbig_image, self.backbig_rect)
            # 播放音效
            self.unopen_sound.set_volume(0.01)
            self.unopen_sound.play()

            # 绘制剩余次数
            self.screen.fill(self.bg_color, self.tip_rect)
            self.screen.blit(self.msg1_image, self.msg_image_rect)
        if mouse == 2:
            # 图像恢复原来大小
            # 绘制卡背位图
            self.screen.blit(self.bg_image, self.back_rect)
            # 停止音效
            self.unopen_sound.stop()

            # 绘制剩余次数
            self.screen.fill(self.bg_color, self.tip_rect)
            self.screen.blit(self.msg1_image, self.msg_image_rect)
        if mouse == 3:
            # 停止播放音效
            self.unopen_sound.stop()
            # 判断奖励颜色和音效
            if color == 0 and golden == 0:
                self.reward_color = (240,248,255)
                self.card_sound = False
                self.over_sound = pygame.mixer.Sound("sound//card_over_normal.ogg")
            elif color == 1 and golden == 0:
                self.reward_color = (30,144,255)
            elif color == 2 and golden == 0:
                self.reward_color = (153,50,204)
                self.card_sound = pygame.mixer.Sound("sound//epic.ogg")
                self.over_sound = pygame.mixer.Sound("sound//card_over_epic.ogg")
            elif color == 3 and golden == 0:
                self.reward_color = (255,130,71)
                self.card_sound = pygame.mixer.Sound("sound//legend.ogg")
                self.over_sound = pygame.mixer.Sound("sound//card_over_legend.ogg")
            elif color == 0 and golden == 1:
                self.reward_color = (240,248,255)
                self.card_sound = pygame.mixer.Sound("sound//golden_C.ogg")
                self.over_sound = pygame.mixer.Sound("sound//card_over_normal.ogg")
            elif color == 1 and golden == 1:
                self.reward_color = (30,144,255)
                self.card_sound = pygame.mixer.Sound("sound//golden_R.ogg")
                self.over_sound = pygame.mixer.Sound("sound//card_over_rare.ogg")
            elif color == 2 and golden == 1:
                self.reward_color = (153,50,204)
                self.card_sound = pygame.mixer.Sound("sound//golden_E.ogg")
                self.over_sound = pygame.mixer.Sound("sound//card_over_epic.ogg")
            elif color == 3 and golden == 1:
                self.reward_color = (255,130,71)
                self.card_sound = pygame.mixer.Sound("sound//golden_L.ogg")
                self.over_sound = pygame.mixer.Sound("sound//card_over_legend.ogg")

            # 图像转化为奖励,利用big_image的颜色框，里面一个背景框框着奖励文字
            self.screen.fill(self.reward_color, self.backbig_rect)
            msg3 = self.reward_font.render(reward, True, self.reward_color, (205, 201,165))
            msg3_rect = pygame.Rect(self.back_positionX + 30,
                                           self.back_positionY + 100, 100, 50)
            # 显示奖励文字
            self.screen.blit(msg3, msg3_rect)
            # 显示卡牌和翻面声音
            if self.card_sound:
                self.card_sound.play()
            self.over_sound.play()

            # 绘制剩余次数
            self.screen.fill(self.bg_color, self.tip_rect)
            self.screen.blit(self.msg2_image, self.msg_image_rect)

# 倒计时类
class DecTime(object):
    def __init__(self, screen, totalTime):
        self.screen = screen
        self.bg_color = (255, 236, 139)
        self.font1 = pygame.font.SysFont('KaiTi', 60)
        self.font2 = pygame.font.SysFont('KaiTi', 70)
        # 将秒转化为时分秒
        self.sec = totalTime
        self.hour = int(self.sec / 3600)
        self.sec = self.sec % 3600
        self.minute = int(self.sec / 60)
        self.sec = int(self.sec % 60)

    def draw_timedec(self, text, ch):
        self.screen.fill(self.bg_color)
        self.screen.blit(self.font1.render(text, True,(238, 99, 99)), (170, 200))
        self.screen.blit(self.font2.render(ch, True,(238, 99, 99)), (200, 400))

    # 时间减    
    def subTime(self):
        if self.sec > 0:
            self.sec -=  1
        else:
            if self.minute > 0:
                self.minute -= 1
                self.sec = 59
            else:
                if self.hour > 0:
                    self.hour -= 1
                    self.minute = 59
                    self.sec = 59
                else:
                    self.sec = -1


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

        self.msg2_image = self.font.render('等级:' + str(self.girl.level),
                                           True, self.text_color, self.bg_color)
        self.msg2_image_rect = pygame.Rect(self.positionX + 20,
                                           self.positionY + 60, 50, 50)
        if self.girl.grade == 'A':
            self.msg3_image = self.font.render('星级:' + self.girl.grade +
                                               '  好感:'
                                               + str(self.girl.love) + "/50",
                                               True, self.text_color, self.bg_color)
        elif self.girl.grade == 'S':
            self.msg3_image = self.font.render('星级:' + self.girl.grade +
                                               '  好感:'
                                               + str(self.girl.love) + "/150",
                                               True, self.text_color,
                                               self.bg_color)
        elif self.girl.grade == 'SS':
            self.msg3_image = self.font.render('星级:' + self.girl.grade +
                                               '  好感:'
                                               + str(self.girl.love) + "/350",
                                               True, self.text_color,
                                               self.bg_color)
        elif self.girl.grade == 'SSS':
            self.msg3_image = self.font.render('星级:' + self.girl.grade +
                                               '  好感:'
                                               + str(self.girl.love) + "/650",
                                               True, self.text_color,
                                               self.bg_color)
        elif self.girl.grade == 'EX':
            self.msg3_image = self.font.render('星级:' + self.girl.grade +
                                               '  好感:'
                                               + str(self.girl.love) + "/1000",
                                               True, self.text_color,
                                               self.bg_color)
        elif self.girl.grade == 'MAX':
            self.msg3_image = self.font.render('星级:' + self.girl.grade +
                                               '  好感:'
                                               + str(self.girl.love) + "/MAX",
                                               True, self.text_color,
                                               self.bg_color)
        self.msg3_image_rect = pygame.Rect(self.positionX + 140,
                                           self.positionY + 60, 100, 50)

        self.msg4_image = self.font.render('武器:'+ self.girl.weapon, True,
                                           self.text_color, self.bg_color)
        self.msg4_image_rect = pygame.Rect(self.positionX + 230,
                                           self.positionY + 20, 50, 50)

        self.msg5_image = self.font.render('眼色: ' + self.girl.eyecolor, True,
                                           self.text_color, self.bg_color)
        self.msg5_image_rect = pygame.Rect(self.positionX + 370,
                                           self.positionY + 20, 50, 50)

        self.msg6_image = self.font.render('发色: ' + self.girl.haircolor, True,
                                           self.text_color, self.bg_color)
        self.msg6_image_rect = pygame.Rect(self.positionX + 370,
                                           self.positionY + 60, 50, 50)

        self.msg7_image = self.font.render('技能:' + str(self.girl.skilllevel),
                                           True, self.text_color, self.bg_color)
        self.msg7_image_rect = pygame.Rect(self.positionX + 140,
                                           self.positionY + 20, 50, 50)

    # 绘制基础文字块
    def draw_textbasic(self):
        self.screen.fill(self.bg_color, self.rect)
        self.screen.blit(self.msg1_image, self.msg1_image_rect)
        self.screen.blit(self.msg2_image, self.msg2_image_rect)
        self.screen.blit(self.msg3_image, self.msg3_image_rect)
        self.screen.blit(self.msg4_image, self.msg4_image_rect)
        self.screen.blit(self.msg5_image, self.msg5_image_rect)
        self.screen.blit(self.msg6_image, self.msg6_image_rect)
        self.screen.blit(self.msg7_image, self.msg7_image_rect)

    def draw_infolottery(self):
        self.screen.fill(self.bg_color, self.rect)
        self.screen.blit(self.msg1_image, self.msg1_image_rect)
        self.screen.blit(self.msg2_image, self.msg2_image_rect)
        self.screen.blit(self.msg3_image, self.msg3_image_rect)
        self.screen.blit(self.msg4_image, self.msg4_image_rect)
        self.screen.blit(self.msg5_image, self.msg5_image_rect)
        self.screen.blit(self.msg6_image, self.msg6_image_rect)
        self.screen.blit(self.msg7_image, self.msg7_image_rect)
