import json
from win10toast import ToastNotifier
from kirara_figure import *
from cards_open import *
from sundry import *
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
KiraraL_icon_path = "icon/V2.1.ico"

mouse_rollup = 0        # 鼠标滑轮转动
mouse_roll_dis = 80     # 鼠标单次滑动敏感度
text_len = 30           # 单个字符长度
lottery_mouse_x = 0     # 鼠标x坐标
lottery_mouse_y = 0     # 鼠标y坐标
big_bg = 1              # 全局背景图编号,从1开始
toaster = ToastNotifier() # 全局toaster，方便destroy
toaster_destroy = True  # toaster已经被destroy
pressed_button = ""     # 按下的button
is_press_text = 0       # 是否按下文本
pressed_text1 = ""      # 按下的文本


def check_events(screen, button_list, text_list):
    """监视主页面事件

    按下对应按钮跳转到不同页面

    Args:
        screen: Setting()设置的页面
        button_list: 主页面按钮
        text_list: [sum_time消耗总时间]
    """
    global big_bg, toaster, toaster_destroy, pressed_button
    while True:
        for event in pygame.event.get():
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
                mouse_x, mouse_y = pygame.mouse.get_pos()
                tmp = 0
                # 销毁toaster内存占用
                if not toaster_destroy:
                    toaster.custom_destroy()
                    toaster_destroy = True
                # 查看鼠标点击在哪个范围内，使用tmp确定是第几个按钮
                # 由于button是在list中不确定，没有tmp就会只进入第一个read_girls_list()函数
                # pressed_button==button用于判断按下的按钮在鼠标抬起后是否还在此处，不在不进入
                for button in button_list:
                    tmp += 1
                    if button.rect.collidepoint(mouse_x, mouse_y) and tmp == 1 and pressed_button==button:
                        read_my_girls()
                    elif button.rect.collidepoint(mouse_x, mouse_y) and tmp == 2 and pressed_button==button:
                        if query_current_assist_girl()!="":
                            read_assist_girl()
                    elif button.rect.collidepoint(mouse_x, mouse_y) and tmp == 3 and pressed_button==button:
                        click_button_lottery()
                    elif button.rect.collidepoint(mouse_x, mouse_y) and tmp == 4 and pressed_button==button:
                        read_knapsack()
                    elif button.rect.collidepoint(mouse_x, mouse_y) and tmp == 5 and pressed_button==button:
                        read_adventures()         # 先选择事件再进入专注选择
                    elif button.rect.collidepoint(mouse_x, mouse_y) and tmp == 6 and pressed_button==button:
                        read_mission(1)
                    elif button.rect.collidepoint(mouse_x, mouse_y) and tmp == 7 and pressed_button==button:
                        read_girls_list()
                #将按下按钮回归
                pressed_button = ""
                update_screen(screen, button_list=button_list, home_page_text=text_list)

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

def read_girls_list():
    """读取目前的角色列表

    跳转到update_screen - girl中，显示所有角色的列表
    """
    query_sql = "Select * from figure"
    cursor.execute(query_sql)
    tuple_tmp = cursor.fetchall()
    girls_list = []
    for girls in tuple_tmp:
        girls_list.append(Figure(girls[0], girls[1], girls[2], girls[3], 
                                 girls[4], girls[5], girls[6], girls[7], 
                                 girls[8], girls[9], girls[10], girls[11], 
                                 girls[12],  girls[13], girls[14], girls[15], 
                                 girls[16],  girls[17], girls[18], girls[19],
                                 skin=girls[20]))
    girl_setting = Settingssmallwindow()
    screen_works = pygame.display.set_mode((girl_setting.screen_width, girl_setting.screen_height))
    button_back = Button(150, 100, screen_works, "返回", 50, 650)
    button_list = [button_back]
    # 进入girls查看页面
    while True:
        # 返回主菜单,检测鼠标滑轮
        click_mouse_and_index(button_list)
        # 屏幕更新
        update_screen(screen_works, girl_setting, button_list, girls_list,
                      'girl', use_small_bg="1", button_height=0)

def select_one_have_girl_all(name=""):
    """查询拥有女武神的信息

    Args:
        name: 女武神名字

    Returns:
        ret: 女武神的对象
    """
    query_sql = "Select * from my_figure where my_figure_name='" + name + "'"
    cursor.execute(query_sql)
    girl = cursor.fetchall()[0]
    query_sql = "Select * from figure where name='" + girl[1] + "'"
    cursor.execute(query_sql)
    info = cursor.fetchall()[0]
    ret = Figure(info[0], info[1], info[2], girl[14], 
                 info[4], info[5], info[6], girl[8], 
                 girl[9], girl[10], girl[11], info[11], 
                 info[12], info[13], info[14], info[15],
                 girl[7], girl[2], info[18], info[19],
                 girl[3], girl[4], girl[5], girl[6],
                 girl[12], girl[13], girl[15])
    return ret

def read_assist_girl():
    """查询助战角色

    跳转到update_screen - one中，显示该角色的详细信息
    """
    setting = Settingssmallwindow()
    screen = pygame.display.set_mode((setting.screen_width, setting.screen_height))
    button_back = Button(150, 100, screen, "返回", 50, 650)
    update_screen(screen, button_list=[button_back], text_list=[select_one_have_girl_all(name=query_current_assist_girl())], typed="one", use_small_bg="1")

def read_my_girls():
    """读取拥有的女武神

    跳转到update_screen - my_girl中，显示目前拥有角色的列表
    """
    query_sql = "Select * from my_figure"
    cursor.execute(query_sql)
    ret_my_figure = cursor.fetchall()
    my_girls_list = []
    for girl in ret_my_figure:
        query_sql = "Select * from figure where name='" + girl[1] + "'"
        cursor.execute(query_sql)
        info = cursor.fetchall()[0]
        my_girls_list.append(Figure(info[0], info[1], info[2], girl[14], 
                                 info[4], info[5], info[6], girl[8], 
                                 girl[9], girl[10], girl[11], info[11], 
                                 info[12], info[13], info[14], info[15],
                                 girl[7], girl[2], info[18], info[19],
                                 girl[3], girl[4], girl[5], girl[6],
                                 girl[12], girl[13], girl[15]))
    my_girls_list.sort(key=lambda t: t.level, reverse=True)   #按照等级降序排序
    girl_setting = Settingssmallwindow()
    screen_works = pygame.display.set_mode((girl_setting.screen_width, girl_setting.screen_height))
    button_back = Button(150, 100, screen_works, "返回", 50, 650)
    button_list = [button_back]
    # 进入girls查看页面
    while True:
        # 返回主菜单,检测鼠标滑轮
        click_mouse_and_index(button_list)
        # 屏幕更新
        update_screen(screen_works, girl_setting, button_list, my_girls_list,
                      'my_girl', use_small_bg="1", button_height=0)

def read_works():
    """读取作品列表

    跳转到update_screen - work 中，显示目前作品的列表
    """
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
    # 进入作品查看页面
    while True:
        # 返回主菜单,检测鼠标滑轮
        click_mouse_and_index(button_list)
        # 屏幕更新
        update_screen(screen_works, work_setting, button_list, work_list,
                      "work", use_small_bg="1")

def read_knapsack():
    """读取背包

    Plans:
        读取背包中武器、圣痕、材料，武器等会显示基础信息
    """
    cursor.execute("select t1.*, t2.type, t2.grade, t2.m_coefficient, t2.feature, t2.feature_info, \
                    t2.value1, t2.value2, t2.value3, t2.value4, t2.value5 \
                    from my_weapon t1, weapon t2 where t1.name=t2.name")
    weapon_tuple = list(cursor.fetchall())
    weapon_tuple = sorted(weapon_tuple, key=lambda x:(x[7], x[2], x[0]), reverse=True)
    weapon_list = []
    for weapon in weapon_tuple:
        weapon_list.append(Weapon(weapon[0], weapon[1], weapon[2], weapon[3], 
                                 weapon[4], weapon[5], weapon[6], weapon[7], 
                                 weapon[8], weapon[9], weapon[10], weapon[11],
                                 weapon[12], weapon[13], weapon[14], weapon[15]))
    cursor.execute("select * from knapsack")
    material_tuple = list(cursor.fetchall())
    material_list = []
    for material in material_tuple:
        material_list.append(Material(material[0], material[1], material[2], material[3]))

    knapsack_setting = Settings()
    screen_knapsack = pygame.display.set_mode((knapsack_setting.screen_width, knapsack_setting.screen_height))
    button_list = [Button(150, 100, screen_knapsack, "返回", 50, 650)]
    while True:
        click_mouse_and_index(button_list)
        update_screen(screen_knapsack, knapsack_setting, button_list, weapon_list, "knapsack", extra_list=material_list)

def read_adventures():
    """读取冒险列表

    跳转到update_screen - adventures_previous 中，显示当前冒险的列表
    """
    query_sql = "Select * from adventure"
    cursor.execute(query_sql)
    tuple_tmp = cursor.fetchall()

    achi_list = []
    for adventures in tuple_tmp:
        if adventures[5] < adventures[4] and adventures[3] == None:       # 仅显示未完成事件
            timestamp = time.mktime(time.strptime(str(adventures[6]), "%Y-%m-%d %H:%M:%S"))
            achi_list.append({'name': adventures[1], 'startdate': adventures[2],
                              'enddate': adventures[3], 'planinvest': adventures[4],
                              'nowinvest': adventures[5], 'adventureid': adventures[0],
                              'lastopendate': adventures[6],'lastopentimestamp': timestamp})

    achi_list = sorted(achi_list, key=lambda key:float(key['lastopentimestamp']),reverse=True)  # 按照id排序
    achieve_setting = Settingssmallwindow()
    screen = pygame.display.set_mode((achieve_setting.screen_width, achieve_setting.screen_height))
    button_back = Button(150, 100, screen, "返回", 50, 650)
    button_list = [button_back]
    while True:
        # 不间断监控鼠标事件
        click_mouse_and_index(button_list)
        # 屏幕更新
        update_screen(screen, Settings(), button_list, achi_list,
                      "adventures_previous", use_small_bg="1")

def read_mission(typed):
    """
    读取任务列表
    """
    mission_setting = Settings()
    screen_mission = pygame.display.set_mode((mission_setting.screen_width, mission_setting.screen_height))
    button_back = Button(150, 100, screen_mission, "返回", 50, 650)
    query_sql = ""
    button_click1, button_click2, button_click3 = "", "", ""
    button_width = 250
    if typed == 1:
        query_sql = "Select * from mission where type='日常任务'"
        button_click1 = Button(button_width, 100, screen_mission, "日常任务", 100, 100, clickable=0)
        button_click2 = Button(button_width, 100, screen_mission, "周常任务", 400, 100)
        button_click3 = Button(button_width, 100, screen_mission, "长期任务", 700, 100)
        #判断是否完成全部日常
        cursor.execute("select getreward from mission where missionid between 1 and 7")
        daily_judge = cursor.fetchall()
        complete_mission = 0
        for m in daily_judge:
            if m[0]==1:
                complete_mission += 1
        cursor.execute("update mission set complete=" + str(complete_mission) + " where missionid=8")
        #判断是否可签到,不可签设置Button clickable=0
        if checkin_check() == 2 or checkin_check() == 3 or checkin_check() == 4:
            cursor.execute("update mission set finish=0 where missionid=9")
        elif checkin_check() == 5:
            cursor.execute("update mission set finish=10 where missionid=9")
        else:
            cursor.execute("update mission set finish=1 where missionid=9")
    elif typed == 2:
        query_sql = "Select * from mission where type='周常任务'"
        button_click1 = Button(button_width, 100, screen_mission, "日常任务", 100, 100)
        button_click2 = Button(button_width, 100, screen_mission, "周常任务", 400, 100, clickable=0)
        button_click3 = Button(button_width, 100, screen_mission, "长期任务", 700, 100)
        #判断是否完成全部周常
        cursor.execute("select getreward from mission where missionid between 10 and 18")
        weekly_judge = cursor.fetchall()
        complete_mission = 0
        for m in weekly_judge:
            if m[0]==1:
                complete_mission += 1
        cursor.execute("update mission set complete=" + str(complete_mission) + " where missionid=19")
    elif typed == 3:
        query_sql = "Select * from mission where type<>'周常任务' and type<>'日常任务'"
        button_click1 = Button(button_width, 100, screen_mission, "日常任务", 100, 100)
        button_click2 = Button(button_width, 100, screen_mission, "周常任务", 400, 100)
        button_click3 = Button(button_width, 100, screen_mission, "长期任务", 700, 100, clickable=0)
    button_list = [button_back, button_click1, button_click2, button_click3]
    cursor.execute(query_sql)
    ret_mission = cursor.fetchall()
    mission_list = []
    for mission in ret_mission:
        mission_list.append(Mission(mission[0], mission[1], mission[2], mission[3], 
                                 mission[4], mission[5], mission[6], mission[7], 
                                 mission[8]))
    # 进入mission任务查看页面
    while True:
        # 返回主菜单,检测鼠标滑轮
        click_mouse_and_index(button_list)
        # 屏幕更新
        update_screen(screen_mission, mission_setting, button_list, mission_list,
                      'mission', use_small_bg="", button_height=0, extra_list=[typed])

def click_button_lottery():
    """按下lottery按钮事件

    跳转到update_screen - lottery 中，进入抽奖页面
    """
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
    # 绘制复位按钮
    button_reset = Button(300, 100, screen_lottery, "再抽一次", 250, 650)
    button_list = [button_back, button_reset]
    work_setting = Settings()
    # 抽奖页面
    while True:
        # 屏幕更新
        update_screen(screen_lottery, work_setting, button_list, lottery_crystal,
                      "lottery", use_small_bg="1", button_height=0)
        # 降低cpu占用率，减少主页面刷新频率，delay一秒从30%降到0.5%
        fpsClock.tick(highFPS)

def click_button_adventure(achi):
    """按下adventure按钮事件

    跳转到update_screen - adventure 中，显示对应的番茄钟

    Args:
        achi: 选择的冒险事件
    """
    achieve_setting = Settingssmallwindow()
    screen_adventure = pygame.display.set_mode((achieve_setting.screen_width, achieve_setting.screen_height))
    button_paper = Button(500, 80, screen_adventure, "一个番茄50min", 50, 240)
    button_learn = Button(500, 80, screen_adventure, "爱好培养60min", 50, 340)
    button_language = Button(500, 80, screen_adventure, "半个番茄25min", 50, 440)
    button_play = Button(240, 80, screen_adventure, "10min", 50, 540)
    button_hplay = Button(240, 80, screen_adventure, "5min", 300, 540)
    button_back = Button(150, 100, screen_adventure, "返回", 50, 650)
    button_list = [button_back, button_paper, button_learn, button_language, button_play, button_hplay]
    work_setting = Settings()
    update_screen(screen_adventure, work_setting, button_list, [achi],
                      "adventure", use_small_bg="1")

def checkin_check():
    """可签到判断函数

    根据签到时间段一天有三次签到机会

    Returns:
        last_checkin_time: 不可签到时，显示上次签到的时间，防止同一时间多次签到
        2：早间可签到
        3：午间可签到
        4：晚间可签到
        5：不在签到时间段
    """
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

def click_button_checkin():
    """按下checkin按钮事件

    多倍签到活动通过多次执行sql语句实现，角色签到相关特性在这里体现
    签到结束后跳转到主页面
    """
    nowtime = datetime.datetime.now()
    nowtime_str = nowtime.strftime('%Y-%m-%d %H:%M:%S')
    #签到特性
    passive_checkin = 1
    passive_onecheck = 1
    toast_passive_msg = ""
    if query_current_assist_girl_feature()=="第二类中二病":
        passive_checkin = 1.2
        toast_passive_msg = ",五更琉璃特性'第二类中二病'发动,"
    elif query_current_assist_girl_feature()=="工作狂":
        passive_onecheck = 3
    crystal_add = int(80 * passive_checkin)
    # 签到增加水晶
    select_lottery_sql = "Select lottery_crystal from lottery"
    update_checkdate_sql = "update lottery set check_date=%s"
    update_check_lottery_sql = "update lottery set lottery_crystal=lottery_crystal+" + str(crystal_add)
    cursor.execute(select_lottery_sql)
    tuple_tmp = cursor.fetchall()
    lottery_crystal = tuple_tmp[0][0]
    lottery_crystal += crystal_add
    last_checkin_time=checkin_check()
    # 气泡通知
    global toaster,toaster_destroy
    # 销毁toaster内存占用
    if not toaster_destroy:
        toaster.custom_destroy()
        toaster_destroy = True
    # 早间签到
    if last_checkin_time == 2:
        # 更新checkdate
        cursor.execute(update_checkdate_sql, (str(nowtime), ))
        if passive_onecheck==3:
            cursor.execute(update_checkdate_sql, (str(nowtime), ))
            cursor.execute(update_checkdate_sql, (str(nowtime), ))
            toast_passive_msg = ",八神光特性'工作狂'发动,"
        cursor.execute(update_check_lottery_sql)
        # 2020/10/26特别活动，连续7天早上签到三倍水晶奖励
        # 2020/12/18早上签到三倍水晶奖励
        toaster.show_toast(u'早间签到', u"已经于" + str(nowtime_str) + "早间签到," + toast_passive_msg +
                             "水晶+"  + str(crystal_add*passive_onecheck) + "; 剩余水晶：" + str(lottery_crystal),
                             icon_path=KiraraL_icon_path, dbm=True)
        toaster_destroy = False
    # 午间签到
    elif last_checkin_time == 3:
        # 更新checkdate
        cursor.execute(update_checkdate_sql, (str(nowtime), ))
        cursor.execute(update_check_lottery_sql)
        toaster.show_toast(u'午间签到', u"已经于" + str(nowtime_str) + "午间签到," + toast_passive_msg + "水晶+"  
                            + str(crystal_add) + "; 剩余水晶：" + str(lottery_crystal), 
                            icon_path=KiraraL_icon_path, dbm=True)
        toaster_destroy = False
    # 夜间签到
    elif last_checkin_time == 4:
        # 更新checkdate
        cursor.execute(update_checkdate_sql, (str(nowtime), ))
        cursor.execute(update_check_lottery_sql)
        toaster.show_toast(u'夜间签到', u"已经于" + str(nowtime_str) + "夜间签到," + toast_passive_msg + "水晶+"  
                            + str(crystal_add) + "; 剩余水晶：" + str(lottery_crystal), 
                            icon_path=KiraraL_icon_path, dbm=True)
        toaster_destroy = False
    elif last_checkin_time == 5:
        toaster.show_toast(u'签到提示', u"目前不在签到时间内~", icon_path=KiraraL_icon_path, dbm=True)
        toaster_destroy = False
        logging.debug("目前不在签到时间内~")
    else:
        toaster.show_toast(u'签到提示', u"已经于" + str(last_checkin_time) + "签到,无法重复签到！", 
                            icon_path=KiraraL_icon_path, dbm=True)
        toaster_destroy = False
        logging.debug("已经于" + str(last_checkin_time) + "签到,无法重复签到！")
    commitDB()
    read_mission(1)       # 刷新页面

def big_bg_queue(sequence):
    """主窗口背景图顺序

    根据提供的顺序号，主背景图进行翻页，当翻到最左边时不再递减

    Args:
        sequence: 主页面图顺序号

    Returns:
        big_bg_list[sequence - 1]: 顺序号对应的图片名
    """
    global big_bg
    big_bg_list = ["v2.1.png", "v2.0.png", "v1.2.png", "v1.1.png", 
              "73700395.png", "62593374.jpg", "64457976_7.jpg", "63119355.png",   
              "76717514.jpg", "81925889.png", "83410346.jpg", "85090331_p0.jpg",
              "69296639_1.png", "60155475(1).png"]
    if sequence < 1:            # 最左侧背景图不能小于序号1
        sequence = 1
        big_bg = 1
    if sequence >= len(big_bg_list):            # 序号超过列表长度时利用余数找图
        sequence = sequence % len(big_bg_list) + 1
    return big_bg_list[sequence - 1]

def update_screen(screen, setting=Settings(), button_list=[], text_list=[], typed='', 
                  use_small_bg="", home_page_text=[], draw_achi=[], draw_text=[], button_height=1, 
                  extra_list=[]):
    """更新屏幕函数

    根据提供的参数先填补底色后绘制页面，并flip刷新显示窗口

    Args:
        screen: 需要更新的surface
        setting: 更新的参数(应该可以不用，因为screen自带了)
        button_list: 绘制的按钮列表，如果有和全局表里pressed_button相等的按钮，
            调用其对应的draw_pressed_button()函数
        text_list: 绘制的文字列表
        typed: 调用其他绘制函数
        use_small_bg:  '' - 不使用小图
                       '1' - 使用小图默认图
                       'file.png' - 使用small_bg，'file.png'图
        home_page_text: [sum_time] - 总投入时间
        draw_achi: 绘制冒险事件
        draw_text: 绘制一次事件结束的文字
        button_height: 1 - 带阴影有按钮效果的按钮
                       0 - 不带阴影的普通按钮
    """
    # 全局变量声明
    global text_len
    global mouse_rollup
    global lottery_mouse_y
    global lottery_mouse_x
    global toaster, toaster_destroy   # win10气泡提示
    global pressed_button
    # 绘制背景色
    screen.fill(setting.bg_color)
    if use_small_bg!="":
        #当规定要使用的small_bg时使用该图，否则使用默认图
        small_bg = "85102162_p0.png" if use_small_bg == "1" else use_small_bg
        # 小窗口背景图片
        background = pygame.image.load("image//small_bg//" + small_bg)
        screen.blit(background,(0,0))
    else:
        # 主窗口背景图片
        background = pygame.image.load(r"image//big_bg//" + big_bg_queue(big_bg))
        screen.blit(background,(0,0))
    # 绘制事件结束的文字
    if(len(draw_text)!=0):
        for text in draw_text:
            text.draw_complete_text()
    # 绘制按钮列表(主要是返回按钮)
    for button in button_list:
        button.draw_pressed_button() if button == pressed_button else button.draw_button(button_height)
    # 绘制总时间
    if len(home_page_text)!=0:
        hour = int(home_page_text[0]/60)
        minute = home_page_text[0]%60
        text = "总投入时间: " + str(hour) + "小时" + str(minute) + "分钟"
        hp = TextBasic(width=50, height=20, screen=screen, positionX=850, positionY=15, msg4=text)
        hp.draw_home_page_text()
    # 绘制一个冒险事件
    if(len(draw_achi)!=0):
        for achi_ in draw_achi:
            achi_.draw_textbasic()
    # 这些选项运行画出列表页面
    one_list_len = 130
    if typed == 'work' or typed == 'girl' or typed == 'adventures_previous' or typed == 'my_girl':
        one_list_len = draw_list(screen, typed, button_list, text_list)
    # 绘制抽奖页面
    if typed == 'lottery':
        draw_lottery(screen, button_list, text_list)
    # 绘制冒险页面
    if typed == 'adventure':
        draw_adventure(screen, button_list, text_list)
    #绘制选择女武神页面
    if typed == 'one':
        draw_the_one_girl(screen, button_list, text_list)
    #绘制详情页的女武神页面
    if typed == 'one_only_read':
        draw_the_one_girl_only_read(screen, button_list, text_list)
    #绘制任务页面
    if typed == 'mission':
        one_list_len = draw_mission(screen, button_list, text_list, extra_list[0])
    #绘制背包页面
    if typed == 'knapsack':
        draw_knapsack(screen, button_list, text_list, extra_list)
    # 获取文字列表总长度            
    text_len = len(text_list) * one_list_len
    # 显示窗口
    pygame.display.flip()


def draw_knapsack(screen, button_list, weapon_list, material_list):
    """绘制背包页面

    在此页面显示拥有的武器、消耗品材料

    Args:
        screen: 当前surface
        button_list: 返回按钮
        weapon_list: 所有拥有的武器
        material_list: 所有拥有的消耗品材料
    """
    # 全局变量声明
    global mouse_rollup, lottery_mouse_x, lottery_mouse_y
    global pressed_button
    global toaster, toaster_destroy

    one_tb = KnapsackBasic(screen, weapon_list, material_list)
    one_tb.draw_origin_pack()
    pygame.display.flip()
    while True:
        # 监视器
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # 按下button事件
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_list[0].rect.collidepoint(mouse_x, mouse_y):
                    pressed_button = button_list[0]
                    update_screen(screen, button_list=button_list, text_list=weapon_list, 
                        typed="knapsack", extra_list=material_list, button_height=0)
                else:
                    for rect in one_tb.rect_image_list:
                        if rect.collidepoint(mouse_x, mouse_y):
                            pressed_button = rect

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # 判断是否销毁toaster
                if not toaster_destroy:
                    toaster.custom_destroy()
                    toaster_destroy = True
                if button_list[0].rect.collidepoint(mouse_x, mouse_y) and event.button == 1 and pressed_button == button_list[0]:
                    mouse_rollup = 0
                    lottery_mouse_x = 0
                    lottery_mouse_y = 0
                    run_game()
                else:
                    for rect in one_tb.rect_image_list:
                        if rect.collidepoint(mouse_x, mouse_y) and pressed_button==rect:
                            update_screen(screen, button_list=button_list, button_height=1)
                            one_tb.draw_origin_pack()
                            one_tb.draw_special_pack(rect)
            # 降低cpu占用率，减少主页面刷新频率，delay一秒从30%降到0.5%
            pygame.display.flip()
        fpsClock.tick(highFPS)


def draw_mission(screen, button_list, text_list, typed):
    """绘制任务列表函数

    在此页面绘制可通过滚轮滚动的任务列表页面，在上方可选择按钮

    Args:
        screen: 当前surface
        #button_list: 返回、日常、周常、长期任务按钮
        text_list: 储存需要滚动的对象们的列表
    """
    global is_press_text, pressed_text1
    global toaster, toaster_destroy
    # 绘制文字
    positionx = 30
    positiony = 210
    width = 1000
    height = 50
    positiony_add = 55
    for text in text_list:
        mb = MissionBasic(width, height, screen, positionx,
                           positiony - mouse_rollup, text)
        # 按下高亮
        if is_press_text == 1 and mb.have_image_rect.collidepoint(lottery_mouse_x, lottery_mouse_y):
            mb.draw_missionbasic()
            pressed_text1 = mb
        else:
            mb.draw_missionbasic()

        # 同一文字块选中进入，不同区域刷新选中
        if is_press_text == 2 and type(pressed_text1)==type(mb) and \
            pressed_text1.have_image_rect.collidepoint(lottery_mouse_x, lottery_mouse_y) and \
            pressed_text1.ready_to_click==True:
            is_press_text = 0
            # 判断是否销毁toaster
            if not toaster_destroy:
                toaster.custom_destroy()
                toaster_destroy = True
            selected_mission = pressed_text1.get_mission()
            #签到另算
            if selected_mission.missionid == 9:
                click_button_checkin()
            else:
                reward_text = mission_complete(selected_mission.missionid)
                toaster.show_toast(u'提示', u"领取任务奖励: " + reward_text, icon_path=KiraraL_icon_path, dbm=True)
                toaster_destroy = False
            read_mission(typed)
        elif is_press_text == 2:
            is_press_text = 0
            pressed_text1 = ""
        positiony += positiony_add  # 下一个文本间隔距离
    # 每秒运行帧数
    fpsClock.tick(highFPS)
    return positiony_add + 20

def draw_adventure(screen, button_list, text_list):
    """绘制冒险选择页面

    在此页面选择番茄钟，并进入倒计时

    Args:
        screen: 当前surface
        button_list: 返回按钮和4个番茄钟按钮
        text_list: [achi] - 点击事件具体信息
    """
    # 全局变量声明
    global mouse_rollup
    global lottery_mouse_y
    global lottery_mouse_x
    global toaster, toaster_destroy   # win10气泡提示
    global pressed_button
    
    finishadventure = False   # 判断是否完成这一事件
    small_bg = small_bg_random()
    #画出点击事件具体信息
    achi = text_list[0]
    ab = AdventureBasic(500, 100, screen, 30, 100, achi)
    ab.draw_textbasic()
    draw_text = []
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            mouse_x, mouse_y = pygame.mouse.get_pos()   # 鼠标位置
            # 下面函数跳转一次u_s函数后又进入click_button_adventure中
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                #选择哪个按钮被按下
                #画出按下的按钮
                for button in button_list:
                    if button.rect.collidepoint(mouse_x, mouse_y):
                        pressed_button = button
                        update_screen(screen, button_list=button_list, text_list=text_list, use_small_bg=small_bg, draw_achi=[ab], draw_text=draw_text)
            # 按下按钮事件
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:      
                before_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                #当倒计时结束后,list将只保留返回按钮,列表长度正确性判断
                if len(button_list) > 1:
                    # 看论文做实验,50分钟倒计时
                    if button_list[1].rect.collidepoint(mouse_x, mouse_y) and toaster_destroy==True:
                       finishadventure, duration_minutes, crystal_add, \
                       adventure_str, adventure_dt = countdown(screen, 0, small_bg)

                    # 读书整理书爱培,50分钟倒计时
                    if button_list[2].rect.collidepoint(mouse_x, mouse_y) and toaster_destroy==True:
                        finishadventure,duration_minutes, crystal_add, \
                        adventure_str, adventure_dt = countdown(screen, 1, small_bg)

                    # 半个番茄钟,25分钟倒计时
                    if button_list[3].rect.collidepoint(mouse_x, mouse_y) and toaster_destroy==True:
                        finishadventure,duration_minutes, crystal_add, \
                        adventure_str, adventure_dt = countdown(screen, 2, small_bg)

                    # 游戏娱乐,20分钟倒计时
                    # v1.1修改为休息时间,10分钟倒计时
                    if button_list[4].rect.collidepoint(mouse_x, mouse_y) and toaster_destroy==True:
                       finishadventure,duration_minutes, crystal_add, \
                       adventure_str, adventure_dt = countdown(screen, 3, small_bg)

                    # v2.1增加新休息时间,5分钟倒计时
                    if button_list[5].rect.collidepoint(mouse_x, mouse_y) and toaster_destroy==True:
                       finishadventure,duration_minutes, crystal_add, \
                       adventure_str, adventure_dt = countdown(screen, 4, small_bg)

                if finishadventure == True:       # 完成奖励
                    after_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))    # 当前时间
                    finish_one_adventure = "null"
                    set_crystal_sql = "update lottery set lottery_crystal=lottery_crystal+" + str(crystal_add)  # 水晶增加
                    query_crystal_sql = "Select lottery_crystal from lottery"   # 查询数据库
                    cursor.execute(set_crystal_sql)     # 执行数据库水晶增加指令
                    cursor.execute(query_crystal_sql)        # 查询水晶数量
                    crystal_number = cursor.fetchall()[0][0] # 取出水晶数量
                    #更新数据库中的时间
                    set_invest_sql = "update adventure set nowinvest=nowinvest+%s where adventureid=%s"  # 投入时间增加
                    cursor.execute(set_invest_sql,[duration_minutes, achi['adventureid']])
                    set_lastdate_sql = "update adventure set lastopendate=%s where adventureid=%s"
                    cursor.execute(set_lastdate_sql, [after_time, achi['adventureid']])
                    add_sum_time_sql = "update lottery set sum_time=sum_time+" + str(duration_minutes)  # 总投入时间增加
                    cursor.execute(add_sum_time_sql)
                    remark = adventure_dt.public_stuff     #备注掉落品信息
                    if (achi['nowinvest'] + duration_minutes) >= achi['planinvest']:
                        set_end_sql = "update adventure set enddate=%s where name=%s" # 结束事件时间
                        cursor.execute(set_end_sql,[after_time, achi['name']])
                        if achi['planinvest'] > 1200:       # 完成一个大于20h的事件奖励时间分钟3/4的Cys
                            crystal_add = round(achi['planinvest']*0.75)
                            add_adventure_cys_sql = "update lottery set lottery_crystal=lottery_crystal+" + str(crystal_add) # 完成事件水晶
                            cursor.execute(add_adventure_cys_sql)
                            finish_one_adventure = "恭喜你已经于" + str(after_time) + "完成了事件" + achi['name'] +\
                                                     " 水晶增加" + str(crystal_add)
                            remark = finish_one_adventure
                        else:
                            finish_one_adventure = "恭喜你已经于" + str(after_time) + "完成了事件" + achi['name'] +\
                                                     " 计划时长未大于20h无法获得奖励"
                            remark = finish_one_adventure
                    #记录日志数据库
                    insert_log_sql = "insert into log_adventure(name, last_time, starttime, endtime, crystal_add, crystal_hold, assistant, remark) values('" \
                        + achi['name'] + "'," + str(duration_minutes) + ",'" + \
                        before_time + "','" + after_time + "'," + str(crystal_add) + \
                        "," + str(crystal_number) + ",'" + query_current_assist_girl() + "','" + remark + "')" 
                    cursor.execute(insert_log_sql)
                    #事件结束后的任务
                    if "写作" in achi['name']:
                        cursor.execute("update mission set complete=complete+1 where missionid=1")
                    if "阅读" in achi['name']:
                        cursor.execute("update mission set complete=complete+1 where missionid=2")
                    if duration_minutes>=60:
                        cursor.execute("update mission set complete=complete+1 where missionid=6")
                    #完成6次冒险事件
                    cursor.execute("update mission set complete=complete+1 where missionid=5")
                    #专注8小时
                    addhours = round(duration_minutes / 60, 2)
                    cursor.execute("update mission set complete=complete+" + str(addhours) + " where missionid=7")
                    #周任务10-16
                    week_num = (int(achi['adventureid']) - 1)%7
                    cursor.execute("update mission set complete=complete+" + str(addhours) + \
                                 " where missionid=10+" + str(week_num))
                    #专注40小时
                    cursor.execute("update mission set complete=complete+" + str(addhours) + " where missionid=17")
                    commitDB()
                    # 返回主页面按钮绘制
                    finishadventure == True and button_list[0].draw_button()
                    finishadventure = False # 不重复获得奖励
                    # 冒险事件完成提示
                    if finish_one_adventure != "null":    
                        toaster.show_toast(finish_one_adventure, icon_path=KiraraL_icon_path, dbm=True)
                        toaster_destroy = False
                        logging.debug(finish_one_adventure)
                    else:
                        # 弹出气泡进行通知
                        toaster.show_toast(u'番茄完成！', 
                                           u'' + adventure_str + str(crystal_number) 
                                           + u' 已经为' + achi['name'] + u'投资了' + str(duration_minutes) + '分钟',
                                           icon_path=KiraraL_icon_path,
                                           dbm=True)
                        toaster_destroy = False
                        logging.debug(before_time + "-" + after_time + adventure_str + str(crystal_number)
                            + ' 已经为' + achi['name'] + '投资了' + str(duration_minutes) + '分钟')
                    #绘制返回按钮
                    button_list = [button_list[0]]
                    # 绘制结束页面的冒险卡片
                    ab = AdventureBasic(500, 100, screen, 30, 100, achi, duration_minutes)
                    ab.draw_textbasic()
                    # 绘制结束文字
                    draw_text.append(adventure_dt)

                # 返回按钮点击事件
                if button_list[0].rect.collidepoint(mouse_x, mouse_y):
                    mouse_rollup = 0
                    mouse_rollup = 0
                    lottery_mouse_x = 0
                    lottery_mouse_y = 0
                    if not toaster_destroy:
                        toaster.custom_destroy()
                        toaster_destroy = True
                    read_adventures()
                #一旦进入倒计时画面,button_list将只保留返回按钮,否则还是原先的按钮
                pressed_button = ""
                update_screen(screen, button_list=button_list, text_list=text_list, use_small_bg=small_bg, draw_achi=[ab], draw_text=draw_text)

            pygame.display.flip()   #刷新屏幕
        fpsClock.tick(FPS)          # 降低cpu占用率，减少主页面刷新频率，delay一秒从30%降到0.5%

def draw_list(screen, typed, button_list, text_list):
    """绘制可滚动列表函数

    在此页面绘制可通过滚轮滚动的页面

    Args:
        screen: 当前surface
        typed:  work - 作品列表
                girl - 角色列表
                my_girl - 拥有的角色列表
                adventures_previous - 选择冒险事件列表
        button_list: 返回按钮
        text_list: 储存需要滚动的对象们的列表
    """
    global is_press_text, pressed_text1
    # 绘制文字
    positionx = 30
    positiony = 10
    width = 530
    height = 100
    positiony_add = 110
    temp = 0
    for text in text_list:
        #############################################################
        if typed=='work': 
            tb = TextBasic(width, height, screen, positionx,
                           positiony - mouse_rollup, text['name'],
                           text['year'], text['company'])
            # 按下高亮
            if is_press_text == 1 and tb.rect.collidepoint(lottery_mouse_x, lottery_mouse_y):
                tb.draw_pressed_textbasic()
                pressed_text1 = tb
            else:
                tb.draw_textbasic()
            # 同一文字块选中，不同区域刷新选中
            if is_press_text == 2 and type(pressed_text1)!=str and pressed_text1.rect.collidepoint(lottery_mouse_x, lottery_mouse_y):
                is_press_text = 0
                if type(pressed_text1)==type(tb):
                    logging.debug(text)
            elif is_press_text == 2:
                is_press_text = 0
                pressed_text1 = ""
        #############################################################
        if typed=='girl':
            height = 135
            positiony_add = 145
            gb = GirlBasic(width, height, screen, positionx,
                               positiony - mouse_rollup, text)
            # 按下高亮
            if is_press_text == 1 and gb.rect.collidepoint(lottery_mouse_x, lottery_mouse_y):
                gb.draw_girl_list_pressed_textbasic()
                pressed_text1 = gb
            else:
                gb.draw_girl_list_textbasic()
            # 同一文字块选中进入，不同区域刷新选中
            if is_press_text == 2 and type(pressed_text1)!=str and pressed_text1.rect.collidepoint(lottery_mouse_x, lottery_mouse_y):
                is_press_text = 0
                if type(pressed_text1)==type(gb):
                    update_screen(screen, button_list=button_list, 
                        text_list=[pressed_text1.get_girl_text()], typed="one_only_read", use_small_bg="1")
            elif is_press_text == 2:
                is_press_text = 0
                pressed_text1 = ""
        #############################################################
        if typed=='my_girl':
            height = 135
            positiony_add = 145
            gb = GirlBasic(width, height, screen, positionx,
                               positiony - mouse_rollup, text)
            # 按下高亮
            if is_press_text == 1 and gb.rect.collidepoint(lottery_mouse_x, lottery_mouse_y):
                gb.draw_my_girl_list_pressed_textbasic()
                pressed_text1 = gb
            else:
                gb.draw_my_girl_list_textbasic()
            # 同一文字块选中进入，不同区域刷新选中
            if is_press_text == 2 and type(pressed_text1)!=str and pressed_text1.rect.collidepoint(lottery_mouse_x, lottery_mouse_y):
                is_press_text = 0
                if type(pressed_text1)==type(gb):
                    update_screen(screen, button_list=button_list, 
                        text_list=[pressed_text1.get_girl_text()], typed="one", 
                        use_small_bg="1")
            elif is_press_text == 2:
                is_press_text = 0
                pressed_text1 = ""
        #############################################################
        if typed=='adventures_previous':
            ab = AdventureBasic(width, height, screen, positionx,
                               positiony - mouse_rollup, text)
            # 按下高亮
            if is_press_text == 1 and ab.rect.collidepoint(lottery_mouse_x, lottery_mouse_y):
                ab.draw_pressed_textbasic()
                pressed_text1 = ab
            else:
                ab.draw_textbasic()
            # 同一文字块选中进入，不同区域刷新选中
            if is_press_text == 2 and type(pressed_text1)!=str and pressed_text1.rect.collidepoint(lottery_mouse_x, lottery_mouse_y):
                is_press_text = 0
                if type(pressed_text1)==type(ab):
                        click_button_adventure(pressed_text1.get_adventurebasic_text())
            elif is_press_text == 2:
                is_press_text = 0
                pressed_text1 = ""
        positiony += positiony_add  # 下一个文本间隔距离
        temp += 1                   # 点击进入哪个事件
    # 每秒运行帧数
    fpsClock.tick(highFPS)
    return positiony_add + 20

def draw_lottery(screen, button_list, text_list):
    """绘制抽奖页面

    在此页面绘制抽奖页面，可通过点击卡牌抽奖

    Args:
        screen: 当前surface
        button_list: 复位按钮和返回按钮
        text_list: [lottery_crystal] - 当前拥有的水晶
    """
    global toaster, toaster_destroy    # win10气泡提示
    lottery_crystal = text_list[0]
    must_num = query_how_long_to_5star_charc()  #剩余保底次数
    up = "平泽唯"      #抽奖up角色池设置
    crystal_to_lottery = 280    #抽奖限制
    lottery_lb = LotteryBasic(screen, lottery_crystal, must_num, up)  
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
            # 获取鼠标位置
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if pygame.Rect(positionx, positiony, width, height).collidepoint(mouse_x, mouse_y) and clicked == False:
                lottery_lb.draw_mouseeffect(1)  #1悬停效果
                is_hover = True
            elif pygame.Rect(positionx - 30, positiony - 40, width + 60, height + 80).collidepoint(mouse_x, mouse_y)\
                 and is_hover == True and clicked == False:
                lottery_lb.draw_mouseeffect(2)  #2离开效果
                is_hover = False
                # 刷新screen
                update_screen(screen, button_list=button_list, text_list=text_list, typed="lottery", use_small_bg="1", button_height=0)
            elif clicked == False:
                lottery_lb.draw_lotteryback()
            # 按下按钮事件
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # 判断是否销毁toaster
                if not toaster_destroy:
                    toaster.custom_destroy()
                    toaster_destroy = True
                # 判断返回/复位抽奖页面
                tmp = 0
                for button in button_list:
                    tmp += 1
                    if button.rect.collidepoint(mouse_x, mouse_y) and tmp == 1:
                        mouse_rollup = 0
                        run_game()
                    elif button.rect.collidepoint(mouse_x, mouse_y) and tmp == 2:
                        click_button_lottery()
                # 抽奖主程序
                if text_list[0] >= crystal_to_lottery and clicked == False and \
                   pygame.Rect(positionx, positiony, width, height).collidepoint(mouse_x, mouse_y):
                    # 刷新screen
                    update_screen(screen, button_list=button_list, use_small_bg="1", button_height=0)
                    # 减去280水晶抽卡
                    set_sql = "update lottery set lottery_crystal=lottery_crystal-280"
                    cursor.execute(set_sql)
                    #日常、周常任务抽奖次数
                    cursor.execute("update mission set complete=complete+1 where missionid=4")
                    cursor.execute("update mission set complete=complete+1 where missionid=18")
                    # 提交数据库
                    commitDB()
                    # 设置为打开状态
                    clicked = True
                    # 获取抽奖结果
                    reward_text, color, new = open_girls_card(must_num, up)
                    # 输出到控制台
                    write_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                               time.localtime(time.time()))
                    # 页面更新
                    lottery_lb.draw_mouseeffect(3, reward_text, color, new)
                    # 提前刷新一下奖励页面
                    pygame.display.flip()
                    # 气泡以及控制台输出提示
                    if new == 0:
                        toaster.show_toast(u'抽卡提示', u'' + write_time + " 获得奖励：" + reward_text + "; 剩余水晶： " + 
                            str(text_list[0] - 280), icon_path=KiraraL_icon_path, dbm=True)
                    elif new == 1:
                        toaster.show_toast(u'抽卡提示', u'' + write_time + " 获得新角色：" + reward_text + "! 剩余水晶： " +
                         str(text_list[0] - 280), icon_path=KiraraL_icon_path, dbm=True)
                    toaster_destroy = False
                    logging.debug(write_time + " 获得奖励：" + reward_text +
                                 "; 剩余水晶： " + str(text_list[0] - 280))
                elif text_list[0] < crystal_to_lottery and clicked == False and \
                   pygame.Rect(positionx, positiony, width, height).collidepoint(mouse_x, mouse_y):
                    # 气泡以及控制台输出提示
                    toaster.show_toast(u'温馨提示', u'没有足够水晶,水晶数大于' + str(crystal_to_lottery) + '才可抽卡', 
                        icon_path=KiraraL_icon_path, dbm=True)
                    toaster_destroy = False
                    logging.debug("没有足够水晶")
            pygame.display.flip()
        fpsClock.tick(highFPS)

def draw_the_one_girl(screen, button_list, text_list):
    """绘制进入单个女孩页面

    在此页面可以完成升级、升阶、查看技能、好感度，装备武器(未完成)操作

    Args:
        screen: 当前surface
        button_list: 返回按钮
        text_list: [girl] - 该女武神的对象
    """
    # 全局变量声明
    global mouse_rollup, lottery_mouse_x, lottery_mouse_y
    global pressed_button
    global toaster, toaster_destroy

    girl = text_list[0]
    one_tb = TheSelectFigureBasic(screen, girl)
    one_tb.draw_theselectgirlbasic(query_current_assist_girl())
    pygame.display.flip()
    select_exp_book_4 = 0
    select_exp_book_3 = 0
    select_exp_book_2 = 0
    iterative_depth = 0
    while True:
        # 监视器
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # 按下button事件
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_list[0].rect.collidepoint(mouse_x, mouse_y):
                    pressed_button = button_list[0]
                    update_screen(screen, button_list=button_list, text_list=text_list, typed="one", use_small_bg="1")
                elif one_tb.rect_level.collidepoint(mouse_x, mouse_y):
                    pressed_button = one_tb.rect_level
                elif one_tb.rect_love.collidepoint(mouse_x, mouse_y):
                    pressed_button = one_tb.rect_love
                elif one_tb.rect_feature.collidepoint(mouse_x, mouse_y):
                    pressed_button = one_tb.rect_feature
                elif one_tb.rect_assist.collidepoint(mouse_x, mouse_y):
                    pressed_button = one_tb.rect_assist
                elif one_tb.rect_cgradeup.collidepoint(mouse_x, mouse_y):
                    pressed_button = one_tb.rect_cgradeup
                elif one_tb.rect_clevel.collidepoint(mouse_x, mouse_y):
                    pressed_button = one_tb.rect_clevel
                elif one_tb.rect_4exp.collidepoint(mouse_x, mouse_y) and iterative_depth==2:
                    pressed_button = one_tb.rect_4exp
                elif one_tb.rect_3exp.collidepoint(mouse_x, mouse_y) and iterative_depth==2:
                    pressed_button = one_tb.rect_3exp
                elif one_tb.rect_2exp.collidepoint(mouse_x, mouse_y) and iterative_depth==2:
                    pressed_button = one_tb.rect_2exp
                elif one_tb.rect_levelUp.collidepoint(mouse_x, mouse_y) and iterative_depth==2:
                    pressed_button = one_tb.rect_levelUp
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # 判断是否销毁toaster
                if not toaster_destroy:
                    toaster.custom_destroy()
                    toaster_destroy = True
                if button_list[0].rect.collidepoint(mouse_x, mouse_y) and event.button == 1 and pressed_button == button_list[0]:
                    mouse_rollup = 0
                    lottery_mouse_x = 0
                    lottery_mouse_y = 0
                    read_my_girls()
                #点击等级、品质详情
                elif one_tb.rect_level.collidepoint(mouse_x, mouse_y) and event.button == 1 and pressed_button == one_tb.rect_level:
                    update_screen(screen, button_list=button_list, text_list=text_list,  use_small_bg="1")
                    one_tb.draw_theselectgirlbasic(query_current_assist_girl())  #重新绘制页面,去掉之前的底部信息
                    one_tb.draw_click_rect_level()
                    iterative_depth = 1
                #点击好感度详情
                elif one_tb.rect_love.collidepoint(mouse_x, mouse_y) and event.button == 1 and pressed_button == one_tb.rect_love:
                    update_screen(screen, button_list=button_list, text_list=text_list,  use_small_bg="1")
                    one_tb.draw_theselectgirlbasic(query_current_assist_girl())
                    one_tb.draw_click_rect_love()
                    iterative_depth = 1
                #点击人物特性详情   
                elif one_tb.rect_feature.collidepoint(mouse_x, mouse_y) and event.button == 1 and pressed_button == one_tb.rect_feature:
                    update_screen(screen, button_list=button_list, text_list=text_list,  use_small_bg="1")
                    one_tb.draw_theselectgirlbasic(query_current_assist_girl())
                    one_tb.draw_click_rect_feature()
                    iterative_depth = 1
                #选择当前角色作为助阵角色
                elif one_tb.rect_assist.collidepoint(mouse_x, mouse_y) and event.button == 1 and pressed_button == one_tb.rect_assist:
                    #判断助阵按钮为蓝色(可点击)
                    if one_tb.assist_color==one_tb.blue_color:
                        update_sql = "update lottery set current_girl= '" + girl.name + "'"
                        cursor.execute(update_sql)
                        commitDB()
                        #db.commit()
                        toaster.show_toast(u'提示', u"更改助战角色成功！" + girl.name + "正在待命", icon_path=KiraraL_icon_path, dbm=True)
                        toaster_destroy = False
                        one_tb = TheSelectFigureBasic(screen, girl)
                        update_screen(screen, button_list=button_list, text_list=[girl],  use_small_bg="1")
                        one_tb.draw_theselectgirlbasic(query_current_assist_girl())

                    elif one_tb.cgradeup_color==one_tb.grey_color:
                        update_sql = "update lottery set current_girl=''"
                        cursor.execute(update_sql)
                        commitDB()
                        #db.commit()
                        toaster.show_toast(u'提示', u"取消助战角色成功！目前没有助战角色", icon_path=KiraraL_icon_path, dbm=True)
                        toaster_destroy = False
                        one_tb = TheSelectFigureBasic(screen, girl)
                        update_screen(screen, button_list=button_list, text_list=[girl],  use_small_bg="1")
                        one_tb.draw_theselectgirlbasic(query_current_assist_girl())
                #消耗碎片提升品质
                elif one_tb.rect_cgradeup.collidepoint(mouse_x, mouse_y) and event.button == 1 and pressed_button == one_tb.rect_cgradeup:
                    #判断品质提升按钮为蓝色(可点击)
                    if one_tb.cgradeup_color==one_tb.blue_color:
                        next_grade = formula_grade_up(girl.grade)
                        #自强者被动
                        girl.fragment -= one_tb.need_fragment
                        update_sql = "update my_figure set grade = '" + next_grade + "' where my_figure_name = '" + girl.name + "'"
                        cursor.execute(update_sql)
                        update_sql = "update my_figure set fragment = " + str(girl.fragment) + " where my_figure_name = '" + girl.name + "'"
                        cursor.execute(update_sql)
                        commitDB()
                        girl.grade = next_grade
                        toaster.show_toast(u'升阶提示', u"升阶成功！" + girl.name + "成功升阶为" + girl.grade + "品质！", 
                            icon_path=KiraraL_icon_path, dbm=True)
                        toaster_destroy = False
                        one_tb = TheSelectFigureBasic(screen, girl)
                        update_screen(screen, button_list=button_list, text_list=[girl],  use_small_bg="1")
                        one_tb.draw_theselectgirlbasic(query_current_assist_girl())
                        one_tb.draw_click_rect_level()
                    elif one_tb.cgradeup_color==one_tb.grey_color:
                        toaster.show_toast(u'升阶提示', u'' + girl.name + "没有足够的角色碎片", icon_path=KiraraL_icon_path, dbm=True)
                        toaster_destroy = False
                #消耗强化经验提高角色等级
                elif one_tb.rect_clevel.collidepoint(mouse_x, mouse_y) and event.button == 1 and pressed_button == one_tb.rect_clevel:
                    quantity_4, quantity_3, quantity_2 = query_how_many_exp_books()
                    one_tb.draw_click_rect_clevel(quantity_4, quantity_3, quantity_2)
                    iterative_depth = 2
                #点击角色书
                elif one_tb.rect_4exp.collidepoint(mouse_x, mouse_y) and event.button == 1 and pressed_button == one_tb.rect_4exp:
                    quantity_4, quantity_3, quantity_2 = query_how_many_exp_books()
                    if select_exp_book_4<quantity_4:
                        select_exp_book_4 += 1
                    one_tb.draw_click_books(select_exp_book_4, select_exp_book_3, select_exp_book_2)
                elif one_tb.rect_3exp.collidepoint(mouse_x, mouse_y) and event.button == 1 and pressed_button == one_tb.rect_3exp:
                    quantity_4, quantity_3, quantity_2 = query_how_many_exp_books()
                    if select_exp_book_3<quantity_3:
                        select_exp_book_3 += 1
                    one_tb.draw_click_books(select_exp_book_4, select_exp_book_3, select_exp_book_2)
                elif one_tb.rect_2exp.collidepoint(mouse_x, mouse_y) and event.button == 1 and pressed_button == one_tb.rect_2exp:
                    quantity_4, quantity_3, quantity_2 = query_how_many_exp_books()
                    if select_exp_book_2<quantity_2:
                        select_exp_book_2 += 1
                    one_tb.draw_click_books(select_exp_book_4, select_exp_book_3, select_exp_book_2)
                #升级模块
                elif one_tb.rect_levelUp.collidepoint(mouse_x, mouse_y) and event.button == 1 and pressed_button == one_tb.rect_levelUp:
                    new_level, new_exp = formula_levelUp_with_expbook(girl.level, girl.exp,select_exp_book_4, select_exp_book_3, select_exp_book_2)
                    update_sql = "update my_figure set level=" + str(new_level) + ",exp=" + str(new_exp) + " where my_figure_name='" + girl.name + "'"
                    cursor.execute(update_sql)
                    update_sql = "update knapsack set number=number-" + str(select_exp_book_4) + " where id=3"
                    cursor.execute(update_sql)
                    update_sql = "update knapsack set number=number-" + str(select_exp_book_3) + " where id=4"
                    cursor.execute(update_sql)
                    update_sql = "update knapsack set number=number-" + str(select_exp_book_2) + " where id=5"
                    cursor.execute(update_sql)
                    #日常任务角色升级
                    cursor.execute("update mission set complete=complete+1 where missionid=3")
                    commitDB()
                    girl.level = new_level
                    girl.exp = new_exp
                    quantity_4 -= select_exp_book_4
                    quantity_3 -= select_exp_book_3
                    quantity_2 -= select_exp_book_2
                    toaster.show_toast(u'升级提示', u"提升成功！" + girl.name + "目前等级为" + str(girl.level) + "！", icon_path=KiraraL_icon_path, dbm=True)
                    toaster_destroy = False
                    one_tb = TheSelectFigureBasic(screen, girl)
                    update_screen(screen, button_list=button_list, text_list=[girl],  use_small_bg="1")
                    one_tb.draw_theselectgirlbasic(query_current_assist_girl())
                    one_tb.draw_click_rect_level()
                else:
                    pressed_button = ""
                    update_screen(screen, button_list=button_list, text_list=text_list, typed="one", use_small_bg="1")
                    iterative_depth = 0

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if one_tb.rect_4exp.collidepoint(mouse_x, mouse_y) or\
                     one_tb.rect_3exp.collidepoint(mouse_x, mouse_y) or\
                     one_tb.rect_2exp.collidepoint(mouse_x, mouse_y):
                    pressed_button = one_tb
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                if one_tb.rect_4exp.collidepoint(mouse_x, mouse_y) and event.button == 3 and pressed_button == one_tb:
                    if select_exp_book_4 > 0:
                        select_exp_book_4 -= 1
                    one_tb.draw_click_books(select_exp_book_4, select_exp_book_3, select_exp_book_2)
                elif one_tb.rect_3exp.collidepoint(mouse_x, mouse_y) and event.button == 3 and pressed_button == one_tb:
                    if select_exp_book_3 > 0:
                        select_exp_book_3 -= 1
                    one_tb.draw_click_books(select_exp_book_4, select_exp_book_3, select_exp_book_2)
                elif one_tb.rect_2exp.collidepoint(mouse_x, mouse_y) and event.button == 3 and pressed_button == one_tb:
                    if select_exp_book_2 > 0:
                        select_exp_book_2 -= 1
                    one_tb.draw_click_books(select_exp_book_4, select_exp_book_3, select_exp_book_2)
                else:
                    pressed_button = ""
            # 降低cpu占用率，减少主页面刷新频率，delay一秒从30%降到0.5%
            pygame.display.flip()
        fpsClock.tick(highFPS)

def draw_the_one_girl_only_read(screen, button_list, text_list):
    """绘制详情页进入单个女孩页面

    在此页面可以完成查看技能、好感度

    Args:
        screen: 当前surface
        button_list: 返回按钮
        text_list: [girl] - 该女武神的对象
    """
    # 全局变量声明
    global mouse_rollup, lottery_mouse_x, lottery_mouse_y
    global pressed_button
    global toaster, toaster_destroy

    girl = text_list[0]
    one_tb = TheSelectFigureBasic(screen, girl)
    one_tb.draw_theselectgirlbasic_only_read()
    pygame.display.flip()
    while True:
        # 监视器
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # 按下button事件
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_list[0].rect.collidepoint(mouse_x, mouse_y):
                    pressed_button = button_list[0]
                    update_screen(screen, button_list=button_list, text_list=text_list, typed="one_only_read", use_small_bg="1")
                elif one_tb.rect_love.collidepoint(mouse_x, mouse_y):
                    pressed_button = one_tb.rect_love
                elif one_tb.rect_feature.collidepoint(mouse_x, mouse_y):
                    pressed_button = one_tb.rect_feature
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # 判断是否销毁toaster
                if not toaster_destroy:
                    toaster.custom_destroy()
                    toaster_destroy = True
                if button_list[0].rect.collidepoint(mouse_x, mouse_y) and event.button == 1 and pressed_button == button_list[0]:
                    mouse_rollup = 0
                    lottery_mouse_x = 0
                    lottery_mouse_y = 0
                    read_girls_list()
                #点击好感度详情
                elif one_tb.rect_love.collidepoint(mouse_x, mouse_y) and event.button == 1 and pressed_button == one_tb.rect_love:
                    update_screen(screen, button_list=button_list, text_list=text_list,  use_small_bg="1")
                    one_tb.draw_theselectgirlbasic_only_read()
                    one_tb.draw_click_rect_love()
                #点击人物特性详情   
                elif one_tb.rect_feature.collidepoint(mouse_x, mouse_y) and event.button == 1 and pressed_button == one_tb.rect_feature:
                    update_screen(screen, button_list=button_list, text_list=text_list,  use_small_bg="1")
                    one_tb.draw_theselectgirlbasic_only_read()
                    one_tb.draw_click_rect_feature()

            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                    pressed_button = ""
            # 降低cpu占用率，减少主页面刷新频率，delay一秒从30%降到0.5%
            fpsClock.tick(highFPS)
            pygame.display.flip()

def countdown(screen, option, small_bg):
    """进行倒计时

    计算倒计时和回归奖励

    Args:
        screen：当前surface
        option：0-4对应["一个番茄", "测试用例", "半个番茄", 10min休息, 5min休息]
        small_bg：背景小图

    Returns:
        finishadventure:    True - 完成事件
                            False - 未完成事件
        duration_minutes: 事件持续时间
        crystal_add: 时间结束后水晶增加数量
        return_str: toast通知的奖励文字
        adventure_dt: 绘制到页面的奖励文字
    """
    duration_minutes_list = [50, 60, 25, 10, 5]         # 4种不同选项的数据
    text_list = ["一个番茄", "爱好培养", "半个番茄", "起来走走", "小休息"]
    crystal_add_list = [220, 260, 90, 5, 2]             # 基础水晶奖励
    a_minute_coeffi = 60                                #一分钟具有多少秒系数
    duration_minutes = duration_minutes_list[option]    # 持续时间
    text = text_list[option]                            # 显示文字
    passive_duration = 1                                #角色特性时间加成
    assist_girl_name = query_current_assist_girl()
    if query_current_assist_girl_feature()=="单纯与幸运":
        passive_duration = 1.1
    pygame.display.set_caption("倒计时……") # 设置标题
    adventure_dt = DecTime(screen, duration_minutes * a_minute_coeffi * passive_duration, small_bg) 
    # 倒计时更新页面
    while (adventure_dt.hour>0) or (adventure_dt.minute>0) or (adventure_dt.sec>=0):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        # 规范时间显示
        str_hour = "0" + str(adventure_dt.hour) if adventure_dt.hour < 10 else str(adventure_dt.hour)
        str_minute = "0" + str(adventure_dt.minute) if adventure_dt.minute < 10 else str(adventure_dt.minute)
        str_sec = "0" + str(adventure_dt.sec) if adventure_dt.sec < 10 else str(adventure_dt.sec)
        ch = str_hour+':'+str_minute+':'+str_sec
        adventure_dt.draw_timedec(text, ch)
        adventure_dt.subTime()
        # 休眠1秒刷新屏幕
        pygame.time.delay(1000)
        pygame.display.flip()
    # 判断成功完成
    if adventure_dt.sec == -1:
        finishadventure = True
        crystal_basic = crystal_add_list[option]
        crystal_add, stuff_drop, color_ret, love_add = adventure_end_with_girl_reward(duration_minutes, crystal_basic)
        # 要说的话
        if stuff_drop!="":
            stuff_drop = "本次掉落物品:" + stuff_drop
        return_str = "进行了" + text + str(duration_minutes) + "min 获得了" + str(crystal_add) + "水晶！" + stuff_drop + "。剩余水晶： "
        adventure_str = "进行了" + text + str(duration_minutes) + "min 获得了" + str(crystal_add) + "水晶"
        # 更新类属性
        adventure_dt.public_text = text + "结束"
        adventure_dt.public_ch = adventure_str
        adventure_dt.public_stuff = stuff_drop
        adventure_dt.stuff_color_ret = color_ret
        if assist_girl_name!="":
            if int(love_add)==0:
                adventure_dt.love_add = assist_girl_name + "好感已经达到上限"
            else:
                adventure_dt.love_add = assist_girl_name + "好感增加" + str(round(love_add, 2)) + "点"
        return finishadventure, duration_minutes, crystal_add, return_str, adventure_dt

def adventure_end_with_girl_reward(duration_minutes, crystal_basic):
    """根据当前助阵角色，计算冒险结束后的奖励

    Returns:
        crystal_add: 加成后的水晶
        stuff_drop: 掉落的物品
        color_ret: 掉落物品的品质颜色
        (love_add:  有助战角色时,增加的好感度)
    """
    #无助战角色时
    if query_current_assist_girl()=="":
        #enthusiasm高品质材料加成
        enthusiasm_rate = 1
        crystal_add = crystal_basic
        if duration_minutes >= 20:          #时间大于等于20分钟才会掉落物品
            stuff_drop, color_ret = adventure_end_material_acquisition(enthusiasm_rate)
            if stuff_drop=="100水晶":
                crystal_add += 100
            elif stuff_drop=="50水晶":
                crystal_add += 50
        elif duration_minutes <20:
            stuff_drop = ""
            color_ret = 2
        return crystal_add, stuff_drop, color_ret
    else:
        girl = select_one_have_girl_all(name=query_current_assist_girl())
        #角色特性列表
        passive_moe = 0
        passive_yxr = 0
        passive_intimacy = 0
        passive_enthusiasm = 0
        passive_stuff_drop = 0
        passive_crystal_rate = 1
        if girl.feature=="亲妹妹":
            passive_yxr = 100
        elif girl.feature=="天然呆":
            passive_moe = 80
        elif girl.feature=="专心工作":
            passive_stuff_drop = 0.05
        elif girl.feature=="单纯与幸运":
            passive_stuff_drop = 0.25
            passive_crystal_rate = 0.5
        elif girl.feature=="热情":
            passive_crystal_rate = 1.1
        elif girl.feature=="单线程天才":
            query_sql = "select count(*) from log_adventure where to_days(endtime) = to_days(now()) AND last_time>=25"
            cursor.execute(query_sql)
            count = cursor.fetchall()[0][0]
            if count >=5:
                passive_crystal_rate = 1.2
        #水晶加成计算
        if duration_minutes >= 30:
            basic = girl.moe
            coefficient = girl.m_coefficient
            passive = passive_moe
        elif duration_minutes < 30:
            basic = girl.intimacy
            coefficient = girl.i_coefficient
            passive = passive_intimacy
        crystal_add = crystal_basic * (1 + formula_four_dismension_add(girl.yxr, girl.y_coefficient, girl.grade, girl.level, passive_yxr) / 1000)
        #yxr好感度加成，时间除以10乘以yxr加成系数
        love_add = (duration_minutes / 10) * (1 + formula_four_dismension_add(girl.yxr, girl.y_coefficient, girl.grade, girl.level, passive_yxr) / 1000)
        query_sql = "select love from my_figure where my_figure_name='" + girl.name + "'"
        cursor.execute(query_sql)
        love_after = cursor.fetchall()[0][0] + love_add
        #好感度不能超过当前阶级上限
        if love_after > formula_grade_love_limit(girl.grade):
            love_after = formula_grade_love_limit(girl.grade)
            love_add = 0
        update_sql = "update my_figure set love=" + str(love_after) + " where my_figure_name='" + girl.name + "'"
        cursor.execute(update_sql)
        #enthusiasm高品质材料加成
        if duration_minutes>=20:
            enthusiasm_rate = 1 + passive_stuff_drop + formula_four_dismension_add(girl.enthusiasm, girl.e_coefficient, girl.grade, girl.level, passive_enthusiasm) / 1000
            stuff_drop, color_ret = adventure_end_material_acquisition(enthusiasm_rate)
            if stuff_drop=="100水晶":
                crystal_add += 100
            elif stuff_drop=="50水晶":
                crystal_add += 50
        elif duration_minutes<20:
            stuff_drop = ""
            color_ret = 2
        return int(crystal_add), stuff_drop, color_ret, love_add

def query_current_assist_girl():
    """查询当前助阵角色

    Returns:
        query_ret: 助阵角色名
    """
    query_sql = "select current_girl from lottery" 
    cursor.execute(query_sql)
    query_ret = cursor.fetchall()[0][0]
    if query_ret==None:
        query_ret = ""
    return query_ret

def query_current_assist_girl_feature():
    """查询当前助阵角色特性

    Returns:
        query_ret: 助阵角色名特性
    """
    if query_current_assist_girl()=="":
        return ""
    query_sql = "select feature from figure where name='" + query_current_assist_girl() + "'"
    cursor.execute(query_sql)
    query_ret = cursor.fetchall()[0][0]
    return query_ret

def click_mouse_and_index(button_list):
    """鼠标和返回主页面监视器

    记录鼠标位置和鼠标点击事件，修改全局变量

    Args:
        button_list: 返回按钮
    """
    # 全局变量声明
    global text_len
    global mouse_rollup, lottery_mouse_x, lottery_mouse_y
    global is_press_text

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # 按下button事件
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            lottery_mouse_x = mouse_x
            lottery_mouse_y = mouse_y
            is_press_text = 1
            
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # 按下左键,先判断是否返回,没有返回记录鼠标点击位置
            if event.button == 1:
                if button_list[0].rect.collidepoint(mouse_x, mouse_y):
                    is_press_text = 0
                    mouse_rollup = 0
                    run_game()
                else:
                    is_press_text = 2
                    lottery_mouse_x = mouse_x
                    lottery_mouse_y = mouse_y
                #为任务页面选择何种任务的处理项
                if len(button_list)==4:
                    if button_list[1].clickable==1 and button_list[1].rect.collidepoint(mouse_x, mouse_y):
                        is_press_text = 0
                        mouse_rollup = 0
                        read_mission(1)
                    elif button_list[2].clickable==1 and button_list[2].rect.collidepoint(mouse_x, mouse_y):
                        is_press_text = 0
                        mouse_rollup = 0
                        read_mission(2)
                    elif button_list[3].clickable==1 and button_list[3].rect.collidepoint(mouse_x, mouse_y):
                        is_press_text = 0
                        mouse_rollup = 0
                        read_mission(3)

            if event.button == 5 and mouse_rollup < (text_len - 600):
                mouse_rollup += mouse_roll_dis
            elif event.button == 4 and mouse_rollup > 0:
                mouse_rollup -= mouse_roll_dis

def admission_fee():
    """入场料收取和登录时间记录

    每日根据延时时间第一次上线后收取入场料，并记录收取的时间

    2021.8.30修改为入场料1000 - 1，不在收取较高费用
    """
    global toaster, toaster_destroy
    fee = 1                                              # 入场费用1氵
    select_addate_sql = "Select admission_date from lottery"# 查询上次收费时间
    select_lgdate_sql = "Select login_date from lottery"

    cursor.execute(select_addate_sql)                       #获取数据库记录上次收入场费时间
    tuple_tmp = cursor.fetchall()
    last_admission_time = tuple_tmp[0][0]
    cursor.execute(select_lgdate_sql)                       #获取上次登录时间
    tuple_tmp = cursor.fetchall()
    last_login_time = tuple_tmp[0][0]

    today_date = datetime.datetime.now()
    # 销毁toaster内存占用
    if not toaster_destroy:
        toaster.custom_destroy()
        toaster_destroy = True
    #录入登录时间
    if today_date.date().__gt__(last_login_time.date()):
        login_time = today_date.strftime('%Y-%m-%d %H:%M:%S')   #记录登录时刻并去掉秒后面的部分
        update_lgdate_sql = "update lottery set login_date=%s"
        cursor.execute(update_lgdate_sql, (str(today_date), ))
        commitDB()

    # 入场料收取延时，修改凌晨四点刷新
    check_postpone = 4
    today_date += datetime.timedelta(hours = -check_postpone)
    last_admission_time += datetime.timedelta(hours = -check_postpone)
    #周常任务重置
    week_sen = "; 日常任务已重置"
    if today_date.isocalendar()[1]!=last_admission_time.isocalendar()[1]:
        reset_sql1 = "update mission set getreward=0 where type='周常任务'"
        reset_sql2 = "update mission set complete=0 where type='周常任务'"
        cursor.execute(reset_sql1)
        cursor.execute(reset_sql2)
        week_sen = week_sen + "; 周常任务已重置"

    if today_date.date().__gt__(last_admission_time.date()):              # 每日时间入场费和任务重置
        today_date_exact = today_date + datetime.timedelta(hours = +check_postpone)   # 签到时间修改为当前时间
        today_date = today_date.date()
        select_lottery_sql = "Select lottery_crystal from lottery"
        cursor.execute(select_lottery_sql)
        tuple_tmp = cursor.fetchall()
        lottery_crystal = tuple_tmp[0][0]
        #日任务重置
        reset_sql1 = "update mission set getreward=0 where type='日常任务'"
        reset_sql2 = "update mission set complete=0 where type='日常任务'"
        cursor.execute(reset_sql1)
        cursor.execute(reset_sql2)

        if lottery_crystal - fee >= 0:                      # 付得起的情况
            update_crystal_sql = "update lottery set lottery_crystal=lottery_crystal-%s"
            update_addate_sql = "update lottery set admission_date=%s"
            cursor.execute(update_crystal_sql, (str(fee), ))
            cursor.execute(update_addate_sql, (str(today_date_exact), ))
                                                            # 通知和记录
            toaster.show_toast(u'入场料收取', u"已经收取" + str(today_date) + "的费用,水晶-" + str(fee) + 
                                "; 剩余水晶：" + str(lottery_crystal-fee) + week_sen, icon_path=KiraraL_icon_path, dbm=True)
            toaster_destroy = False
            commitDB()
        else:                                               # 付不起的情况
            toaster.show_toast(u'入场料收取失效', u"你于" + str(today_date) + "的费用已经付不起了,白嫖入场; 剩余水晶：" 
                + str(lottery_crystal) + week_sen, icon_path=KiraraL_icon_path, dbm=True)
            toaster_destroy = False


def run_game():                              # 初始背景图
    """游戏运行主函数

    根据按下的按钮通过 check_events 跳转到不同的页面

    Plans:
        背包显示 - 武器、圣痕、材料，同时能对其进行一定的操作，比如升级、分解、觉醒
        商城功能 - 替换现有的签到按钮
        任务功能 - 替换现有的签到按钮，同时把签到按钮转移进去
    """
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
    button_girls = Button(400, 100, screen, "女武神", 100, basic_y)
    assist_name = "无" if query_current_assist_girl()=="" else query_current_assist_girl()
    button_my_girl = Button(400, 100, screen, "助:"+assist_name, 700, basic_y)
    button_lottery = Button(205, 100, screen, "抽卡", 100, basic_y + interval_y)
    button_pack = Button(185, 100, screen, "背包", 315, basic_y + interval_y)
    button_adventure = Button(400, 100, screen, "新的冒险", 700, basic_y + interval_y)
    button_mission = Button(400, 100, screen, "任务", 100, basic_y + interval_y * 2)
    # # 判断是否可签到,不可签设置Button clickable=0
    # if checkin_check() == 2 or checkin_check() == 3 or checkin_check() == 4:
    #     button_checkin = Button(400, 100, screen, "签到", 100, basic_y + interval_y * 2)
    # else:
    #     button_checkin = Button(400, 100, screen, "签到", 100, basic_y + interval_y * 2, 0)
    admission_fee()                                         # 收取每日入场料
    button_kirara_girls_list = Button(400, 100, screen, "角色列表", 700, basic_y + interval_y * 2)
    button_list = [button_girls, button_my_girl, button_lottery, button_pack,
                   button_adventure, button_mission, button_kirara_girls_list]
    ##############################测试语句区域##############################

    ########################################################################
    select_sum_time_sql = "Select sum_time from lottery"# 查询总投入时间
    cursor.execute(select_sum_time_sql)                 #获取数据库记录时间
    tuple_tmp = cursor.fetchall()
    sum_time = tuple_tmp[0][0]
    # 首先更新一次页面
    update_screen(screen, ki_setting, button_list, home_page_text=[sum_time])   
    # 获取鼠标键盘命令
    check_events(screen, button_list, text_list=[sum_time])