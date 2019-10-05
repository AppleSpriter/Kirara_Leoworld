import pygame
import sys
import  json
from kirara_figure import *

mouse_rollup = 0
text_len = 30

# 监视鼠标和键盘事件
def check_events(button_list):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # 按下button事件
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # if mouse_x > 100 and mouse_x < 500 and mouse_y > 50 and mouse_y < 150:
            tmp = 0
            for button in button_list:
                tmp += 1
                if button.rect.collidepoint(mouse_x, mouse_y) and tmp == 1:
                    click_button_girls()
                elif button.rect.collidepoint(mouse_x, mouse_y) and tmp == 2:
                    click_button_mission()
                elif button.rect.collidepoint(mouse_x, mouse_y) and tmp == 3:
                    click_button_lottery()
                elif button.rect.collidepoint(mouse_x, mouse_y) and tmp == 4:
                    click_button_achievement()


# 按下girls按钮事件
def click_button_girls():
    # 列出女孩子的列表
    girls = []
    read_girls(girls)

# 女孩子打印
def read_girls(girls):
    with open("GIRLS.txt") as file_object:
        read_list = json.load(file_object)

    girls_list = []
    for content in read_list:
        girls_list.append(Figure(content['name'], content['root'],
                                 content['grade'], content['level'],
                                 content['weapon'], content['sound'],
                                 content['skilllevel'], content['love'],
                                 content['eyecolor'], content['haircolor']))

    screen_works = pygame.display.set_mode((600,800))
    button_back = Button(150, 100, screen_works, "返回", 50, 650)
    button_list = [button_back]
    work_setting = Settings()
    # 进入girls查看页面
    while True:
        # 返回主菜单,检测鼠标滑轮
        click_to_index(button_back)
        # 屏幕更新
        update_screen(screen_works, work_setting, button_list, girls_list,
                      'girl')

# 按下mission按钮事件
def click_button_mission():
    print("mission button")

# 按下lottery按钮事件
def click_button_lottery():
    print("lottery button")

# 按下achievement按钮事件
def click_button_achievement():
    print("achievement button")

# 更新屏幕函数
def update_screen(screen, setting=Settings(), button_list=[], text_list=[],
                  type=''):
    # 全局变量声明
    global text_len
    global mouse_rollup
    # 绘制背景色
    screen.fill(setting.bg_color)
    # 绘制button1
    for button in button_list:
        button.draw_button()

    if type == 'work':
        # 绘制文字
        if text_list:
            positionX = 30
            positionY = 0
            width = 500
            height = 100
            for text in text_list:
                tb = TextBasic(width, height, screen, positionX,
                               positionY - mouse_rollup, text['name'],
                               text['year'], text['company'])
                tb.draw_textbasic()
                positionY += 110

    if type == 'girl':
        # 绘制女孩
        if text_list:
            positionX = 30
            positionY = 0
            width = 500
            height = 100
            for girl in text_list:
                tb = GirlBasic(width, height, screen, positionX,
                               positionY - mouse_rollup, girl)
                tb.draw_textbasic()
                positionY += 110

    text_len = len(text_list) * 130

    # 显示窗口
    pygame.display.flip()

# 返回主页面函数
def click_to_index(button):
    # 全局变量声明
    global text_len
    global mouse_rollup

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # 按下button事件
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if button.rect.collidepoint(mouse_x, mouse_y):
                mouse_rollup = 0
                run_game()
            if event.button == 5 and mouse_rollup < (text_len - 800):
                mouse_rollup += 40
            elif event.button == 4 and mouse_rollup >=0:
                mouse_rollup -= 40

# 返回girls页面函数
def click_to_girls(button):
    # 全局变量声明
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # 按下button事件
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if button.rect.collidepoint(mouse_x, mouse_y):
                click_button_girls()

# 读取作品列表
def read_works(works):
    with open("WORKS.txt") as file_object:
        work_list = json.load(file_object)

    screen_works = pygame.display.set_mode((600,800))
    button_back = Button(150, 100, screen_works, "返回", 50, 650)
    button_list = [button_back]
    work_setting = Settings()
    # 进入作品查看页面
    while True:
        # 返回主菜单,检测鼠标滑轮
        click_to_index(button_back)
        # 屏幕更新
        update_screen(screen_works, work_setting, button_list, work_list,
                      "work")


# 游戏运行主函
def run_game():
    # initialise the game
    pygame.init()
    # 加载设置
    ki_setting = Settings()
    # 设置窗口长宽
    screen = pygame.display.set_mode((ki_setting.screen_width, ki_setting.screen_height))
    # 设置窗口名称
    pygame.display.set_caption("Kirara Leoworld")
    # 创建首页四个button列表
    button_girls = Button(400, 100, screen, "girls", 100, 50)
    button_mission = Button(400, 100, screen, "任务", 700, 50)
    button_lottery = Button(400, 100, screen, "抽卡", 100, 250)
    button_achievement = Button(400, 100, screen, "成就", 700, 250)
    button_list = [button_girls, button_mission, button_lottery, button_achievement]

    # 开始游戏
    while True:
        check_events(button_list)
        update_screen(screen, ki_setting, button_list)

