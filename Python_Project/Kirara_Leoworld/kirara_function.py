import pygame
import sys
import json
import random
import time
import MySQLdb
from kirara_figure import *

mouse_rollup = 0
text_len = 30
lottery_mouse_x = 0
lottery_mouse_y = 0

# 连接数据库
db = MySQLdb.connect("localhost", "root", "sdffdaa1", "kirara_leoworld",
                     charset='utf8')
cursor = db.cursor()


# 监视鼠标和键盘事件
def check_events(button_list):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # 按下button事件
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # if mouse_x > 100 and mouse_x < 500 and mouse_y > 50 and
            # mouse_y < 150:
            tmp = 0
            # 查看鼠标点击在哪个范围内，使用tmp确定是第几个按钮
            for button in button_list:
                tmp += 1
                if button.rect.collidepoint(mouse_x, mouse_y) and tmp == 1:
                    click_button_girls()
                elif button.rect.collidepoint(mouse_x, mouse_y) and tmp == 2:
                    click_button_works()
                elif button.rect.collidepoint(mouse_x, mouse_y) and tmp == 3:
                    click_button_lottery()
                elif button.rect.collidepoint(mouse_x, mouse_y) and tmp == 4:
                    click_button_achievement()


# 按下girls按钮事件
def click_button_girls():
    # 列出女孩子的列表
    read_girls()


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


# 女孩子打印
def read_girls():
    query_sql = "Select * from figure"
    cursor.execute(query_sql)
    tuple_tmp = cursor.fetchall()
    girls_list = []
    for girls in tuple_tmp:
        girls_list.append(Figure(girls[1], girls[2], girls[3], girls[4],
                                 girls[5], girls[6], girls[7], girls[8],
                                 girls[9], girls[10]))

    screen_works = pygame.display.set_mode((600, 800))
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


# 按下mission按钮事件
# 10.06修改为作品按钮
def click_button_works():
    read_works()


# 按下lottery按钮事件
def click_button_lottery():
    # 查询数据库
    query_sql = "Select lottery_num from lottery"
    cursor.execute(query_sql)
    # 取出抽奖次数
    tuple_tmp = cursor.fetchall()
    lottery_num = []
    lottery_num.append(tuple_tmp[0][0])

    screen_lottery = pygame.display.set_mode((600, 800))
    button_back = Button(150, 100, screen_lottery, "返回", 50, 650)
    button_list = [button_back]
    work_setting = Settings()
    # 抽奖页面
    while True:
        # 屏幕更新
        update_screen(screen_lottery, work_setting, button_list, lottery_num,
                      "lottery")



# 按下achievement按钮事件
def click_button_achievement():
    # 抽奖次数+1
    set_sql = "update lottery set lottery_num=lottery_num+1"
    cursor.execute(set_sql)
    # 查询数据库
    query_sql = "Select lottery_num from lottery"
    cursor.execute(query_sql)
    # 取出抽奖次数
    tuple_tmp = cursor.fetchall()[0][0]
    # 提交数据库
    db.commit()
    print("增加后抽奖次数为:" + str(tuple_tmp))

    # 写入log文件
    file_w = open("kirara_lottery.log", 'a+')
    write_time = time.strftime('%Y-%m-%d %H:%M:%S',
                               time.localtime(time.time()))
    # 写入日志
    file_w.write(write_time + " 因为努力工作获得了一次抽奖！剩余抽奖次数： " + str(tuple_tmp) + "\n")

    # 关闭log文件写入
    file_w.close()


# 更新屏幕函数
def update_screen(screen, setting=Settings(), button_list=[], text_list=[],
                  typed=''):
    # 全局变量声明
    global text_len
    global mouse_rollup
    global lottery_mouse_y
    global lottery_mouse_x
    # 绘制背景色
    screen.fill(setting.bg_color)
    # 绘制button1
    for button in button_list:
        button.draw_button()

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

    if typed == 'lottery':
        # 抽奖页面
        # 显示剩余抽奖次数
        lottery_num_text = "剩余抽奖次数：" + str(text_list[0])
        # 绘制抽卡图像
        lottery_lb = LotteryBasic(screen, lottery_num_text)  
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


                # 绘制button1
                for button in button_list:
                    button.draw_button()
                # 按下button事件
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # 先判断是否返回
                    if button.rect.collidepoint(mouse_x, mouse_y):
                        mouse_rollup = 0
                        run_game()

                    # 抽奖主程序
                    if text_list[0] > 0 and clicked == False and \
                       pygame.Rect(positionx, positiony, width, height).collidepoint(mouse_x, mouse_y):
                        # 刷新screen
                        screen.fill(setting.bg_color)
                        # 减去一个抽奖次数
                        set_sql = "update lottery set lottery_num=lottery_num-1"
                        cursor.execute(set_sql)
                        # 提交数据库
                        db.commit()

                        # 设置为打开状态
                        clicked = True

                        # 抽奖动画主程序
                        # 0 白色. 1 蓝色. 2 紫色. 3 橙色
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
                        lottery_lb.draw_mouseeffect(3, reward_text, color)

                        # 写入log文件
                        file_w = open("kirara_lottery.log", 'a+')
                        write_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                                   time.localtime(time.time()))
                        # 写入日志
                        file_w.write(write_time + " 获得奖励：" + reward_text +
                                     "; 剩余抽奖次数： " + str(text_list[0] - 1) + "\n")

                        # 关闭log文件写入
                        file_w.close()

                pygame.display.flip()


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

    screen_one = pygame.display.set_mode((600, 800))
    button_back = Button(150, 100, screen_one, "返回", 50, 650)
    button_lottery = Button(150, 100, screen_one, "抽卡", 50, 450)
    button_level = Button(150, 100, screen_one, "升级", 350, 450)
    button_skill = Button(250, 100, screen_one, "技能升级", 350, 600)
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
                    click_button_girls()
                elif button_lottery.rect.collidepoint(mouse_x, mouse_y) \
                        and event.button == 1:
                    sig = random.randint(1, 100)
                    increment = 0

                    if 1 <= sig <= 5:
                        print("恭喜你获得S角色卡！好感度+70")
                        increment = 70
                    elif 6 <= sig <= 15:
                        print("恭喜你获得New角色！")
                    elif 16 <= sig <= 50:
                        print("恭喜你获得A角色卡！好感度+18")
                        increment = 18
                    elif 61 <= sig <= 100:
                        print("好感度+1！")
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
                        print("极限训练！等级+10！")
                        increment = 10
                    elif 6 <= sig <= 15:
                        print("高效充实的训练！等级+5")
                        increment = 5
                    elif 16 <= sig <= 35:
                        print("注意力集中的训练！等级+2")
                        increment = 2
                    elif 36 <= sig <= 100:
                        print("训练完成！等级+1")
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
                        print("极限训练！技能等级+5！")
                        increment = 5
                    elif 6 <= sig <= 15:
                        print("高效充实的训练！技能等级+3")
                        increment = 3
                    elif 16 <= sig <= 35:
                        print("注意力集中的训练！技能等级+2")
                        increment = 2
                    elif 36 <= sig <= 100:
                        print("训练完成！技能等级+1")
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
                mouse_rollup += 40
            elif event.button == 4 and mouse_rollup >= 0:
                mouse_rollup -= 40


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
        elif event.type == pygame.MOUSEBUTTONDOWN:
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
                mouse_rollup += 40
            elif event.button == 4 and mouse_rollup >= 0:
                mouse_rollup -= 40


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
                click_button_girls()


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

    screen_works = pygame.display.set_mode((600, 800))
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
    screen = pygame.display.set_mode(
        (ki_setting.screen_width, ki_setting.screen_height))
    # 设置窗口名称
    pygame.display.set_caption("Kirara Leoworld")
    # 创建首页四个button列表
    button_girls = Button(400, 100, screen, "girls", 100, 50)
    button_works = Button(400, 100, screen, "works", 700, 50)
    button_lottery = Button(400, 100, screen, "Lottery", 100, 250)
    button_achievement = Button(400, 100, screen, "+1", 700, 250)
    button_list = [button_girls, button_works, button_lottery,
                   button_achievement]

    # 开始游戏
    while True:
        check_events(button_list)
        update_screen(screen, ki_setting, button_list)
