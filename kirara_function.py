import pygame
import json
import random
import MySQLdb
import os
from win10toast import ToastNotifier
from kirara_figure import *
import logging

"""
CRITICAL    50
ERROR       40
WARNING     30
INFO        20
DEBUG       10
NOTSET       0
"""
logging.basicConfig(level=logging.DEBUG)  # 调试选项,设置日志级别
# 设置frames per second
FPS = 30
highFPS = 80
fpsClock = pygame.time.Clock()
KiraraL_icon_path = "icon/Adobe_Indesign.ico"

mouse_rollup = 0        # 鼠标滑轮转动
mouse_roll_dis = 80     # 鼠标单次滑动敏感度
text_len = 30           # 单个字符长度
lottery_mouse_x = 0     # 鼠标x坐标
lottery_mouse_y = 0     # 鼠标y坐标
big_bg = 1              # 全局背景图编号,从1开始
toaster = ToastNotifier() # 全局toaster，方便destroy
toaster_destroy = True  # toaster已经被destroy
pressed_button = ""     # 按下的button

# mysqlclient连接数据库
db = MySQLdb.connect("localhost", "root", "sdffdaa1", "kirara_leoworld",
                     charset='utf8')
cursor = db.cursor()

# 监视鼠标和键盘事件
def check_events(screen, button_list, text_list):
    global big_bg, toaster, toaster_destroy, pressed_button
    while True:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                sys.exit()
            # 按下鼠标左键，button显示按下状态
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                #选择哪个按钮被按下
                #画出按下的按钮
                for button in button_list:
                    if button.rect.collidepoint(mouse_x, mouse_y):
                        pressed_button = button
                        update_screen(screen, button_list=button_list, home_page_text=text_list)

            # 松开鼠标左键，button显示原本状态
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                #将按下按钮回归
                pressed_button = ""
                update_screen(screen, button_list=button_list, home_page_text=text_list)

                mouse_x, mouse_y = pygame.mouse.get_pos()
                tmp = 0
                # 销毁toaster内存占用
                if not toaster_destroy:
                    toaster.custom_destroy()
                    toaster_destroy = True
                # 查看鼠标点击在哪个范围内，使用tmp确定是第几个按钮
                # 由于button是在list中不确定，没有tmp就会只进入第一个read_girls()函数
                for button in button_list:
                    tmp += 1
                    if button.rect.collidepoint(mouse_x, mouse_y) and tmp == 1:
                        read_girls()
                    elif button.rect.collidepoint(mouse_x, mouse_y) and tmp == 2:
                        read_works()
                    elif button.rect.collidepoint(mouse_x, mouse_y) and tmp == 3:
                        click_button_lottery()
                    elif button.rect.collidepoint(mouse_x, mouse_y) and tmp == 4:
                        read_achievements()         # 先选择事件再进入专注选择
                    elif button.rect.collidepoint(mouse_x, mouse_y) and tmp == 5:
                        click_button_checkin()
                    elif button.rect.collidepoint(mouse_x, mouse_y) and tmp == 6:
                        click_button_log("kirara")
                    elif button.rect.collidepoint(mouse_x, mouse_y) and tmp == 7:
                        click_button_log("lottery")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:         # 主页面背景图向左切换
                    big_bg -= 1
                elif event.key  == pygame.K_l:      # 主页面背景图向右切换
                    big_bg += 1
                elif event.key == pygame.K_r:       # reset主页面背景图
                    big_bg = 1
                elif event.key == pygame.K_ESCAPE:
                    sys.exit()
                update_screen(screen, button_list=button_list, home_page_text=text_list)


        # 降低cpu占用率，减少主页面刷新频率，delay一秒从30%降到0.5%
        fpsClock.tick(FPS)

# 更新查询figure列中某一项
def sql_update_one(girl):
    query_sql = "Select * from figure where name=%s"
    cursor.execute(query_sql,[girl.name])
    tuple_tmp = cursor.fetchall()
    for girls in tuple_tmp:
        this_girl = Figure(girls[1], girls[2], girls[3], girls[4],
                                 girls[5], girls[6], girls[7], girls[8],
                                 girls[9], girls[10])
    return this_girl

# 女孩子查询
def read_girls():
    query_sql = "Select * from figure"
    cursor.execute(query_sql)
    tuple_tmp = cursor.fetchall()
    girls_list = []
    for girls in tuple_tmp:
        girls_list.append(Figure(girls[1], girls[2], girls[3], girls[4],
                                 girls[5], girls[6], girls[7], girls[8],
                                 girls[9], girls[10]))
    girl_setting = Settingssmallwindow()
    screen_works = pygame.display.set_mode((girl_setting.screen_width, girl_setting.screen_height))
    button_back = Button(150, 100, screen_works, "返回", 50, 650)
    button_list = [button_back]
    work_setting = Settings()
    # 进入girls查看页面
    while True:
        # 返回主菜单,检测鼠标滑轮
        click_lottery_and_index(button_back)
        # 屏幕更新
        update_screen(screen_works, work_setting, button_list, girls_list,
                      'girl')
        
# 读取作品列表
def read_works():
    # with open("WORKS.txt") as file_object:
    #     work_list = json.load(file_object)
    query_sql = "Select * from work"
    cursor.execute(query_sql)

    tuple_tmp = cursor.fetchall()
    work_list = []
    for works in tuple_tmp:
        work_list.append({'name': works[1], 'year': str(works[2]),
                          'company': works[3]})
    work_setting = Settingssmallwindow()
    screen_works = pygame.display.set_mode((work_setting.screen_width, work_setting.screen_height))
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

def read_achievements():   # 读取成就
    query_sql = "Select * from achievement"
    cursor.execute(query_sql)
    tuple_tmp = cursor.fetchall()

    achi_list = []
    for achievements in tuple_tmp:
        if achievements[5] < achievements[4] and achievements[3] == None:       # 仅显示未完成事件
            timestamp = time.mktime(time.strptime(str(achievements[6]), "%Y-%m-%d %H:%M:%S"))
            achi_list.append({'name': achievements[1], 'startdate': achievements[2],
                              'enddate': achievements[3], 'planinvest': achievements[4],
                              'nowinvest': achievements[5], 'achievementid': achievements[0],
                              'lastopendate': achievements[6],'lastopentimestamp': timestamp})

    achi_list = sorted(achi_list, key=lambda key:float(key['lastopentimestamp']),reverse=True)  # 按照id排序
    achieve_setting = Settingssmallwindow()
    screen_works = pygame.display.set_mode((achieve_setting.screen_width, achieve_setting.screen_height))
    button_back = Button(150, 100, screen_works, "返回", 50, 650)
    button_list = [button_back]
    work_setting = Settings()
    # 进入作品查看页面
    while True:
        # 返回主菜单,检测鼠标滑轮
        click_lottery_and_index(button_back)
        # 屏幕更新
        update_screen(screen_works, work_setting, button_list, achi_list,
                      "achievements_previous")

# 按下lottery按钮事件
def click_button_lottery():
    # 查询数据库
    query_sql = "Select lottery_crystal from lottery"
    cursor.execute(query_sql)
    # 取出抽奖次数
    tuple_tmp = cursor.fetchall()
    lottery_crystal = []
    lottery_crystal.append(tuple_tmp[0][0])
    lottery_setting = Settingssmallwindow()
    screen_lottery = pygame.display.set_mode((lottery_setting.screen_width, lottery_setting.screen_height))
    button_back = Button(150, 100, screen_lottery, "返回", 50, 650)
    button_list = [button_back]
    work_setting = Settings()
    # 抽奖页面
    while True:
        # 屏幕更新
        update_screen(screen_lottery, work_setting, button_list, lottery_crystal,
                      "lottery")
        # 降低cpu占用率，减少主页面刷新频率，delay一秒从30%降到0.5%
        fpsClock.tick(highFPS)

# 按下achievement按钮事件
def click_button_achievement(achi):
    achieve_setting = Settingssmallwindow()
    screen_achievement = pygame.display.set_mode((achieve_setting.screen_width, achieve_setting.screen_height))
    button_paper = Button(500, 80, screen_achievement, "看论文做实验", 50, 240)
    button_learn = Button(500, 80, screen_achievement, "读书整理书爱培", 50, 340)
    button_language = Button(500, 80, screen_achievement, "半个番茄钟", 50, 440)
    button_play = Button(500, 80, screen_achievement, "休息", 50, 540)
    button_back = Button(150, 100, screen_achievement, "返回", 50, 650)
    button_list = [button_back, button_paper, button_learn, button_language, button_play]
    work_setting = Settings()
    # 抽奖页面
    while True:
        # 屏幕更新
        update_screen(screen_achievement, work_setting, button_list, [achi],
                      "achievement")
        
# 可签到判断函数
def checkin_check():
    # 设置三个签到时间段,6:30-8:10   13:00-13:30    22:30-23:00
    morning_t1 = datetime.time(6, 30, 0, 0)
    morning_t2 = datetime.time(8, 11, 0, 0)
    noon_t1 = datetime.time(13, 0, 0, 0)
    noon_t2 = datetime.time(13, 31, 0, 0)
    night_t1 = datetime.time(22, 30, 0, 0)
    night_t2 = datetime.time(23, 1, 0, 0)

    nowtime = datetime.datetime.now()
    # 查询上次签到时间
    select_checkdate_sql = "Select check_date from lottery"
    cursor.execute(select_checkdate_sql)
    tuple_tmp = cursor.fetchall()
    last_checkin_time = tuple_tmp[0][0]
    # 早间签到
    if nowtime.time().__ge__(morning_t1) and nowtime.time().__le__(morning_t2):
        # 判断是否重复签到
        if last_checkin_time.date().__eq__(nowtime.date()) and \
            last_checkin_time.time().__ge__(morning_t1) and \
            last_checkin_time.time().__le__(morning_t2):
            return last_checkin_time
        else:
            return 2    # 早间可签到
    # 午间签到
    elif nowtime.time().__ge__(noon_t1) and nowtime.time().__le__(noon_t2):
        # 判断是否重复签到
        if last_checkin_time.date().__eq__(nowtime.date()) and \
            last_checkin_time.time().__ge__(noon_t1) and \
            last_checkin_time.time().__le__(noon_t2):
            return last_checkin_time
        else:
            return 3    # 午间可签到
    # 夜间签到
    elif nowtime.time().__ge__(night_t1) and nowtime.time().__le__(night_t2):
        # 判断是否重复签到
        if last_checkin_time.date().__eq__(nowtime.date()) and \
            last_checkin_time.time().__ge__(night_t1) and \
            last_checkin_time.time().__le__(night_t2):
            return last_checkin_time
        else:
            return 4    # 夜间可签到
    else:
        return 5    # 不在签到时间段

# 按下checkin按钮事件
def click_button_checkin():
    nowtime = datetime.datetime.now()
    nowtime_str = nowtime.strftime('%Y-%m-%d %H:%M:%S')

    select_lottery_sql = "Select lottery_crystal from lottery"
    update_checkdate_sql = "update lottery set check_date=%s"
    update_check_lottery_sql = "update lottery set lottery_crystal=lottery_crystal+80"
    cursor.execute(select_lottery_sql)
    tuple_tmp = cursor.fetchall()
    lottery_crystal = tuple_tmp[0][0]
    # 签到增加水晶
    lottery_crystal += 80
    last_checkin_time=checkin_check()
    # 气泡通知
    global toaster,toaster_destroy
    # 早间签到
    if last_checkin_time == 2:
        # 更新checkdate
        cursor.execute(update_checkdate_sql, (str(nowtime), ))
        cursor.execute(update_check_lottery_sql)
        # 2020/10/26特别活动，连续7天早上签到三倍水晶奖励
        # 2020/12/18早上签到三倍水晶奖励
        cursor.execute(update_check_lottery_sql)
        cursor.execute(update_check_lottery_sql)
        toaster.show_toast(u'早间签到', u"已经于" + str(nowtime_str) + "早间签到,水晶+240; 剩余水晶：" + str(lottery_crystal),dbm=True)
        toaster_destroy = False
        logging.debug("已经于" + str(nowtime_str) + "早间签到,水晶+240; 剩余水晶：" + str(lottery_crystal))
        # 写入log文件
        file_w = open("kirara_lottery.log", 'a+')
        file_w.write(str(nowtime_str) + "早间签到,水晶+240; 剩余水晶：" + str(lottery_crystal) + "\n")
        file_w.close()
    # 午间签到
    elif last_checkin_time == 3:
        # 更新checkdate
        cursor.execute(update_checkdate_sql, (str(nowtime), ))
        cursor.execute(update_check_lottery_sql)
        toaster.show_toast(u'午间签到', u"已经于" + str(nowtime_str) + "午间签到,水晶+80; 剩余水晶：" + str(lottery_crystal),dbm=True)
        toaster_destroy = False
        logging.debug("已经于" + str(nowtime_str) + "午间签到,水晶+80; 剩余水晶：" + str(lottery_crystal))
        # 写入log文件
        file_w = open("kirara_lottery.log", 'a+')
        file_w.write(str(nowtime_str) + "午间签到,水晶+80; 剩余水晶：" + str(lottery_crystal) + "\n")
        file_w.close()
    # 夜间签到
    elif last_checkin_time == 4:
        # 更新checkdate
        cursor.execute(update_checkdate_sql, (str(nowtime), ))
        cursor.execute(update_check_lottery_sql)
        toaster.show_toast(u'夜间签到', u"已经于" + str(nowtime_str) + "夜间签到,水晶+80; 剩余水晶：" + str(lottery_crystal),dbm=True)
        toaster_destroy = False
        logging.debug("已经于" + str(nowtime_str) + "夜间签到,水晶+80; 剩余水晶：" + str(lottery_crystal))
        # 写入log文件
        file_w = open("kirara_lottery.log", 'a+')
        file_w.write(str(nowtime_str) + "夜间签到,水晶+80; 剩余水晶：" + str(lottery_crystal) + "\n")
        file_w.close()
    elif last_checkin_time == 5:
        toaster.show_toast(u'签到提示', u"目前不在签到时间内~",dbm=True)
        toaster_destroy = False
        logging.debug("目前不在签到时间内~")
    else:
        toaster.show_toast(u'签到提示', u"已经于" + str(last_checkin_time) + "签到,无法重复签到！",dbm=True)
        toaster_destroy = False
        logging.debug("已经于" + str(last_checkin_time) + "签到,无法重复签到！")
    db.commit()      # 提交数据库
    run_game()       # 刷新页面

# 打开lottery_log文件
def click_button_log(log):
    if log == 'kirara':
        file = os.system(r'kirara.log')
    elif log == 'lottery':
        file = os.system(r'kirara_lottery.log')

# 小窗口背景图随机
def small_bg_random():
    small_bg_list = ["48785626.png", "76182830.png", "79270076_46.jpg", "79630371.jpg", 
                "79766498.png", "82730039.png", "82651099.png", "82778068.png", 
                "82788872.png","82977478.png", "83408932(1).png", "83980327.png",
                "85057160_p0.png", "85102162_p0.png",
                #第二期背景图
                "27421218.png", "50489348.jpg", "54968155.jpg", "63511691.png", "65646343.jpg",
                "68068733_18.png", "68068733_19.png", "68485858_30.png", "69076928_14.png",
                "69076928_19.png", "69485543_14.png", "73440912.jpg", "75746571.png",
                #第三期背景图
                "63261643_p0.jpg", "73796140_p0.jpg", "74990422_p0.png", "75689551_p2.jpg",
                "88605301_p0.jpg", "89286311_p0.jpg", "89920989_p0.jpg", "90436688_p23.jpg",
                "90722077_p0.png" ]
    return random.choice(small_bg_list)

# 主窗口背景图顺序
def big_bg_queue(sequence):
    global big_bg
    big_bg_list = ["v1.1.png", "73700395.png", "62593374.jpg", "64457976_7.jpg", "63119355.png",   
              "76717514.jpg", "81925889.png", "83410346.jpg", "83667969.png", "85090331_p0.jpg",
              "69296639_1.png", "60155475(1).png", "90803945_p0.jpg"]
    if sequence < 1:            # 最左侧背景图不能小于序号1
        sequence = 1
        big_bg = 1
    if sequence >= len(big_bg_list):            # 序号超过列表长度时利用余数找图
        sequence = sequence % len(big_bg_list) + 1
    logging.debug(sequence)
    return big_bg_list[sequence - 1]

# 抽奖lottery的判断程序
def open_one_card():
    # 0 白色. 1 蓝色. 2 紫色. 3 橙色. 金卡翻倍
    #   事件        概率 对应颜色
    # 看一集番       100  蓝色
    # 看两集番       50   紫色
    # 看三集番       10   橙色
    # MD两局         300  白色
    # MD十局         50   紫色
    # 炉石战旗一局   100  蓝色
    # 炉石战旗三局   20   紫色
    # 一百现金       3    橙色
    # 十元现金       30   紫色
    # 三元现金       200  白色
    # 半小时其他     100  蓝色
    # 一小时其他     30   紫色
    # 三小时其他     7    橙色
    # 判断金色
    golden = 0
    if random.randint(1, 100) == 1:
        golden = 1
    # 判断奖励
    game_point = random.randint(1, 1000)
    if game_point <= 100:
        color = 1
        reward_text = "看一集番"
    elif game_point <= 150:
        color = 2
        reward_text = "看两集番"
    elif game_point <= 160:
        color = 3
        reward_text = "看三集番"
    elif game_point <= 460:
        color = 0
        reward_text = "MD两局"
    elif game_point <= 510:
        color = 2
        reward_text = "MD十局"
    elif game_point <= 610:
        color = 1
        reward_text = "炉石战旗一局"
    elif game_point <= 630:
        color = 2
        reward_text = "炉石战旗三局"
    elif game_point <= 633:
        color = 3
        reward_text = "一百现金"
    elif game_point <= 663:
        color = 2
        reward_text = "十元现金"
    elif game_point <= 863:
        color = 0
        reward_text = "三元现金"
    elif game_point <= 963:
        color = 1
        reward_text = "半小时其他"
    elif game_point <= 993:
        color = 2
        reward_text = "一小时其他"
    elif game_point <= 1000:
        color = 3
        reward_text = "三小时其他"
    # 金卡效果
    if golden == 1:
        reward_text = reward_text + "(金卡翻倍)"

    return reward_text, color, golden

# 更新屏幕函数
def update_screen(screen, setting=Settings(), button_list=[], text_list=[],
                  typed='', use_small_bg="", home_page_text=[]):
    # 全局变量声明
    global text_len
    global mouse_rollup
    global lottery_mouse_y
    global lottery_mouse_x
    global toaster, toaster_destroy   # win10气泡提示
    global pressed_button

    screen.fill(setting.bg_color)                              # 绘制背景色
    if typed == 'work' or typed == 'achievements_previous' or typed == 'girl' or\
       typed == 'one' or typed == 'achievement' or use_small_bg!="":
        #当规定要使用的small_bg时使用该图，否则使用默认图
        small_bg = "85102162_p0.png" if use_small_bg == "" else use_small_bg
        background = pygame.image.load("image//small_bg//" + small_bg)   # 小窗口背景图片
        screen.blit(background,(0,0))
    elif typed != 'lottery':
        background = pygame.image.load(r"image//big_bg//" + big_bg_queue(big_bg))   # 主窗口背景图片
        screen.blit(background,(0,0))
    # 绘制按钮列表(主要是返回按钮)
    for button in button_list:
        button.draw_pressed_button() if button == pressed_button else button.draw_button()
    # 绘制总时间
    if len(home_page_text)!=0:
        hour = int(home_page_text[0]/60)
        minute = home_page_text[0]%60
        text = "总投入时间: " + str(hour) + "小时" + str(minute) + "分钟"
        print(text)
        hp = TextBasic(width=50, height=20, screen=screen, positionX=850, positionY=15, msg4=text)
        hp.draw_home_page_text()

    if typed == 'work':
        # 绘制文字
        if text_list: 
            positionx = 30
            positiony = 0
            width = 500
            height = 100
            for text in text_list:
                tb = TextBasic(width, height, screen, positionx,
                               positiony - mouse_rollup, text['name'],
                               text['year'], text['company'])
                tb.draw_textbasic()
                positiony += 110
                fpsClock.tick(highFPS)

    if typed == 'achievements_previous':
        # 绘制文字
        if text_list: 
            positionx = 30
            positiony = 10
            width = 500
            height = 100
            for achi in text_list:
                ab = AchievementBasic(width, height, screen, positionx,
                               positiony - mouse_rollup, achi['name'],
                               achi['lastopendate'], achi['planinvest'], 
                               achi['nowinvest'], achi['achievementid'])
                # 点击某一个具体事件后跳转
                if positionx < lottery_mouse_x < positionx + width and \
                        positiony - mouse_rollup < lottery_mouse_y < \
                        positiony - mouse_rollup + height:
                    click_button_achievement(achi)
                else:
                    ab.draw_textbasic()
                positiony += 110
                fpsClock.tick(highFPS)

    if typed == 'lottery':
        # 抽奖页面
        # 绘制抽卡图像
        lottery_lb = LotteryBasic(screen, text_list[0])  
        positionx = 150
        positiony = 100
        width = 300
        height = 400
        # 鼠标事件
        clicked = False
        is_hover = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                # 鼠标位置
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if pygame.Rect(positionx, positiony, width, height).collidepoint(mouse_x, mouse_y) and clicked == False:
                    lottery_lb.draw_mouseeffect(1)
                    is_hover = True
                elif pygame.Rect(positionx - 30, positiony - 40, width + 60, height + 80).collidepoint(mouse_x, mouse_y)\
                     and is_hover == True and clicked == False:
                    # 刷新screen
                    screen.fill(setting.bg_color)
                    lottery_lb.draw_mouseeffect(2)
                    is_hover = False
                elif clicked == False:
                    lottery_lb.draw_lotteryback()

                # 绘制返回按钮
                for button in button_list:
                    button.draw_button()
                # 按下按钮事件
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # 判断是否销毁toaster
                    if not toaster_destroy:
                        toaster.custom_destroy()
                        toaster_destroy = True
                    # 判断是否返回
                    if button.rect.collidepoint(mouse_x, mouse_y):
                        mouse_rollup = 0
                        run_game()
                    
                    # 抽奖主程序
                    if text_list[0] >= 280 and clicked == False and \
                       pygame.Rect(positionx, positiony, width, height).collidepoint(mouse_x, mouse_y):
                        # 刷新screen
                        screen.fill(setting.bg_color)
                        # 减去280水晶抽卡
                        set_sql = "update lottery set lottery_crystal=lottery_crystal-280"
                        cursor.execute(set_sql)
                        # 提交数据库
                        db.commit()
                        # 设置为打开状态
                        clicked = True
                        reward_text, color, golden = open_one_card()
                        # 输出到控制台
                        write_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                                   time.localtime(time.time()))
                        # 页面更新
                        lottery_lb.draw_mouseeffect(3, reward_text, color, golden)
                        # 提前刷新一下奖励页面
                        pygame.display.flip()
                        # 气泡以及控制台输出提示
                        toaster.show_toast(u'抽卡提示', u'' + write_time + " 获得奖励：" + reward_text +
                                     "; 剩余水晶： " + str(text_list[0] - 280), dbm=True)
                        toaster_destroy = False
                        logging.debug(write_time + " 获得奖励：" + reward_text +
                                     "; 剩余水晶： " + str(text_list[0] - 280))
                        # 写入log文件
                        file_w = open("kirara_lottery.log", 'a+')
                        file_w.write(write_time + " 获得奖励：" + reward_text +
                                     "; 剩余水晶： " + str(text_list[0] - 280) + "\n")
                        file_w.close()
                    elif text_list[0] < 280 and clicked == False and \
                       pygame.Rect(positionx, positiony, width, height).collidepoint(mouse_x, mouse_y):
                        # 气泡以及控制台输出提示
                        toaster.show_toast(u'温馨提示(穷就快去工作吖', u'没有足够水晶', dbm=True)
                        toaster_destroy = False
                        logging.debug("没有足够水晶")

                pygame.display.flip()

            # 降低cpu占用率，减少主页面刷新频率，delay一秒从30%降到0.5%
            fpsClock.tick(FPS)

    if typed == 'achievement':
        
        finishAchievement = False   # 判断是否完成这一事件
        small_bg = small_bg_random()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                mouse_x, mouse_y = pygame.mouse.get_pos()   # 鼠标位置
                #画出点击事件具体信息
                achi = text_list[0]
                ab = AchievementBasic(500, 100, screen, 30, 100, achi['name'],
                               achi['lastopendate'], achi['planinvest'], 
                               achi['nowinvest'], achi['achievementid'])
                ab.draw_textbasic()
                # 下面函数跳转一次u_s函数后又进入click_button_achievement中
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    #选择哪个按钮被按下
                    #画出按下的按钮
                    for button in button_list:
                        if button.rect.collidepoint(mouse_x, mouse_y):
                            pressed_button = button
                            update_screen(screen, setting, button_list, text_list, use_small_bg=small_bg)

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:      # 按下按钮事件
                    before_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    duration_minutes = 0                    # 专注持续时间
                    #当倒计时结束后,list将只保留返回按钮,列表长度正确性判断
                    if len(button_list) > 1:
                        # 看论文做实验,50分钟倒计时
                        if button_list[1].rect.collidepoint(mouse_x, mouse_y) and toaster_destroy==True:
                            pygame.display.set_caption("倒计时……") # 设置标题
                            duration_minutes = 50
                            achievement_dt = DecTime(screen, duration_minutes * 60, small_bg)     # 倒计时3000s
                            # 倒计时更新页面
                            while (achievement_dt.hour>0) or (achievement_dt.minute>0) or (achievement_dt.sec>=0):
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        sys.exit()
                                ch = str(achievement_dt.hour)+':'+str(achievement_dt.minute)+':'+str(achievement_dt.sec)
                                achievement_dt.draw_timedec("看论文做实验", ch)
                                achievement_dt.subTime()
                                # 休眠1秒刷新屏幕
                                pygame.time.delay(1000)
                                pygame.display.flip()
                            # 判断成功完成
                            if achievement_dt.sec == -1:
                                finishAchievement = True
                                # 水晶奖励
                                crystal_add = 220
                                # 要说的话
                                achievement_str = "看论文做实验50min 获得了" + str(crystal_add) + "水晶！剩余水晶："

                        # 读书整理书爱培,50分钟倒计时
                        if button_list[2].rect.collidepoint(mouse_x, mouse_y) and toaster_destroy==True:
                            pygame.display.set_caption("倒计时……") # 设置标题
                            duration_minutes = 50
                            achievement_dt = DecTime(screen, duration_minutes * 60, small_bg) 
                            # 倒计时更新页面
                            while (achievement_dt.hour>0) or (achievement_dt.minute>0) or (achievement_dt.sec>=0):
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        sys.exit()
                                ch = str(achievement_dt.hour)+':'+str(achievement_dt.minute)+':'+str(achievement_dt.sec)
                                achievement_dt.draw_timedec("读书整理书爱培", ch)
                                achievement_dt.subTime()
                                # 休眠1秒刷新屏幕
                                pygame.time.delay(1000)
                                pygame.display.flip()
                            # 判断成功完成
                            if achievement_dt.sec == -1:
                                finishAchievement = True
                                # 水晶奖励
                                crystal_add = 200
                                # 要说的话
                                achievement_str = "读书整理书爱培50min 获得了" + str(crystal_add) + "水晶！剩余水晶："

                        # 半个番茄钟,25分钟倒计时
                        if button_list[3].rect.collidepoint(mouse_x, mouse_y) and toaster_destroy==True:
                            pygame.display.set_caption("倒计时……") # 设置标题
                            duration_minutes = 25
                            achievement_dt = DecTime(screen, duration_minutes * 60, small_bg) 
                            # 倒计时更新页面
                            while (achievement_dt.hour>0) or (achievement_dt.minute>0) or (achievement_dt.sec>=0):
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        sys.exit()
                                ch = str(achievement_dt.hour)+':'+str(achievement_dt.minute)+':'+str(achievement_dt.sec)
                                achievement_dt.draw_timedec("半个番茄钟", ch)
                                achievement_dt.subTime()
                                # 休眠1秒刷新屏幕
                                pygame.time.delay(1000)
                                pygame.display.flip()
                            # 判断成功完成
                            if achievement_dt.sec == -1:
                                finishAchievement = True
                                # 水晶奖励
                                crystal_add = 90
                                # 要说的话
                                achievement_str = "半个番茄钟25min 获得了" + str(crystal_add) + "水晶！剩余水晶："

                        # 游戏娱乐,20分钟倒计时
                        # v1.1修改为休息时间,10分钟倒计时
                        if button_list[4].rect.collidepoint(mouse_x, mouse_y) and toaster_destroy==True:
                            pygame.display.set_caption("倒计时……") # 设置标题
                            duration_minutes = 10
                            achievement_dt = DecTime(screen, duration_minutes * 60, small_bg) 
                            # 倒计时更新页面
                            while (achievement_dt.hour>0) or (achievement_dt.minute>0) or (achievement_dt.sec>=0):
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        sys.exit()
                                ch = str(achievement_dt.hour)+':'+str(achievement_dt.minute)+':'+str(achievement_dt.sec)
                                achievement_dt.draw_timedec("休息", ch)
                                achievement_dt.subTime()
                                # 休眠1秒刷新屏幕
                                pygame.time.delay(1000)
                                pygame.display.flip()
                            # 判断成功完成
                            if achievement_dt.sec == -1:
                                finishAchievement = True
                                # 水晶奖励
                                crystal_add = 5
                                # 要说的话
                                achievement_str = "进行了休息10min 获得了" + str(crystal_add) + "水晶！剩余水晶："

                    if finishAchievement == True:       # 完成奖励
                        after_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))    # 当前时间
                        finish_one_achievement = "null"
                        set_crystal_sql = "update lottery set lottery_crystal=lottery_crystal+" + str(crystal_add)  # 水晶增加
                        query_crystal_sql = "Select lottery_crystal from lottery"   # 查询数据库
                        cursor.execute(set_crystal_sql)     # 执行数据库水晶增加指令
                        cursor.execute(query_crystal_sql)        # 查询水晶数量
                        crystal_number = cursor.fetchall()[0][0] # 取出水晶数量
                        #更新数据库中的时间
                        set_invest_sql = "update achievement set nowinvest=nowinvest+%s where achievementid=%s"  # 投入时间增加
                        cursor.execute(set_invest_sql,[duration_minutes, text_list[0]['achievementid']])
                        set_lastdate_sql = "update achievement set lastopendate=%s where achievementid=%s"
                        cursor.execute(set_lastdate_sql, [after_time, text_list[0]['achievementid']])
                        add_sum_time_sql = "update lottery set sum_time=sum_time+" + str(duration_minutes)  # 总投入时间增加
                        cursor.execute(add_sum_time_sql)
                        if (text_list[0]['nowinvest'] + duration_minutes) >= text_list[0]['planinvest']:
                            set_end_sql = "update achievement set enddate=%s where name=%s" # 结束事件时间
                            cursor.execute(set_end_sql,[after_time, text_list[0]['name']])
                            if text_list[0]['planinvest'] > 1200:       # 完成一个大于20h的事件奖励时间分钟3/4的Cys
                                crystal_add = round(text_list[0]['planinvest']*0.75)
                                add_achievement_cys_sql = "update lottery set lottery_crystal=lottery_crystal+" + str(crystal_add) # 完成事件水晶
                                cursor.execute(add_achievement_cys_sql)
                                finish_one_achievement = "恭喜你已经于" + str(after_time) + "完成了事件" + text_list[0]['name'] +\
                                                         " 水晶增加" + str(crystal_add)
                            else:
                                finish_one_achievement = "恭喜你已经于" + str(after_time) + "完成了事件" + text_list[0]['name'] +\
                                                         " 计划时长未大于20h无法获得奖励"
                        # 提交数据库
                        db.commit()
                        # 返回主页面按钮绘制
                        finishAchievement == True and button.draw_button()
                        # 不重复获得奖励
                        finishAchievement = False
                        # 写入log文件
                        file_w = open("kirara_lottery.log", 'a+')
                        # 写入日志
                        file_w.write(before_time + " - " + after_time + 
                            "因 " + achievement_str + " " + str(crystal_number)  + u' 已经为' + 
                            text_list[0]['name'] + u'投资了' + str(duration_minutes) + '分钟' + "\n")
                        if finish_one_achievement != 'null':
                            file_w.write(finish_one_achievement + "\n")
                        # 关闭log文件写入
                        file_w.close()
                        if finish_one_achievement != "null":    # 成就事件完成提示
                            toaster.show_toast(finish_one_achievement, icon_path=KiraraL_icon_path, dbm=True)
                            toaster_destroy = False
                            logging.debug(finish_one_achievement)
                        else:
                            # 弹出气泡进行通知
                            toaster.show_toast(u'番茄完成！', 
                                               u'' + achievement_str + str(crystal_number) 
                                               + u' 已经为' + text_list[0]['name'] + u'投资了' + str(duration_minutes) + '分钟',
                                               icon_path=KiraraL_icon_path,
                                               dbm=True)
                            toaster_destroy = False
                            logging.debug(before_time + "-" + after_time + achievement_str + str(crystal_number)
                                + ' 已经为' + text_list[0]['name'] + '投资了' + str(duration_minutes) + '分钟')
                        #绘制返回按钮
                        button_list = [button_list[0]]

                    # 返回按钮点击事件
                    if button_list[0].rect.collidepoint(mouse_x, mouse_y):
                        mouse_rollup = 0
                        mouse_rollup = 0
                        lottery_mouse_x = 0
                        lottery_mouse_y = 0
                        if not toaster_destroy:
                            toaster.custom_destroy()
                            toaster_destroy = True
                        read_achievements()
                    #一旦进入倒计时画面,button_list将只保留返回按钮,否则还是原先的按钮
                    pressed_button = ""
                    update_screen(screen, setting, button_list, text_list, use_small_bg=small_bg)

                pygame.display.flip()   #刷新屏幕
            fpsClock.tick(FPS)          # 降低cpu占用率，减少主页面刷新频率，delay一秒从30%降到0.5%

    if typed == 'girl':
        positionx = 30
        positiony = 0
        width = 500
        height = 100
        # 绘制女孩
        if text_list:
            for girl in text_list:
                tb = GirlBasic(width, height, screen, positionx,
                               positiony - mouse_rollup, girl)

                # 点击某一个具体女孩后跳转
                if positionx < lottery_mouse_x < positionx + width and \
                        positiony - mouse_rollup < lottery_mouse_y < \
                        positiony - mouse_rollup + height:
                    click_to_one_girl(girl)
                else:
                    tb.draw_textbasic()
                positiony += 110
                fpsClock.tick(highFPS)

    if typed == 'one':
        positionx = 30
        positiony = 0
        width = 500
        height = 100
        # 绘制女孩
        if text_list:
            for girl in text_list:
                updated_girl = sql_update_one(girl)
                tb = GirlBasic(width, height, screen, positionx,
                               positiony , updated_girl)
                tb.draw_textbasic()
                fpsClock.tick(highFPS)
    text_len = len(text_list) * 130
    
    # 显示窗口
    pygame.display.flip()

# 进入单个女孩页面,可以完成抽卡升级操作
def click_to_one_girl(girl):
    # 全局变量声明
    global text_len
    global mouse_rollup
    global lottery_mouse_x
    global lottery_mouse_y
    global toaster

    onegirl_setting = Settingssmallwindow()
    screen_one = pygame.display.set_mode((onegirl_setting.screen_width, onegirl_setting.screen_height))
    button_back = Button(150, 100, screen_one, "返回", 50, 650)
    button_lottery = Button(150, 100, screen_one, "抽卡", 50, 450)
    button_level = Button(150, 100, screen_one, "升级", 350, 450)
    button_skill = Button(250, 100, screen_one, "技能升级", 300, 600)
    button_list = [button_back, button_lottery, button_level, button_skill]
    one_setting = Settings()
    text_list = [girl]
    # 进入girls查看页面
    while True:
        # 监视器
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # 按下button事件
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if button_back.rect.collidepoint(mouse_x, mouse_y) and \
                        event.button == 1:
                    mouse_rollup = 0
                    lottery_mouse_x = 0
                    lottery_mouse_y = 0
                    read_girls()
                elif button_lottery.rect.collidepoint(mouse_x, mouse_y) \
                        and event.button == 1:
                    sig = random.randint(1, 100)
                    increment = 0

                    if 1 <= sig <= 5:
                        toaster.show_toast(u'抽卡提示', u'恭喜你获得S角色卡！好感度+70')
                        logging.debug("恭喜你获得S角色卡！好感度+70")
                        increment = 70
                    elif 6 <= sig <= 15:
                        toaster.show_toast(u'抽卡提示', u'恭喜你获得New角色！')
                        logging.debug("恭喜你获得New角色！")
                    elif 16 <= sig <= 50:
                        toaster.show_toast(u'抽卡提示', u'恭喜你获得A角色卡！好感度+18')
                        logging.debug("恭喜你获得A角色卡！好感度+18")
                        increment = 18
                    elif 61 <= sig <= 100:
                        toaster.show_toast(u'抽卡提示', u'好感度+1！')
                        logging.debug("好感度+1！")
                        increment = 1


                    # 查询好感度并设置其值增加increment
                    query_sql = "Select love from figure where name=%s"
                    cursor.execute(query_sql, [girl.name])
                    for old_love in cursor.fetchall():
                        new_love = int(old_love[0]) + increment

                    # 写入log文件
                    file_w = open("kirara.log", 'a+')
                    write_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                               time.localtime(time.time()))
                    # 判断increment并写入日志
                    if increment == 70:
                        file_w.write(write_time + " " + girl.name +
                                     ": 获得S角色卡！好感度+70  当前好感度: "
                                     + str(new_love) + "\n")
                    elif increment == 18:
                        file_w.write(write_time + " " + str(girl.name) +
                               ": 获得A角色卡！好感度+18  当前好感度: "
                                     + str(new_love) + "\n")
                    elif increment == 1:
                        file_w.write(write_time + " " + str(girl.name) +
                                     ": 好感度+1  当前好感度: "
                                     + str(new_love) + "\n")
                    elif increment == 0:
                        file_w.write(write_time + " 恭喜你获得New角色！\n")

                    # 关闭log文件写入
                    file_w.close()

                    if 0 <= new_love < 50:
                        query_sql = "update figure set love=%s, grade=%s " \
                                    "where name=%s"
                        cursor.execute(query_sql,[new_love, "A", girl.name])
                    elif 50 <= new_love < 150:
                        query_sql = "update figure set love=%s, grade=%s " \
                                    "where name=%s"
                        cursor.execute(query_sql, [new_love, "S", girl.name])
                    elif 150 <= new_love < 350:
                        query_sql = "update figure set love=%s, grade=%s " \
                                    "where name=%s"
                        cursor.execute(query_sql, [new_love, "SS", girl.name])
                    elif 350 <= new_love < 650:
                        query_sql = "update figure set love=%s, grade=%s " \
                                    "where name=%s"
                        cursor.execute(query_sql, [new_love, "SSS", girl.name])
                    elif 650 <= new_love < 1000:
                        query_sql = "update figure set love=%s, grade=%s " \
                                    "where name=%s"
                        cursor.execute(query_sql, [new_love, "EX", girl.name])
                    elif 1000 <= new_love :
                        query_sql = "update figure set love=%s, grade=%s " \
                                    "where name=%s"
                        cursor.execute(query_sql, [new_love, "MAX", girl.name])
                    db.commit()

                elif button_level.rect.collidepoint(mouse_x, mouse_y) and \
                        event.button == 1:
                    sig = random.randint(1, 100)
                    increment = 0

                    if 1 <= sig <= 5:
                        toaster.show_toast(u'升级提示', u'极限训练！等级+10！')
                        logging.debug("极限训练！等级+10！")
                        increment = 10
                    elif 6 <= sig <= 15:
                        toaster.show_toast(u'抽卡提示', u'高效充实的训练！等级+5')
                        logging.debug("高效充实的训练！等级+5")
                        increment = 5
                    elif 16 <= sig <= 35:
                        toaster.show_toast(u'抽卡提示', u'注意力集中的训练！等级+2')
                        logging.debug("注意力集中的训练！等级+2")
                        increment = 2
                    elif 36 <= sig <= 100:
                        toaster.show_toast(u'抽卡提示', u'训练完成！等级+1')
                        logging.debug("训练完成！等级+1")
                        increment = 1

                    # 查询好感度并设置其值增加increment
                    query_sql = "Select level from figure where name=%s"
                    cursor.execute(query_sql, [girl.name])
                    for old_level in cursor.fetchall():
                        new_level = int(old_level[0]) + increment
                    query_sql = "update figure set level=%s where name = %s"
                    cursor.execute(query_sql, [new_level, girl.name])
                    db.commit()

                    # 写入log文件
                    file_w = open("kirara.log", 'a+')
                    write_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                               time.localtime(time.time()))

                    # 判断increment并写入日志
                    if increment == 10:
                        file_w.write(write_time + " " + girl.name +
                                     ": 等级+10  当前等级: "
                                     + str(new_level) + "\n")
                    elif increment == 5:
                        file_w.write(write_time + " " + girl.name +
                                     ": 等级+5  当前等级: "
                                     + str(new_level) + "\n")
                    elif increment == 2:
                        file_w.write(write_time + " " + girl.name +
                                     ": 等级+2  当前等级: "
                                     + str(new_level) + "\n")
                    elif increment == 1:
                        file_w.write(write_time + " " + girl.name +
                                     ": 等级+1  当前等级: "
                                     + str(new_level) + "\n")

                    file_w.close()

                elif button_skill.rect.collidepoint(mouse_x, mouse_y) and \
                    event.button == 1:
                    sig = random.randint(1, 100)
                    increment = 0

                    if 1 <= sig <= 5:
                        toaster.show_toast(u'技能提升提示', u'极限训练！技能等级+5！')
                        logging.debug("极限训练！技能等级+5！")
                        increment = 5
                    elif 6 <= sig <= 15:
                        toaster.show_toast(u'技能提升提示', u'高效充实的训练！技能等级+3')
                        logging.debug("高效充实的训练！技能等级+3")
                        increment = 3
                    elif 16 <= sig <= 35:
                        toaster.show_toast(u'技能提升提示', u'意力集中的训练！技能等级+2')
                        logging.debug("注意力集中的训练！技能等级+2")
                        increment = 2
                    elif 36 <= sig <= 100:
                        toaster.show_toast(u'技能提升提示', u'训练完成！技能等级+1')
                        logging.debug("训练完成！技能等级+1")
                        increment = 1

                    # 查询好感度并设置其值增加increment
                    query_sql = "Select skilllevel from figure where name=%s"
                    cursor.execute(query_sql, [girl.name])
                    for old_level in cursor.fetchall():
                        new_level = int(old_level[0]) + increment
                    query_sql = "update figure set skilllevel=%s where name = %s"
                    cursor.execute(query_sql, [new_level, girl.name])
                    db.commit()

                    # 写入log文件
                    file_w = open("kirara.log", 'a+')
                    write_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                               time.localtime(time.time()))
                    # 判断increment并写入日志
                    if increment == 3:
                        file_w.write(write_time + " " + girl.name +
                                     ": 技能等级+3  当前技能等级: "
                                     + str(new_level) + "\n")
                    elif increment == 5:
                        file_w.write(write_time + " " + girl.name +
                                     ": 技能等级+5  当前技能等级: "
                                     + str(new_level) + "\n")
                    elif increment == 2:
                        file_w.write(write_time + " " + girl.name +
                                     ": 技能等级+2  当前技能等级: "
                                     + str(new_level) + "\n")
                    elif increment == 1:
                        file_w.write(write_time + " " + girl.name +
                                     ": 技能等级+1  当前技能等级: "
                                     + str(new_level) + "\n")

                    file_w.close()

        # 降低cpu占用率，减少主页面刷新频率，delay一秒从30%降到0.5%
        fpsClock.tick(highFPS)

        update_screen(screen_one, one_setting, button_list, text_list, "one")


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
            if button.rect.collidepoint(mouse_x, mouse_y) and event.button == 1:
                mouse_rollup = 0
                run_game()
            if event.button == 5 and mouse_rollup < (text_len - 800):
                mouse_rollup += mouse_roll_dis
            elif event.button == 4 and mouse_rollup >= 0:
                mouse_rollup -= mouse_roll_dis


# 抽奖和返回主页面监视器
def click_lottery_and_index(button):
    # 全局变量声明
    global text_len
    global mouse_rollup
    global lottery_mouse_x
    global lottery_mouse_y

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # 按下button事件
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # 按下左键,先判断是否返回,没有返回记录鼠标点击位置
            if event.button == 1:
                if button.rect.collidepoint(mouse_x, mouse_y):
                    mouse_rollup = 0
                    run_game()
                else:
                    lottery_mouse_x = mouse_x
                    lottery_mouse_y = mouse_y

            if event.button == 5 and mouse_rollup < (text_len - 800):
                mouse_rollup += mouse_roll_dis
            elif event.button == 4 and mouse_rollup > 0:
                mouse_rollup -= mouse_roll_dis


# 返回girls页面函数
def click_to_girls(button):
    # 全局变量声明
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # 按下button事件
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if button.rect.collidepoint(mouse_x, mouse_y):
                read_girls()

# 入场料收取和登录时间记录
def admission_fee():
    global toaster, toaster_destroy
    fee = 1000                                              # 入场费用1000氵
    select_addate_sql = "Select admission_date from lottery"# 查询上次收费时间
    select_lgdate_sql = "Select login_date from lottery"
    cursor.execute(select_addate_sql)                       #获取数据库记录时间

    tuple_tmp = cursor.fetchall()
    last_admission_time = tuple_tmp[0][0]
    cursor.execute(select_lgdate_sql)
    tuple_tmp = cursor.fetchall()
    last_admission_time = tuple_tmp[0][0]
    last_login_time = tuple_tmp[0][0]
    today_date = datetime.datetime.now()
    # 销毁toaster内存占用
    if not toaster_destroy:
        toaster.custom_destroy()
        toaster_destroy = True
    #文件录入登录时间
    if today_date.date().__gt__(last_login_time.date()):
        login_time = today_date.strftime('%Y-%m-%d %H:%M:%S')   #记录登录时刻并去掉秒后面的部分
        update_lgdate_sql = "update lottery set login_date=%s"
        cursor.execute(update_lgdate_sql, (str(today_date), ))
        file_w = open("kirara_lottery.log", 'a+')       # 写入log文件
        file_w.write("\n您已经于 " + str(login_time) + " 登录Kirara Leoworld, 欢迎归来！" + "\n")
        file_w.close()
        db.commit()

    # 入场料收取延时，修改凌晨四点刷新
    check_postpone = 4
    today_date += datetime.timedelta(hours = -check_postpone)
    last_admission_time += datetime.timedelta(hours = -check_postpone)
    if today_date.date().__gt__(last_admission_time.date()):              # 每日时间入场费
        today_date_exact = today_date + datetime.timedelta(hours = +check_postpone)   # 签到时间修改为当前时间
        today_date = today_date.date()
        select_lottery_sql = "Select lottery_crystal from lottery"
        cursor.execute(select_lottery_sql)
        tuple_tmp = cursor.fetchall()
        lottery_crystal = tuple_tmp[0][0]
        if lottery_crystal - fee >= 0:                      # 付得起的情况
            update_crystal_sql = "update lottery set lottery_crystal=lottery_crystal-%s"
            update_addate_sql = "update lottery set admission_date=%s"
            cursor.execute(update_crystal_sql, (str(fee), ))
            cursor.execute(update_addate_sql, (str(today_date_exact), ))
                                                            # 通知和记录
            toaster.show_toast(u'入场料收取', u"已经收取" + str(today_date) + "的费用,水晶-" + str(fee) + 
                                "; 剩余水晶：" + str(lottery_crystal-fee), dbm=True)
            toaster_destroy = False
            file_w = open("kirara_lottery.log", 'a+')       # 写入log文件
            file_w.write(str(today_date) + "入场收费收取,水晶-" + str(fee) + 
                         "; 剩余水晶：" + str(lottery_crystal-fee) + "\n")
            file_w.close()
            db.commit()                                     # 提交数据库
        else:                                               # 付不起的情况
            toaster.show_toast(u'入场料收取失效', u"你于" + str(today_date) + "的费用已经付不起了,白嫖入场; 剩余水晶：" 
                + str(lottery_crystal), dbm=True)
            toaster_destroy = False

# 游戏运行主函数
def run_game():                              # 初始背景图
    pygame.init()                                           # 初始化游戏
    os.environ['SDL_VIDEO_CENTERED'] = '1'                  # 屏幕居中显示
    #设置加载
    ki_setting = Settings()                                 # 加载通用设置
    screen = pygame.display.set_mode(   
        (ki_setting.screen_width, ki_setting.screen_height))# 设置窗口长宽
    pygame.display.set_caption("Kirara Leoworld")           # 设置窗口名称
                                                            # 创建首页四个button列表
    basic_y = 350
    interval_y = 150
    button_girls = Button(400, 100, screen, "girls", 100, basic_y)
    button_works = Button(400, 100, screen, "works", 700, basic_y)
    button_lottery = Button(400, 100, screen, "lottery", 100, basic_y + interval_y)
    button_achievement = Button(400, 100, screen, "selfstudy", 700, basic_y + interval_y)
                                                            # 判断是否可签到,不可签设置Button clickable=0
    if checkin_check() == 2 or checkin_check() == 3 or checkin_check() == 4:
        button_checkin = Button(400, 100, screen, "checkin", 100, basic_y + interval_y * 2)
    else:
        button_checkin = Button(400, 100, screen, "checkin", 100, basic_y + interval_y * 2, 0)
    admission_fee()                                         # 收取每日入场料
    button_kirara_log = Button(195, 100, screen, "klog", 700, basic_y + interval_y * 2)
    button_lottery_log =  Button(195, 100, screen, "llog", 905, basic_y + interval_y * 2)
    button_list = [button_girls, button_works, button_lottery,
                   button_achievement, button_checkin, button_kirara_log,
                   button_lottery_log]

    select_sum_time_sql = "Select sum_time from lottery"# 查询总投入时间
    cursor.execute(select_sum_time_sql)                 #获取数据库记录时间
    tuple_tmp = cursor.fetchall()
    sum_time = tuple_tmp[0][0]

    update_screen(screen, ki_setting, button_list, home_page_text=[sum_time])   # 首先更新一次页面
    check_events(screen, button_list, text_list=[sum_time])                     # 获取鼠标键盘命令

