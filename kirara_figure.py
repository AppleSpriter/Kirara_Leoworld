'''
Author = Leo
Date = 19.10.04
Subscription = to store class
'''
import pygame
import time
import sys
import os
import datetime
from formula import *


class Work(object):
    """番剧作品类

    Attribute:
        name: 番剧名
        year: 播出年份
        company: 制作公司

    """
    def __init__(self, name, year, company):
        self.name = name
        self.year = year
        self.producer = company

class Figure(object):
    # 通用角色类
    # to initialize girls
    def __init__(self, gid, name, root, grade, weapon_type, feature, feature_info, moe, yxr, intimacy, enthusiasm, m_coefficient, y_coefficient, i_coefficient, e_coefficient, sound, love, level, eyecolor, haircolor, weapon_hold="", stigma_up="", stigma_mid="", stigma_down="", skin="", fragment=0, exp=0):
        self.id = gid
        self.name = name
        self.root = root
        self.grade = grade
        self.weapon_type = weapon_type
        self.feature = feature
        self.feature_info = feature_info
        self.moe = moe
        self.yxr = yxr
        self.intimacy = intimacy
        self.enthusiasm = enthusiasm
        self.m_coefficient = m_coefficient
        self.y_coefficient = y_coefficient
        self.i_coefficient = i_coefficient
        self.e_coefficient = e_coefficient
        self.level = level
        self.sound = sound
        self.love = love
        self.eyecolor = eyecolor
        self.haircolor = haircolor
        #拥有角色属性
        self.weapon_hold = "无" if weapon_hold==None else weapon_hold
        self.stigma_up = stigma_up
        self.stigma_mid = stigma_mid
        self.stigma_down = stigma_down
        self.skin = skin
        self.fragment = fragment
        self.exp = exp


class Weapon(object):
    # 武器
    def __init__(self, idx, name, level, moe, awaken, equip_figure_name, typed, grade, m_coefficient, feature, feature_info, value1, value2, value3, value4, value5):
        self.idx = idx
        self.name = name
        self.level = level
        self.moe = moe
        self.awaken = awaken
        self.equip_figure_name = equip_figure_name
        self.typed = typed
        self.grade = grade
        self.m_coefficient = m_coefficient
        self.feature = feature
        self.feature_info = feature_info
        self.value1 = value1
        self.value2 = value2
        self.value3 = value3
        self.value4 = value4
        self.value5 = value5

class Material(object):
    '''消耗品类
    '''
    def __init__(self, idx, name, number, typed):
        self.idx = idx
        self.name = name
        self.number = number
        self.typed = typed

class Mission(object):
    '''任务类
    '''
    def __init__(self, missionid, name, description, typed, addeddate, reward, complete, finish, getreward):
        self.missionid = missionid
        self.name = name
        self.description = description
        self.typed = typed
        self.addeddate = addeddate
        self.reward = reward
        self.complete = complete
        self.finish = finish
        self.getreward = getreward


# 创建按钮类
class Button(object):
    def __init__(self, width, height, screen, msg, positionX, positionY, clickable=1):
        # 初始化按钮属性
        self.screen = screen
        self.screen_rect = screen.get_rect()
        # 设置按钮长宽
        self.width, self.height = width, height
        #v1.1橙色+黄色配色
        # self.button_color = (205,133,63)
        # self.text_color = (255, 255, 255)
        # v1.2紫罗兰色+灰色+灰色配色
        # self.button_color = ( 216, 191, 216)
        # self.text_color = ( 139, 131, 134)
        # self.shadow_color = (255, 222, 173)
        # v2.1黄色+红色+米色配色
        self.button_color = ( 200, 0, 0)
        self.text_color = ( 255, 242, 0)
        self.shadow_color = ( 255, 228, 225)
        self.font = pygame.font.SysFont('KaiTi', 58)
        self.clickable = clickable
        '''
            宋体：simsunnsimsun 
            黑体：SimHei
            仿宋：FangSong
            楷体：KaiTi
        '''
        # 创建3d按钮（阴影）
        self.shadow = pygame.Rect(positionX+10, positionY+10, self.width, self.height)
        # 创建按钮rect对象
        self.rect = pygame.Rect(positionX, positionY, self.width, self.height)
        # 按钮标签
        self.prep_msg(msg)

    # Button类函数，将标签渲染为图像并居中
    def prep_msg(self, msg):
        # 无法点击状态
        if self.clickable == 0:
            self.button_color = (105, 105, 105)
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        self.msg_image_shadow = self.msg_image.get_rect()
        self.msg_image_shadow.center = self.shadow.center

    # 绘制按钮
    def draw_button(self, height=1):
        # 无法点击状态
        if self.clickable == 0:
            self.button_color = (105, 105, 105)
        elif height == 1:
            self.screen.fill(self.shadow_color, self.shadow)
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    # 绘制按下的按钮
    def draw_pressed_button(self):
        # 无法点击状态
        if self.clickable == 0:
            self.button_color = (105, 105, 105)
            self.screen.fill(self.button_color, self.rect)
            self.screen.blit(self.msg_image, self.msg_image_rect)
        else:
            self.screen.fill(self.button_color, self.shadow)
            self.screen.blit(self.msg_image, self.msg_image_shadow)

# 存储通用游戏设置
class Settings(object):
    def __init__(self):
        self.screen_width = 1130
        self.screen_height = 800
        self.bg_color = (255,222,173)

# 存储小窗口游戏设置
class Settingssmallwindow(object):
    def __init__(self):
        self.screen_width = 598
        self.screen_height = 806
        self.bg_color = (255,222,173)

# 显示基础文字块类，左一右二
class TextBasic(object):
    def __init__(self, width, height, screen, positionX, positionY, msg1='',
                 msg2='', msg3='', msg4=''):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width, self.height = width, height
        self.bg_color = (102,205,170)       # MediumAquamarine
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont('KaiTi', 20)
        self.positionX = positionX
        self.positionY = positionY
        self.rect = pygame.Rect(positionX, positionY, self.width, self.height)
        self.msg1 = msg1
        self.msg2 = msg2
        self.msg3 = msg3
        self.msg4 = msg4
        self.prep_msg()     # 文字标签

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

        self.msg4_image = self.font.render(self.msg4, True, self.text_color,
                                           self.bg_color)
        self.msg4_image_rect = pygame.Rect(self.positionX, self.positionY, 200, 20)

    # 绘制基础文字块
    def draw_textbasic(self):
        self.screen.fill(self.bg_color, self.rect)
        self.screen.blit(self.msg1_image, self.msg1_image_rect)
        self.screen.blit(self.msg2_image, self.msg2_image_rect)
        self.screen.blit(self.msg3_image, self.msg3_image_rect)

    # 绘制选中文字块
    def draw_pressed_textbasic(self):
        self.color = (76, 45, 51)
        self.screen.fill(self.bg_color, self.rect)
        self.screen.blit(self.msg1_image, self.msg1_image_rect)
        self.screen.blit(self.msg2_image, self.msg2_image_rect)
        self.screen.blit(self.msg3_image, self.msg3_image_rect)

    # 绘制主页文字块
    def draw_home_page_text(self):
        self.screen.fill(self.bg_color, self.rect)
        self.screen.blit(self.msg4_image, self.msg4_image_rect)

# 显示任务类
class MissionBasic(object):
    def __init__(self, width, height, screen, positionX, positionY, mission):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width, self.height = width, height
        self.bg_color = (187, 255, 255)
        self.pressed_color = (180, 238, 180)
        self.text_color = (0, 0, 0)
        self.have_text_color = (255, 228, 196)
        self.have_bg_color = (0, 197, 205)
        self.already_bg_color = (190, 190, 190)
        self.font = pygame.font.SysFont('KaiTi', 20)
        self.have_font = pygame.font.SysFont('KaiTi', 40)
        self.positionX = positionX
        self.positionY = positionY
        self.ready_to_click = False
        self.rect = pygame.Rect(positionX, positionY, self.width, self.height)
        self.mission = mission
        self.prep_msg()                     # 文字标签
        
    def prep_msg(self): # 将标签渲染为图像
        self.id_image = self.font.render(str(self.mission.missionid), True, self.text_color, self.bg_color)
        self.id_image_rect = pygame.Rect(self.positionX + 20, self.positionY + 20, 70, 50)
        self.name_image = self.font.render(self.mission.name, True, self.text_color, self.bg_color)
        self.name_image_rect = pygame.Rect(self.positionX + 50, self.positionY + 20, 150, 50)
        self.reward_image = self.font.render("奖励:" + self.mission.reward, True, self.text_color, self.bg_color)
        self.reward_image_rect = pygame.Rect(self.positionX + 400, self.positionY + 20, 150, 50)
        #如果不是浮点数就去掉后面的.0
        if self.mission.complete%1 == 0:
            self.mission.complete = int(self.mission.complete)
        self.finish_image = self.font.render("完成度: " + str(self.mission.complete) + "/" 
                                                + str(int(self.mission.finish)), True, self.text_color, self.bg_color)
        self.finish_image_rect = pygame.Rect(self.positionX + 600, self.positionY + 20, 50, 50)
        self.have_image = self.have_font.render("领取奖励", True, self.have_text_color, self.have_bg_color)
        self.have_image_rect = pygame.Rect(self.positionX + 830, self.positionY+6, 200, 80)
        self.already_image = self.have_font.render("已领取", True, self.have_text_color, self.already_bg_color)
        self.already_image_rect = pygame.Rect(self.positionX + 850, self.positionY+6, 200, 80)

    def draw_missionbasic(self):
        self.screen.fill(self.bg_color, self.rect)
        self.screen.blit(self.id_image, self.id_image_rect)
        self.screen.blit(self.name_image, self.name_image_rect)
        self.screen.blit(self.reward_image, self.reward_image_rect)
        self.screen.blit(self.finish_image, self.finish_image_rect)
        if self.mission.getreward==1:
            self.screen.blit(self.already_image, self.already_image_rect)
            self.ready_to_click = False
        elif self.mission.finish <= self.mission.complete:
            self.screen.blit(self.have_image, self.have_image_rect)
            self.ready_to_click = True
        # pygame.draw.rect(self.screen, (0,0,0), ((self.positionX + 20, self.positionY + 60),(340, 20)), 2)
        # if self.afterpercent != self.percent:
        #     pygame.draw.rect(self.screen, (0,0,0), ((self.positionX + 22 + 3.4*self.percent, self.positionY + 62),(1, 17)), 0)
        # pygame.draw.rect(self.screen, (240,128,128), ((self.positionX + 22, self.positionY + 62),(3.4*self.percent, 17)), 0)

    def get_mission(self):
        return self.mission

    def set_mission_complete(self):
        '''设置任务完成，主要用于点击领取奖励后页面的即时刷新
        '''
        self.mission.getreward = 1
        return self.mission


# 显示投入事件进度条文字块类，左一右二带左进度条
class AdventureBasic(object):
    def __init__(self, width, height, screen, positionX, positionY, adventure,
                 duration_minutes=0):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width, self.height = width, height
        self.id = adventure['adventureid']
        self.bg_color = self.choose_bg_color(self.id)
        self.pressed_color = (180, 238, 180)
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont('KaiTi', 20)
        self.positionX = positionX
        self.positionY = positionY
        self.rect = pygame.Rect(positionX, positionY, self.width, self.height)
        self.name = adventure['name']
        self.lastopendate = str(adventure['lastopendate'])
        self.planinvest = str(round(adventure['planinvest'] / 60,1)) + "h"
        self.afterpercent = round((adventure['nowinvest'] + duration_minutes) * 100 
            / adventure['planinvest'], 2)
        self.percent = round(adventure['nowinvest'] * 100 / adventure['planinvest'], 2)
        self.str_id = str(adventure['adventureid']) + "."
        self.adventure = adventure
        self.prep_msg()                     # 文字标签
        self.prep_msg_pressed()             # 选中的文字标签

    # 按照顺序换背景颜色
    def choose_bg_color(self, idNumber):
        # 颜色名按顺序：Honeydew2浅绿、Aquamarine鲜艳蓝绿、LightSteelBlue1牛仔蓝、LightG oldenrod1金黄、
        #               LightSalmon1橙红、Thistle紫罗兰、PeachPuff2棕色
        color_list = [(224,238,224),(127, 255, 212),(202, 225, 255),(255, 236, 139),(255, 160, 122),
                      (216, 191, 216),(238, 203, 173)]
        return color_list[(int(idNumber)-1)%len(color_list)]

    def prep_msg(self): # 将标签渲染为图像
        self.id_image = self.font.render(self.str_id, True, self.text_color,
                                          self.bg_color)
        self.id_image_rect = pygame.Rect(self.positionX + 20,
                                           self.positionY + 20, 70, 50)
        self.name_image = self.font.render(self.name, True, self.text_color,
                                          self.bg_color)
        self.name_image_rect = pygame.Rect(self.positionX + 50,
                                           self.positionY + 20, 150, 50)
        self.lastopendate_image = self.font.render(self.lastopendate, True, self.text_color,
                                           self.bg_color)
        self.lastopendate_image_rect = pygame.Rect(self.positionX + 300,
                                           self.positionY + 20, 150, 50)
        self.planinvest_image = self.font.render(self.planinvest, True, self.text_color,
                                           self.bg_color)
        self.planinvest_image_rect = pygame.Rect(self.positionX + 440,
                                           self.positionY + 60, 50, 50)
        self.percent_image = self.font.render(str(self.afterpercent) + "%", True, self.text_color,
                                           self.bg_color)
        self.percent_image_rect = pygame.Rect(self.positionX + 370,
                                           self.positionY + 60, 50, 50)

    def prep_msg_pressed(self): # 将选中标签渲染为图像
        self.id_image_pressed = self.font.render(self.str_id, True, self.text_color,
                                          self.pressed_color)
        self.id_image_rect_pressed = pygame.Rect(self.positionX + 20,
                                           self.positionY + 20, 70, 50)
        self.name_image_pressed = self.font.render(self.name, True, self.text_color,
                                          self.pressed_color)
        self.name_image_rect_pressed = pygame.Rect(self.positionX + 50,
                                           self.positionY + 20, 150, 50)
        self.lastopendate_image_pressed = self.font.render(self.lastopendate, True, self.text_color,
                                           self.pressed_color)
        self.lastopendate_image_rect_pressed = pygame.Rect(self.positionX + 300,
                                           self.positionY + 20, 150, 50)
        self.planinvest_image_pressed = self.font.render(self.planinvest, True, self.text_color,
                                           self.pressed_color)
        self.planinvest_image_rect_pressed = pygame.Rect(self.positionX + 440,
                                           self.positionY + 60, 50, 50)
        self.percent_image_pressed = self.font.render(str(self.afterpercent) + "%", True, self.text_color,
                                           self.pressed_color)
        self.percent_image_rect_pressed = pygame.Rect(self.positionX + 370,
                                           self.positionY + 60, 50, 50)

    def draw_textbasic(self):
        self.screen.fill(self.bg_color, self.rect)
        self.screen.blit(self.id_image, self.id_image_rect)
        self.screen.blit(self.name_image, self.name_image_rect)
        self.screen.blit(self.lastopendate_image, self.lastopendate_image_rect)
        self.screen.blit(self.planinvest_image, self.planinvest_image_rect)
        self.screen.blit(self.percent_image, self.percent_image_rect)
        pygame.draw.rect(self.screen, (0,0,0), ((self.positionX + 20, self.positionY + 60),(340, 20)), 2)
        if self.afterpercent != self.percent:
            pygame.draw.rect(self.screen, (0,0,0), ((self.positionX + 22 + 3.4*self.percent, self.positionY + 62),(1, 17)), 0)
        pygame.draw.rect(self.screen, (240,128,128), ((self.positionX + 22, self.positionY + 62),(3.4*self.percent, 17)), 0)

    def draw_pressed_textbasic(self):
        self.screen.fill(self.pressed_color, self.rect)
        self.screen.blit(self.id_image_pressed, self.id_image_rect_pressed)
        self.screen.blit(self.name_image_pressed, self.name_image_rect_pressed)
        self.screen.blit(self.lastopendate_image_pressed, self.lastopendate_image_rect_pressed)
        self.screen.blit(self.planinvest_image_pressed, self.planinvest_image_rect_pressed)
        self.screen.blit(self.percent_image_pressed, self.percent_image_rect_pressed)
        pygame.draw.rect(self.screen, (0,0,0), ((self.positionX + 20, self.positionY + 60),(340, 20)), 2)
        pygame.draw.rect(self.screen, (240,128,128), ((self.positionX + 22, self.positionY + 62),(3.4*self.percent, 17)), 0)

    def get_adventurebasic_text(self):
        return self.adventure

# 绘制抽卡块
class LotteryBasic(object):
    def __init__(self, screen, lottery_crytstal, must_num, up=""):
        self.screen = screen
        self.bg_color = (240,128,128)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont('KaiTi', 20)
        self.msg1 = "剩余水晶：" + str(lottery_crytstal)
        self.msg2 = "剩余水晶：" + str(lottery_crytstal - 280)
        self.must_msg = "距必出传说5星还有：" + str(must_num) + "次(每77抽保底)"
        self.up = up if up=="" else "本期up池传说角色：" + up
        self.up_bg_color = (255, 160, 122)  #up池文字橙色背景
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
                                     self.back_width+45, self.back_height+107)
        # 奖励参数
        self.reward_font = pygame.font.SysFont('KaiTi', 40)
        self.reward_color = (255, 255, 255)
        # 声音参数
        self.unopen_sound = pygame.mixer.Sound("sound//unopened_pack.ogg")
        self.card_sound = pygame.mixer.Sound("sound//rare.ogg")
        self.over_sound = pygame.mixer.Sound("sound//card_over_rare.ogg")
        # 文字、卡背标签
        self.prep_msg()

    def prep_msg(self):
        #剩余水晶
        self.__msg1_image = self.font.render(self.msg1, True, self.text_color,
                                          self.bg_color)
        self.__msg2_image = self.font.render(self.msg2, True, self.text_color,
                                          self.bg_color)
        self.__msg_image_rect = pygame.Rect(400, 40, 300, 50)
        #保底次数
        self.__must_msg_image = self.font.render(self.must_msg, True, self.text_color,
                                            self.bg_color)
        self.__must_msg_image_rect = pygame.Rect(10, 40, 250, 50)
        #本期up池
        self.__up_image =  self.font.render(self.up, True, self.text_color,
                                            self.up_bg_color)
        self.__rect_up = pygame.Rect(10, 65, 250, 50)

    def draw_lotteryback(self):     # 绘制卡背
        self.screen.blit(self.__msg1_image, self.__msg_image_rect)          #绘制剩余水晶
        self.screen.blit(self.__must_msg_image, self.__must_msg_image_rect) #绘制保底次数
        self.screen.blit(self.bg_image, self.back_rect)                 #绘制卡背位图
        if self.up != "":
            self.screen.blit(self.__up_image, self.__rect_up)           #绘制up池文字

    # 鼠标悬停离开点击效果
    def draw_mouseeffect(self, mouse, reward="", color=0, new=0):
        # Mouse 0 无效果. 1 悬停效果. 2 离开效果. 3 点击效果
        if mouse == 1:
            # 图像向外扩大
            # 绘制卡背位图
            self.screen.blit(self.bgbig_image, self.backbig_rect)
            # 播放音效
            self.unopen_sound.set_volume(0.01)
            self.unopen_sound.play()
            # 绘制剩余次数
            self.screen.blit(self.__msg1_image, self.__msg_image_rect)
            self.screen.blit(self.__must_msg_image, self.__must_msg_image_rect)
            #绘制up池文字
            if self.up != "":
                self.screen.blit(self.__up_image, self.__rect_up)           
        if mouse == 2:
            # 图像恢复原来大小
            # 绘制卡背位图
            self.screen.blit(self.bg_image, self.back_rect)
            # 停止音效
            self.unopen_sound.stop()
            # 绘制剩余次数
            self.screen.blit(self.__msg1_image, self.__msg_image_rect)
            self.screen.blit(self.__must_msg_image, self.__must_msg_image_rect)
            #绘制up池文字
            if self.up != "":
                self.screen.blit(self.__up_image, self.__rect_up)  
        if mouse == 3:
            # 停止播放音效
            self.unopen_sound.stop()
            # 判断奖励颜色和音效
            if color == 2 and new == 0:
                self.reward_color = (240,248,255)
                self.card_sound = False
                self.over_sound = pygame.mixer.Sound("sound//card_over_normal.ogg")
            elif color == 3 and new == 0:
                self.reward_color = (30,144,255)
            elif color == 4 and new == 0:
                self.reward_color = (153,50,204)
                self.card_sound = pygame.mixer.Sound("sound//epic.ogg")
                self.over_sound = pygame.mixer.Sound("sound//card_over_epic.ogg")
            elif color == 5 and new == 0:
                self.reward_color = (255,130,71)
                self.card_sound = pygame.mixer.Sound("sound//legend.ogg")
                self.over_sound = pygame.mixer.Sound("sound//card_over_legend.ogg")
            elif color == 2 and new == 1:
                self.reward_color = (240,248,255)
                self.card_sound = pygame.mixer.Sound("sound//new_C.ogg")
                self.over_sound = pygame.mixer.Sound("sound//card_over_normal.ogg")
            elif color == 3 and new == 1:
                self.reward_color = (30,144,255)
                self.card_sound = pygame.mixer.Sound("sound//new_R.ogg")
                self.over_sound = pygame.mixer.Sound("sound//card_over_rare.ogg")
            elif color == 4 and new == 1:
                self.reward_color = (153,50,204)
                self.card_sound = pygame.mixer.Sound("sound//new_E.ogg")
                self.over_sound = pygame.mixer.Sound("sound//card_over_epic.ogg")
            elif color == 5 and new == 1:
                self.reward_color = (255,130,71)
                self.card_sound = pygame.mixer.Sound("sound//new_L.ogg")
                self.over_sound = pygame.mixer.Sound("sound//card_over_legend.ogg")

            # 图像转化为奖励,利用big_image的颜色框，里面一个背景框框着奖励文字
            self.screen.fill(self.reward_color, self.backbig_rect)
            msg3 = self.reward_font.render(reward, True, self.reward_color, (205, 201,165))
            reward_len = formula_get_str_byte_len(reward)
            msg_mid_temp = self.back_width/2 + self.back_positionX - 150  - \
                            reward_len * 20     #奖励文字居中参数
            msg3_rect = pygame.Rect(self.back_positionX + msg_mid_temp,
                                    self.back_positionY + 150, 100, 50)
            # 显示奖励文字
            self.screen.blit(msg3, msg3_rect)
            # 显示卡牌和翻面声音
            if self.card_sound:
                self.card_sound.play()
            self.over_sound.play()
            # 绘制剩余水晶数量
            self.screen.blit(self.__msg2_image, self.__msg_image_rect)
            self.screen.blit(self.__must_msg_image, self.__must_msg_image_rect)
            #绘制up池文字
            if self.up != "":
                self.screen.blit(self.__up_image, self.__rect_up)  

# 倒计时类
class DecTime(object):
    def __init__(self, screen, totalTime, small_bg):
        self.screen = screen
        self.bg_color = (255, 236, 139)
        self.bg_image = pygame.image.load("image//small_bg//" + small_bg)
        self.font1 = pygame.font.SysFont('KaiTi', 60)
        self.font2 = pygame.font.SysFont('KaiTi', 70)
        self.font1_color = (255, 0, 128)    # 亮粉色
        self.font2_color = (181, 230, 29)   # 酸橙色
        # 将秒转化为时分秒
        self.sec = totalTime
        self.hour = int(self.sec / 3600)
        self.sec = self.sec % 3600
        self.minute = int(self.sec / 60)
        self.sec = int(self.sec % 60)
        # 绘制事件结束的文字
        self.font3 = pygame.font.SysFont('KaiTi', 36)
        self.font3_color = (0, 0, 0)
        self.stuff_color_ret = 2
        self.public_text = ""
        self.public_ch = ""
        self.public_stuff = ""
        self.love_add = ""
        
    def draw_timedec(self, text, ch):
        self.screen.fill(self.bg_color)
        self.screen.blit(self.bg_image, (0,0))
        self.screen.blit(self.font1.render(text, True, self.font1_color), (298-30*formula_get_str_byte_len(text), 200))  # 文字居中对齐
        self.screen.blit(self.font2.render(ch, True, self.font2_color), (180, 400))

    def draw_complete_text(self):
        self.screen.blit(self.bg_image, (0,0))
        self.screen.blit(self.font1.render(self.public_text, True, self.font3_color), (298-30*formula_get_str_byte_len(self.public_text), 240))  # 文字居中对齐
        self.screen.blit(self.font3.render(self.public_ch, True, self.font3_color), (298-18*formula_get_str_byte_len(self.public_ch), 400))
        if self.stuff_color_ret==2:
            stuff_color = (240,248,255)
        elif self.stuff_color_ret==3:
            stuff_color = (30,144,255)
        elif self.stuff_color_ret==4:
            stuff_color = (153,50,204)
        elif self.stuff_color_ret==5:
            stuff_color = (255,130,71)
        self.screen.blit(self.font3.render(self.public_stuff, True, stuff_color), (298-18*formula_get_str_byte_len(self.public_stuff), 460))
        self.screen.blit(self.font3.render(self.love_add, True, self.font3_color), (298-18*formula_get_str_byte_len(self.love_add), 520))

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

# 显示女武神列表
class GirlBasic(object):
    def __init__(self, width, height, screen, positionX, positionY, girl):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width, self.height = width, height
        self.bg_color_EX = (154, 255, 154)
        self.bg_color_SSS = (185, 211, 238)
        self.bg_color_SS = (238, 180, 180)
        self.bg_color_S = (255, 250, 205)
        self.bg_color_A = ( 238, 210, 238)
        if girl.grade=="A":
            self.bg_color = self.bg_color_A
        elif girl.grade=="S":
            self.bg_color = self.bg_color_S
        elif girl.grade=="SS":
            self.bg_color = self.bg_color_SS
        elif girl.grade=="SSS":
            self.bg_color = self.bg_color_SSS
        elif girl.grade=="EX":
            self.bg_color = self.bg_color_EX
        self.pressed_color = (180, 238, 180)
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont('KaiTi', 20)
        self.positionX = positionX
        self.positionY = positionY
        self.rect = pygame.Rect(positionX, positionY, self.width, self.height)
        self.girl = girl
        # 文字标签
        self.prep_msg()
        self.prep_rect()
    # 文字渲染为图像
    def prep_msg(self):
        #名称后带p表示按下按钮后显示
        self.__name_image = self.font.render(self.girl.name, True, self.text_color,
                                           self.bg_color)
        self.__namep_image = self.font.render(self.girl.name, True, self.text_color,
                                           self.pressed_color)
        self.__grade_image = self.font.render("星级:" + self.girl.grade, True, self.text_color, self.bg_color)
        self.__gradep_image = self.font.render("星级:" + self.girl.grade, True, self.text_color, self.pressed_color)
        self.__feature_image = self.font.render("特性:" + self.girl.feature, True, self.text_color, self.bg_color)
        self.__featurep_image = self.font.render("特性:" + self.girl.feature, True, self.text_color, self.pressed_color)
        self.__weapontype_image = self.font.render('武器类型:' + self.girl.weapon_type,
                                           True, self.text_color, self.bg_color)
        self.__idp_image = self.font.render('角色编号:' + str(self.girl.id),
                                           True, self.text_color, self.pressed_color)
        self.__sound_image = self.font.render('声优:' + self.girl.sound,
                                           True, self.text_color, self.bg_color)
        self.__rootp_image = self.font.render('作品:' + self.girl.root,
                                           True, self.text_color, self.pressed_color)
        passive_yxr = 0
        passive_moe = 0
        if self.girl.feature=="亲妹妹":
            passive_yxr = 100
        elif self.girl.feature=="天然呆":
            passive_moe = 80
        msg_moe = formula_four_dismension_add(self.girl.moe, self.girl.m_coefficient, self.girl.grade, self.girl.level, passive_moe)
        msg_yxr = formula_four_dismension_add(self.girl.yxr, self.girl.y_coefficient, self.girl.grade, self.girl.level, passive_yxr)
        msg_intimacy = formula_four_dismension_add(self.girl.intimacy, self.girl.i_coefficient, self.girl.grade, self.girl.level)
        msg_enthu = formula_four_dismension_add(self.girl.enthusiasm, self.girl.e_coefficient, self.girl.grade, self.girl.level)
        self.__moe_image = self.font.render('萌:' + str(msg_moe),
                                           True, self.text_color, self.bg_color)
        self.__moep_image = self.font.render('萌:' + str(self.girl.m_coefficient),
                                           True, self.text_color, self.pressed_color)
        self.__yxr_image = self.font.render('幼驯染:' + str(msg_yxr),
                                           True, self.text_color, self.bg_color)
        self.__yxrp_image = self.font.render('幼驯染:' + 
            str(self.girl.y_coefficient), True, self.text_color, self.pressed_color)
        self.__intimacy_image = self.font.render('熟悉:' + str(msg_intimacy),
                                           True, self.text_color, self.bg_color)
        self.__intimacyp_image = self.font.render('熟悉:' + 
            str(self.girl.i_coefficient), True, self.text_color, self.pressed_color)
        self.__enthusiasm_image = self.font.render('积极性:' + 
            str(msg_enthu),  True, self.text_color, self.bg_color)
        self.__enthusiasmp_image = self.font.render('积极性:' + 
            str(self.girl.e_coefficient), True, self.text_color, self.pressed_color)
        self.__moe_origin_image = self.font.render('萌:' + str(int(self.girl.moe)),
                                           True, self.text_color, self.bg_color)
        self.__yxr_origin_image = self.font.render('幼驯染:' + str(int(self.girl.yxr)),
                                           True, self.text_color, self.bg_color)
        self.__intimacy_origin_image = self.font.render('熟悉:' + str(int(self.girl.intimacy)),
                                           True, self.text_color, self.bg_color)
        self.__enthusiasm_origin_image = self.font.render('积极性:' + 
            str(int(self.girl.enthusiasm)),  True, self.text_color, self.bg_color)
        ret_temp = formula_grade_fragment_limit(self.girl.grade)
        if self.girl.feature=="自强者":
            ret_temp = int(ret_temp*0.95)
        fragment_max = "MAX" if ret_temp>300 else str(ret_temp)
        self.__fragment_image = self.font.render('碎片:' + str(self.girl.fragment) + 
            "/" + fragment_max, True, self.text_color, self.bg_color)
        self.__fragmentp_image = self.font.render('碎片:' + str(self.girl.fragment) + 
            "/" + fragment_max, True, self.text_color, self.pressed_color)
        love_max = formula_grade_love_limit(self.girl.grade)
        self.__love_image =  self.font.render('好感:' + str(round(self.girl.love, 2)) + 
            "/" + str(love_max), True, self.text_color, self.bg_color)
        self.__lovep_image =  self.font.render('好感:' + str(round(self.girl.love, 2)) + 
            "/" + str(love_max), True, self.text_color, self.pressed_color)
        self.__weapon_image = self.font.render('武器:' + str(self.girl.weapon_hold),
                                           True, self.text_color, self.bg_color)
        self.__weapontypep_image = self.font.render('武器类型:' + self.girl.weapon_type,
                                           True, self.text_color, self.pressed_color)
        self.__level_image = self.font.render('等级:' + str(self.girl.level),
                                           True, self.text_color, self.bg_color)
        self.__levelp_image = self.font.render('等级:' + str(self.girl.level),
                                           True, self.text_color, self.pressed_color)
    # 绘制矩形图像
    def prep_rect(self):
        #第一行
        self.__rect11l = pygame.Rect(self.positionX + 20, self.positionY + 20, 120, 50)
        self.__rect12s = pygame.Rect(self.positionX + 140, self.positionY + 20, 50, 50)
        self.__rect13s = pygame.Rect(self.positionX + 260, self.positionY + 20, 50, 50)
        self.__rect14s = pygame.Rect(self.positionX + 380, self.positionY + 20, 50, 50)
        #第二行
        self.__rect21l = pygame.Rect(self.positionX + 20, self.positionY + 60, 120, 50)
        self.__rect22l = pygame.Rect(self.positionX + 140, self.positionY + 60, 120, 50)
        self.__rect23l = pygame.Rect(self.positionX + 260, self.positionY + 60, 120, 50)
        #第三行
        self.__rect31s = pygame.Rect(self.positionX + 20, self.positionY + 100, 50, 50)
        self.__rect32s = pygame.Rect(self.positionX + 140, self.positionY + 100, 50, 50)
        self.__rect33s = pygame.Rect(self.positionX + 260, self.positionY + 100, 50, 50)
        self.__rect34s = pygame.Rect(self.positionX + 380, self.positionY + 100, 50, 50)
    # 绘制基础文字块
    def draw_girl_list_textbasic(self):
        self.screen.fill(self.bg_color, self.rect)
        self.screen.blit(self.__name_image, self.__rect11l)
        self.screen.blit(self.__grade_image, self.__rect12s)
        self.screen.blit(self.__feature_image, self.__rect13s)
        self.screen.blit(self.__weapontype_image, self.__rect21l)
        self.screen.blit(self.__sound_image, self.__rect23l)
        self.screen.blit(self.__moe_origin_image, self.__rect31s)
        self.screen.blit(self.__yxr_origin_image, self.__rect32s)
        self.screen.blit(self.__intimacy_origin_image, self.__rect33s)
        self.screen.blit(self.__enthusiasm_origin_image, self.__rect34s)
    # 绘制选中文字块
    def draw_girl_list_pressed_textbasic(self):
        self.screen.fill(self.pressed_color, self.rect)
        self.screen.blit(self.__namep_image, self.__rect11l)
        self.screen.blit(self.__gradep_image, self.__rect12s)
        self.screen.blit(self.__featurep_image, self.__rect13s)
        self.screen.blit(self.__idp_image, self.__rect21l)
        self.screen.blit(self.__rootp_image, self.__rect22l)
        self.screen.blit(self.__moep_image, self.__rect31s)
        self.screen.blit(self.__yxrp_image, self.__rect32s)
        self.screen.blit(self.__intimacyp_image, self.__rect33s)
        self.screen.blit(self.__enthusiasmp_image, self.__rect34s)
    #绘制拥有女武神
    def draw_my_girl_list_textbasic(self):
        self.screen.fill(self.bg_color, self.rect)
        self.screen.blit(self.__name_image, self.__rect11l)
        self.screen.blit(self.__grade_image, self.__rect12s)
        self.screen.blit(self.__fragment_image, self.__rect13s)
        self.screen.blit(self.__level_image, self.__rect14s)
        self.screen.blit(self.__love_image, self.__rect21l)
        self.screen.blit(self.__weapon_image, self.__rect23l)
        self.screen.blit(self.__moe_image, self.__rect31s)
        self.screen.blit(self.__yxr_image, self.__rect32s)
        self.screen.blit(self.__intimacy_image, self.__rect33s)
        self.screen.blit(self.__enthusiasm_image, self.__rect34s)
    def draw_my_girl_list_pressed_textbasic(self):
        self.screen.fill(self.pressed_color, self.rect)
        self.screen.blit(self.__namep_image, self.__rect11l)
        self.screen.blit(self.__gradep_image, self.__rect12s)
        self.screen.blit(self.__fragmentp_image, self.__rect13s)
        self.screen.blit(self.__levelp_image, self.__rect14s)
        self.screen.blit(self.__lovep_image, self.__rect21l)
        self.screen.blit(self.__weapontypep_image, self.__rect23l)
        self.screen.blit(self.__moep_image, self.__rect31s)
        self.screen.blit(self.__yxrp_image, self.__rect32s)
        self.screen.blit(self.__intimacyp_image, self.__rect33s)
        self.screen.blit(self.__enthusiasmp_image, self.__rect34s)

    # 用于获取女武神信息
    def get_girl_text(self):
        return self.girl

#绘制选中女武神类
class TheSelectFigureBasic(object):
    def __init__(self, screen, girl):
        self.screen = screen
        self.bg_color = (216, 191, 216)
        self.text_color = (205, 85, 85)
        self.name_color = (238, 121, 159)
        self.name_font = pygame.font.SysFont('KaiTi', 40, bold=True, italic=True)
        self.font_size = 25
        self.font = pygame.font.SysFont('KaiTi', self.font_size)
        self.font2_size = 35
        self.font2 = pygame.font.SysFont('KaiTi', self.font2_size)
        self.font3 = pygame.font.SysFont('KaiTi', 15)
        self.girl = girl
        self.love_level_msg = str(int(self.girl.love/50)) + "级"
        self.down_coordinate_y = 490
        self.down_interval = 40
        #多图片后缀
        self.charc_image = pygame.image.load("image//charc//黄前久美子_默认.png")
        img_suffix = ['.png', '.jpg', '.jpeg']
        for suf in img_suffix:
            path_name = "image//charc//" + self.girl.skin + suf
            if os.path.exists(path_name):
                self.charc_image = pygame.image.load(path_name)
        #升级品质
        self.white_color = (255, 255, 255)
        self.grey_color = (156, 156, 156)
        self.blue_color = (67, 110, 238)
        self.salmon_color = (233, 150, 122)
        #新等级和经验
        self.green_color = (0, 238, 118)
        #自强者 被动
        self.need_fragment = formula_grade_fragment_limit(self.girl.grade)
        if self.girl.feature=="自强者":
            self.need_fragment = int(self.need_fragment * 0.95)
        self.cgradeup_color = self.blue_color if self.girl.fragment>=self.need_fragment else self.grey_color
        self.assist_color = self.grey_color
        self.init_page()
        self.click_level_page()
        self.exp_book_page()
        self.exp_book_select_page()

    def init_page(self, isAssist=False):
        layout_px = 350
        layout_py = 110
        interval = 35
        self.rect_charc_image = pygame.Rect(40, 100, 300, 550)
        msg_temp = self.girl.skin
        self.__msg_skin = self.font.render(msg_temp, True, self.text_color,
                                          self.bg_color)
        self.rect_skin =  pygame.Rect(100, 570, 
            formula_get_str_byte_len(msg_temp)*self.font_size, 30)
        msg_temp = self.girl.name
        self.__msg_name = self.name_font.render(msg_temp, True, self.text_color,
                                          self.bg_color)
        self.__rect_name =  pygame.Rect(layout_px, 90, 
            formula_get_str_byte_len(msg_temp)*self.font_size, 30)
        msg_temp = "品质 / " + self.girl.grade + "  LV." + str(self.girl.level)
        self.__msg_level =  self.font.render(msg_temp, True, self.text_color, self.bg_color)
        self.rect_level = pygame.Rect(layout_px, layout_py+interval, 
            formula_get_str_byte_len(msg_temp)*self.font_size, 30)
        msg_temp = "好感 / " + self.love_level_msg
        self.__msg_love =  self.font.render(msg_temp, True, self.text_color, 
            self.bg_color)
        self.rect_love = pygame.Rect(layout_px, layout_py+interval*2, 
            formula_get_str_byte_len(msg_temp)*self.font_size, 30)
        msg_temp = "武器 / " + self.girl.weapon_hold
        self.__msg_weapon =  self.font.render(msg_temp, True, self.text_color, 
            self.bg_color)
        self.rect_weapon = pygame.Rect(layout_px, layout_py+interval*3, 
            formula_get_str_byte_len(msg_temp)*self.font_size, 30)
        msg_temp = "特性 / " + self.girl.feature
        self.__msg_feature =  self.font.render(msg_temp, True, self.text_color, 
            self.bg_color)
        self.rect_feature = pygame.Rect(layout_px, layout_py+interval*4, 
            formula_get_str_byte_len(msg_temp)*self.font_size, 30)
        passive_yxr = 0
        passive_moe = 0
        if self.girl.feature=="亲妹妹":
            passive_yxr = 100
        elif self.girl.feature=="天然呆":
            passive_moe = 80
        msg_moe = formula_four_dismension_add(self.girl.moe, self.girl.m_coefficient, self.girl.grade, self.girl.level, passive_moe)
        black_line = (4 - len(str(msg_moe))) * " "
        msg_temp = "萌 / " + black_line + str(msg_moe)
        self.__msg_moe =  self.font.render(msg_temp, True, self.text_color, 
            self.bg_color)
        self.rect_moe = pygame.Rect(layout_px, layout_py+interval*5, 
            formula_get_str_byte_len(msg_temp)*self.font_size, 30)

        msg_yxr = formula_four_dismension_add(self.girl.yxr, self.girl.y_coefficient, self.girl.grade, self.girl.level, passive_yxr)
        black_line = (4 - len(str(msg_yxr))) * " "
        msg_temp = "幼驯染 / " + black_line + str(msg_yxr)
        self.__msg_yxr =  self.font.render(msg_temp, True, self.text_color, 
            self.bg_color)
        self.rect_yxr = pygame.Rect(layout_px, layout_py+interval*6, 
            formula_get_str_byte_len(msg_temp)*self.font_size, 30)

        msg_intimacy = formula_four_dismension_add(self.girl.intimacy, self.girl.i_coefficient, self.girl.grade, self.girl.level)
        black_line = (4 - len(str(msg_intimacy))) * " "
        msg_temp = "熟悉 / " + black_line + str(msg_intimacy)
        self.__msg_intimacy =  self.font.render(msg_temp, True, self.text_color, 
            self.bg_color)
        self.rect_intimacy = pygame.Rect(layout_px, layout_py+interval*7, 
            formula_get_str_byte_len(msg_temp)*self.font_size, 30)

        msg_enthu = formula_four_dismension_add(self.girl.enthusiasm, self.girl.e_coefficient, self.girl.grade, self.girl.level)
        black_line = (4 - len(str(msg_enthu))) * " "
        msg_temp = "积极性 / " + black_line + str(msg_enthu)
        self.__msg_enthu =  self.font.render(msg_temp, True, self.text_color, 
            self.bg_color)
        self.rect_enthu = pygame.Rect(layout_px, layout_py+interval*8, 
            formula_get_str_byte_len(msg_temp)*self.font_size, 30)

        msg_temp = "选择作为助阵角色"
        self.assist_color = self.blue_color if isAssist==False else self.grey_color
        self.__msg_assist =  self.font.render(msg_temp, True, self.white_color, 
            self.assist_color)
        self.rect_assist = pygame.Rect(layout_px, layout_py+interval*9, 
            formula_get_str_byte_len(msg_temp)*self.font_size, 30)

    def click_level_page(self, modify=False, new_level=0, new_exp=0):
        if modify:
            black_line = " " if len(str(new_level)) else ""
            msg_temp = "等级:" + black_line + str(new_level) + "/80"
            self.__msg_clevel = self.font2.render(msg_temp, True, self.green_color, 
                self.salmon_color)
            self.rect_clevel = pygame.Rect(360, self.down_coordinate_y, formula_get_str_byte_len(msg_temp)*self.font2_size, 40)
            black_line = (5 - len(str(new_exp))) * " "
            temp = formula_level_exp_limit(new_level)
            black_line2 = (5 - len(str(temp))) * " "
            msg_temp = "经验:" + black_line + str(new_exp) + "/" + black_line2 + \
                str(temp)
            self.__msg_cexp = self.font.render(msg_temp, True, self.green_color, self.salmon_color)
            self.rect_cexp = pygame.Rect(360, self.down_coordinate_y+self.down_interval+7, formula_get_str_byte_len(msg_temp)*self.font_size, 40)
        else:
            msg_temp = "等级:" + str(self.girl.level) + "/80"
            self.__msg_clevel = self.font2.render(msg_temp, True, self.white_color, 
                self.salmon_color)
            self.rect_clevel = pygame.Rect(360, self.down_coordinate_y, formula_get_str_byte_len(msg_temp)*self.font2_size, 40)
            msg_temp = "经验:" + str(self.girl.exp) + "/" + \
                str(formula_level_exp_limit(self.girl.level))
            self.__msg_cexp = self.font.render(msg_temp, True, self.white_color, self.salmon_color)
            self.rect_cexp = pygame.Rect(360, self.down_coordinate_y+self.down_interval+7, formula_get_str_byte_len(msg_temp)*self.font_size, 40)
        ret_temp = formula_grade_fragment_limit(self.girl.grade)
        if self.girl.feature=="自强者":
            ret_temp = int(ret_temp*0.95)
        fragment_max = "MAX" if ret_temp>300 else str(ret_temp)
        msg_temp = "碎片:" + str(self.girl.fragment) + "/" + fragment_max
        self.__msg_cgrade = self.font2.render(msg_temp, True, self.white_color, self.salmon_color)
        self.rect_cgrade = pygame.Rect(360, self.down_coordinate_y+self.down_interval*2, formula_get_str_byte_len(msg_temp)*self.font2_size, 40)
        msg_temp = "升阶"
        self.__msg_cgradeup = self.font2.render(msg_temp, True, self.white_color, self.cgradeup_color)
        self.rect_cgradeup = pygame.Rect(410, self.down_coordinate_y+self.down_interval*3, formula_get_str_byte_len(msg_temp)*self.font2_size, 40) 

    def click_love_page(self):
        msg_temp = "好感度:" + str(round(self.girl.love, 2)) + "/" + str(formula_grade_love_limit(self.girl.grade))
        self.__msg_clove = self.font2.render(msg_temp, True, self.white_color, 
            self.salmon_color)
        self.rect_clove = pygame.Rect(300, self.down_coordinate_y+self.down_interval, formula_get_str_byte_len(msg_temp)*self.font2_size, 40)

    def click_feature_page(self):
        msg_list = formula_str_to_interval_list("特性说明:" + self.girl.feature_info, 13)
        self.__msg_cfeature_list = []
        self.rect_cfeature_list = []
        height_delta = 25
        for msg_temp, height_temp in zip(msg_list, range(0,len(msg_list))):
            self.__msg_cfeature_list.append(self.font.render(msg_temp, True, self.white_color,self.salmon_color))
            self.rect_cfeature_list.append(pygame.Rect(280, self.down_coordinate_y+self.down_interval+height_temp*height_delta, formula_get_str_byte_len(msg_temp)*self.font_size, 40))

    def exp_book_page(self, quantity_4=0, quantity_3=0, quantity_2=0):
        self.__img_4exp = pygame.image.load("image//good//4星角色书.png")
        self.__img_3exp = pygame.image.load("image//good//3星角色书.png")
        self.__img_2exp = pygame.image.load("image//good//2星角色书.png")
        position_y = 660
        self.rect_4exp = pygame.Rect(260, position_y ,80, 80)
        self.rect_3exp = pygame.Rect(350, position_y ,80, 80)
        self.rect_2exp = pygame.Rect(440, position_y ,80, 80)
        self.__msg_4exp =  self.font3.render("×" + str(quantity_4), True, self.text_color, self.salmon_color)
        self.__msg_3exp =  self.font3.render("×" + str(quantity_3), True, self.text_color, self.salmon_color)
        self.__msg_2exp =  self.font3.render("×" + str(quantity_2), True, self.text_color, self.salmon_color)
        self.__rect_msg_4exp = pygame.Rect(280, position_y+80,50, 25)
        self.__rect_msg_3exp = pygame.Rect(370, position_y+80,50, 25)
        self.__rect_msg_2exp = pygame.Rect(460, position_y+80,50, 25)
        
    def exp_book_select_page(self, quantity_4=0, quantity_3=0, quantity_2=0):
        #点击角色书后增加
        self.__msg_4exp_add =  self.font3.render("×" + formula_format_add0(str(quantity_4),3), True, self.text_color, self.white_color)
        self.__msg_3exp_add =  self.font3.render("×" + formula_format_add0(str(quantity_3),3), True, self.text_color, self.white_color)
        self.__msg_2exp_add =  self.font3.render("×" + formula_format_add0(str(quantity_2),3), True, self.text_color, self.white_color)
        position_y = 660
        interval = 60
        self.__rect_msg_4exp_add = pygame.Rect(280, position_y+interval,50, 25)
        self.__rect_msg_3exp_add = pygame.Rect(370, position_y+interval,50, 25)
        self.__rect_msg_2exp_add = pygame.Rect(460, position_y+interval,50, 25)
        if quantity_4+quantity_3+quantity_2 > 0:
            self.__msg_levelUp = self.font2.render("升级", True, self.white_color, self.blue_color)
        else:
            self.__msg_levelUp = self.font2.render("升级", True, self.white_color, self.grey_color)
        self.rect_levelUp = pygame.Rect(525, position_y+20, 50, 25)

    def draw_theselectgirlbasic(self, assist):     # 绘制初始页面
        self.init_page(assist==self.girl.name)
        self.screen.blit(self.charc_image, self.rect_charc_image)
        self.screen.blit(self.__msg_skin, self.rect_skin)
        self.screen.blit(self.__msg_name, self.__rect_name)          
        self.screen.blit(self.__msg_level, self.rect_level)
        self.screen.blit(self.__msg_love, self.rect_love)
        self.screen.blit(self.__msg_weapon, self.rect_weapon)
        self.screen.blit(self.__msg_feature, self.rect_feature)
        self.screen.blit(self.__msg_moe, self.rect_moe)
        self.screen.blit(self.__msg_yxr, self.rect_yxr)
        self.screen.blit(self.__msg_intimacy, self.rect_intimacy)
        self.screen.blit(self.__msg_enthu, self.rect_enthu)
        self.screen.blit(self.__msg_assist, self.rect_assist)

    def draw_theselectgirlbasic_only_read(self):     # 绘制详情页面
        self.init_page()
        self.screen.blit(self.charc_image, self.rect_charc_image)
        self.screen.blit(self.__msg_skin, self.rect_skin)
        self.screen.blit(self.__msg_name, self.__rect_name)          
        self.screen.blit(self.__msg_level, self.rect_level)
        self.screen.blit(self.__msg_love, self.rect_love)
        self.screen.blit(self.__msg_feature, self.rect_feature)
        self.screen.blit(self.__msg_moe, self.rect_moe)
        self.screen.blit(self.__msg_yxr, self.rect_yxr)
        self.screen.blit(self.__msg_intimacy, self.rect_intimacy)
        self.screen.blit(self.__msg_enthu, self.rect_enthu)

    def draw_click_rect_level(self):
        self.screen.blit(self.__msg_clevel, self.rect_clevel)
        self.screen.blit(self.__msg_cexp, self.rect_cexp)
        self.screen.blit(self.__msg_cgrade, self.rect_cgrade)
        self.screen.blit(self.__msg_cgradeup, self.rect_cgradeup)
    
    def draw_click_rect_love(self):
        self.click_love_page()
        self.screen.blit(self.__msg_clove, self.rect_clove)

    def draw_click_rect_feature(self):
        self.click_feature_page()
        for msg, rect in zip(self.__msg_cfeature_list, self.rect_cfeature_list):
            self.screen.blit(msg, rect)

    def draw_click_rect_clevel(self, quantity_4, quantity_3, quantity_2):
        self.exp_book_page(quantity_4, quantity_3, quantity_2)
        self.screen.blit(self.__img_4exp, self.rect_4exp)
        self.screen.blit(self.__img_3exp, self.rect_3exp)
        self.screen.blit(self.__img_2exp, self.rect_2exp)
        self.screen.blit(self.__msg_4exp, self.__rect_msg_4exp)
        self.screen.blit(self.__msg_3exp, self.__rect_msg_3exp)
        self.screen.blit(self.__msg_2exp, self.__rect_msg_2exp)
        
        
    def draw_click_books(self, quantity_4=0, quantity_3=0, quantity_2=0):
        new_level, new_exp = formula_levelUp_with_expbook(self.girl.level, self.girl.exp,quantity_4, quantity_3, quantity_2)
        self.click_level_page(modify=True, new_level=new_level, new_exp=new_exp)
        self.draw_click_rect_level()
        self.exp_book_select_page(quantity_4, quantity_3, quantity_2)
        self.screen.blit(self.__msg_4exp_add, self.__rect_msg_4exp_add)
        self.screen.blit(self.__msg_3exp_add, self.__rect_msg_3exp_add)
        self.screen.blit(self.__msg_2exp_add, self.__rect_msg_2exp_add)
        self.screen.blit(self.__msg_levelUp, self.rect_levelUp)

class KnapsackBasic(object):
    '''背包类
    '''
    def __init__(self, screen, weapon_list, material_list):
        self.screen = screen
        self.bg_color = (216, 191, 216)
        self.text_color = (205, 85, 85)
        self.white_color = (255, 255, 255)
        self.name_color = (238, 121, 159)

        self.font = pygame.font.SysFont('KaiTi', 17)
        self.font2 = pygame.font.SysFont('KaiTi', 15, bold=True, italic=True)
        self.font3 = pygame.font.SysFont('KaiTi', 20)
        self.littlefont_size = 20
        self.littlefont = pygame.font.SysFont('KaiTi', self.littlefont_size)
        self.wlen = len(weapon_list)
        self.mlen = len(material_list)
        #建立武器图片列表
        self.weapon_list = weapon_list
        self.material_list = material_list
        self.left_pack_init()
        
    def left_pack_init(self):
        self.image_list = []
        self.rect_image_list = []
        self.littlefont_list = []
        self.rect_littlefont_list = []
        self.levelornum_list = []
        self.rect_levelornum_list = []
        self.name_list = []
        self.rect_name_list = []
        self.delta_x, self.delta_y = 50, 170
        self.width_x, self.height_y = 130, 110
        stuff_num = self.wlen + self.mlen
        pos_x, pos_y = 1, 1
        weapon_num, material_num = 0, 0
        for i in range(stuff_num):
            if pos_x==6:
                pos_x = 1
                pos_y += 1
            if weapon_num < self.wlen:
                suffix = "_默认.png"
                if self.weapon_list[weapon_num].awaken==4:
                    suffix = "_突破.png"
                self.image_list.append(pygame.image.load("image//good//" + self.weapon_list[weapon_num].name + suffix))
                self.rect_image_list.append(pygame.Rect(self.width_x*pos_x+self.delta_x, self.height_y*pos_y+self.delta_y, 80, 80))
                self.littlefont_list.append(self.littlefont.render(str(self.weapon_list[weapon_num].awaken), True, self.text_color, self.white_color))
                self.rect_littlefont_list.append(pygame.Rect(self.width_x*pos_x+self.delta_x, self.height_y*pos_y+self.delta_y, 5, 5))
                self.levelornum_list.append(self.font2.render("lv." + str(self.weapon_list[weapon_num].level), True, self.text_color, self.white_color))
                self.rect_levelornum_list.append(pygame.Rect(self.width_x*pos_x+self.delta_x, self.height_y*pos_y+self.delta_y + 65, 10, 10))
                self.name_list.append(self.font.render(self.weapon_list[weapon_num].name, True, self.text_color, self.white_color))
                self.rect_name_list.append(pygame.Rect(self.width_x*pos_x+self.delta_x+5, self.height_y*pos_y+self.delta_y+85, 20, 20))
                weapon_num += 1
            else:
                self.image_list.append(pygame.image.load("image//good//" + self.material_list[material_num].name + ".png"))
                self.rect_image_list.append(pygame.Rect(self.width_x*pos_x+self.delta_x, self.height_y*pos_y+self.delta_y, 80, 80))
                self.levelornum_list.append(self.font2.render("×" + str(self.material_list[material_num].number), True, self.text_color, self.white_color))
                self.rect_levelornum_list.append(pygame.Rect(self.width_x*pos_x+self.delta_x, self.height_y*pos_y+self.delta_y + 65, 10, 10))
                self.name_list.append(self.font.render(self.material_list[material_num].name, True, self.text_color, self.white_color))
                self.rect_name_list.append(pygame.Rect(self.width_x*pos_x+self.delta_x+5, self.height_y*pos_y+self.delta_y+85, 20, 20))
                material_num += 1
            pos_x += 1

    def weapon_detail(self, weapon):
        suffix = "_默认.png"
        if weapon.awaken==4:
            suffix = "_突破.png"
        self.__image_weapon = pygame.image.load("image//weapon//" + weapon.name + suffix)
        self.__name_weapon = self.font3.render(weapon.name, True, self.text_color, self.white_color)
        self.__level_weapon = self.font3.render("Lv." + str(weapon.level), True, self.text_color, self.white_color)
        self.__moe_weapon = self.font3.render("moe值: " + str(weapon.moe), True, self.text_color, self.white_color)
        self.__awaken_weapon = self.font3.render("突破等阶: " + str(weapon.awaken), True, self.text_color, self.white_color)
        if weapon.equip_figure_name:
            self.__equip_figure_name_weapon = self.font3.render("装备角色: " + weapon.equip_figure_name, True, self.text_color, self.white_color)
        else:
            self.__equip_figure_name_weapon = self.font3.render("装备角色: 无", True, self.text_color, self.white_color)
        self.__typed_weapon = self.font3.render("武器类型: " + weapon.typed, True, self.text_color, self.white_color)
        
        interval_y = 25
        pos_x = 850
        self.__rect_image_weapon = pygame.Rect(pos_x, 280, 180, 180)
        self.__rect_name_weapon = pygame.Rect(pos_x, 470, 40, 20)
        self.__rect_level_weapon = pygame.Rect(pos_x, 470 + interval_y, 40, 20)
        self.__rect_moe_weapon = pygame.Rect(pos_x, 470 + interval_y * 2, 40, 20)
        self.__rect_awaken_weapon = pygame.Rect(pos_x, 470 + interval_y * 3, 40, 20)
        self.__rect_equip_figure_name_weapon = pygame.Rect(pos_x, 470 + interval_y * 4, 40, 20)
        self.__rect_typed_weapon = pygame.Rect(pos_x, 470 + interval_y * 5, 40, 20)
        if weapon.feature:
            self.__feature_weapon = self.font3.render("武器特性: " + weapon.feature, True, self.text_color, self.white_color)
            self.__rect_feature_weapon = pygame.Rect(pos_x, 470 + interval_y * 6, 40, 20)
            #特性说明居中显示
            #self.__feature_info_weapon = self.font3.render("特性说明: " + weapon.feature_info, True, self.text_color, self.white_color)
            #self.__rect_feature_info_weapon = pygame.Rect(720, 470 + interval_y * 7, 40, 40)
            msg_list = formula_str_to_interval_list("特性说明:" + weapon.feature_info.replace("$1$", str(formula_weapon_awaken_value(weapon))), 13)
            self.__feature_info_weapon = []
            self.__rect_feature_info_weapon = []
            for msg_temp, height_temp in zip(msg_list, range(0,len(msg_list))):
                self.__feature_info_weapon.append(self.font3.render(msg_temp, True, self.text_color,self.white_color))
                self.__rect_feature_info_weapon.append(pygame.Rect(pos_x, 470+(height_temp+7)*interval_y, formula_get_str_byte_len(msg_temp)*20, 40))

    def draw_origin_pack(self):
        for i in range(len(self.image_list)):
            self.screen.blit(self.image_list[i], self.rect_image_list[i])
            self.screen.blit(self.levelornum_list[i], self.rect_levelornum_list[i])
            self.screen.blit(self.name_list[i], self.rect_name_list[i])
            if(i<self.wlen):
                self.screen.blit(self.littlefont_list[i], self.rect_littlefont_list[i])

    def draw_special_pack(self, rect):
        select_num = int((rect.left - self.delta_x)/self.width_x - 1 + ((rect.top - self.delta_y)/self.height_y - 1)*5)
        if select_num < self.wlen:
            self.weapon_detail(self.weapon_list[select_num])
            self.screen.blit(self.__image_weapon, self.__rect_image_weapon)
            self.screen.blit(self.__name_weapon, self.__rect_name_weapon)
            self.screen.blit(self.__level_weapon, self.__rect_level_weapon)
            self.screen.blit(self.__moe_weapon, self.__rect_moe_weapon)
            self.screen.blit(self.__awaken_weapon, self.__rect_awaken_weapon)
            self.screen.blit(self.__equip_figure_name_weapon, self.__rect_equip_figure_name_weapon)
            self.screen.blit(self.__typed_weapon, self.__rect_typed_weapon)
            if self.weapon_list[select_num].feature:
                self.screen.blit(self.__feature_weapon, self.__rect_feature_weapon)
                for i,j in zip(self.__feature_info_weapon, self.__rect_feature_info_weapon):
                    self.screen.blit(i, j)
        else:
            print(self.material_list[select_num-self.wlen].name)