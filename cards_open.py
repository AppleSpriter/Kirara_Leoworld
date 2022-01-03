import MySQLdb
import random
import time

# mysqlclient连接数据库
db = MySQLdb.connect("localhost", "root", "sdffdaa1", "kirara_leoworld",
                     charset='utf8')
cursor = db.cursor()

def commitDB():
    debug = 0
    if debug==0:
        db.commit()
    return

def open_girls_card(must_num, up=""):
    """抽奖lottery的判断程序

    #   事件          概率      颜色
    # 5星武器         0.3%      橙色
    # 初始S角色       0.7%      橙色
    # 4星武器         2.5%      紫色
    # 初始A角色       5.0%      紫色
    # 4星强化料*(1-2) 4.0%      紫色
    # 4星角色书*(1-2) 8.0%      紫色
    # 3星强化料*(1-3) 10%       蓝色
    # 3星角色书*(1-3) 40%       蓝色
    # 2星强化料*(2-5) 4.5%      白色
    # 2星角色书*(2-5) 25%       白色

    Args:
        must_num: 还有多少次必出传说5星（保底机制）
        up: 当前池子Up的传说角色

    Returns:
        reward_text: 抽奖奖励的名字
        color_ret: 抽奖奖励的显示颜色
        new:    1 - 新角色
                0 - 已拥有角色
    """
    # 长度为10
    prob = [3, 7, 25, 50, 40, 80, 100, 400, 45, 250] 
    #5 橙色   4 紫色    3 蓝色    2 白色
    color = [5, 5, 4, 4, 4, 4, 3, 3, 2, 2]
    # 判断奖励
    if must_num<=23:
        legend_random_point = random.randint(1, 23)
        if legend_random_point >= must_num:
            game_point = random.randint(1, 10)
        else:
            game_point = random.randint(1, 1000)
    else:
        game_point = random.randint(1, 1000)            #debug测试修改lhhcxxg 概率为2000
    new = 0
    if game_point <= sum(prob[:1]):
        reward_text = draw_54star_weapon(5)
        color_ret = color[0]
    elif game_point <= sum(prob[:2]):
        reward_text, new = draw_SAstar_charc("S", up)
        color_ret = color[1]
    elif game_point <= sum(prob[:3]):
        reward_text = draw_54star_weapon(4)
        color_ret = color[2]
    elif game_point <= sum(prob[:4]):
        reward_text, new = draw_SAstar_charc("A")
        color_ret = color[3]
    elif game_point <= sum(prob[:5]):
        reward_text = add_material_book(1, 4)
        color_ret = color[4]
    elif game_point <= sum(prob[:6]):
        reward_text = add_material_book(2, 4)
        color_ret = color[5]
    elif game_point <= sum(prob[:7]):
        reward_text = add_material_book(1, 3)
        color_ret = color[6]
    elif game_point <= sum(prob[:8]):
        reward_text = add_material_book(2, 3)
        color_ret = color[7]
    elif game_point <= sum(prob[:9]):
        reward_text = add_material_book(1, 2)
        color_ret = color[8]
    elif game_point <= sum(prob[:10]):
        reward_text = add_material_book(2, 2)
        color_ret = color[9]
    #记录日志数据库
    now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) 
    insert_log_sql = "insert into log_lottery_charc(name, lottery_time, grade) values('" + \
                     reward_text + "','" + now_time + "'," + str(color_ret) \
                     + ")"
    cursor.execute(insert_log_sql)
    commitDB()
    #db.commit()     # 提交数据库
    return reward_text, color_ret, new

def draw_SAstar_charc(grade, up=""):
    """随机抽取A、S级星角色

    根据星级选择随机选择一名角色

    Args:
        grade: 获得新角色的星级
        up: 当前池子up角色

    Returns:
        ret[1]: 新角色名
        new:    1 - 新角色
                0 - 已拥有角色，增加碎片 
    """
    query_sql = "Select * from figure where grade=%s"
    cursor.execute(query_sql, [grade])
    all_5star = cursor.fetchall()
    ret = ""
    if up=="":
        ret = random.choice(all_5star)
    else:
        for charc in all_5star:                 #判断该角色存在
            if charc == up:
                if random.randint(1,5) <= 2:    #40%概率命中up池角色
                    ret = charc
        if ret=="":
            ret = random.choice(all_5star)
            print("未找到up角色")
    new = insert_upgrade_charc(ret)
    return ret[1], new

def insert_upgrade_charc(charc):
    """角色插入或者更新星级

    根据角色加入到my_weapon中

    Args:
        charc:  新角色的Figure对象

    Returns:
        new:    1 - 新角色
                0 - 已拥有角色，增加碎片
    """
    query_sql = "Select count(my_figure_name) from my_figure where my_figure_name = '" \
                + charc[1] + "'"
    cursor.execute(query_sql)
    count = cursor.fetchall()[0][0]

    if count==0:    #插入新角色
        insert_sql = "insert into my_figure(my_figure_name, level, love, moe, yxr, " + \
                     "intimacy, enthusiasm, skin, fragment, grade, exp) values('" + charc[1] \
                     + "','" +  str(charc[17]) + "','" + str(charc[16]) + "','" + \
                     str(charc[7]) + "','" + str(charc[8]) + "','" + str(charc[9]) + \
                     "','" + str(charc[10]) + "','" + charc[20] + "',0,'"+ charc[3] + \
                     "',0)"
        cursor.execute(insert_sql)
        new = 1
    elif count==1:  #为现有角色增加碎片
        frag_add = 30 if charc[3] == "S" else 18
        update_sql = "update my_figure set fragment = fragment + " + str(frag_add) + \
                     " where my_figure_name = '" + charc[1] + "'"
        cursor.execute(update_sql)
        new = 0
    commitDB()
    #db.commit()     # 提交数据库
    return new

def draw_54star_weapon(grade):
    """随机抽取5、4星武器

    根据星级选择随机选择一把武器加入到my_weapon中

    Args:
        grade: 获得新武器的星级

    Returns:
        ret[1]: 新武器名
    """
    query_sql = "Select * from weapon where grade=" + str(grade)
    cursor.execute(query_sql)
    all_weapon = cursor.fetchall()
    ret = random.choice(all_weapon)
    insert_weapon(ret)
    return ret[1]

def insert_weapon(weapon):
    """获得新武器插入数据库

    根据武器名加入到my_weapon中

    Args:
        weapon: 获得新武器的名称
    """
    insert_sql = "insert into my_weapon(name, level, moe, awaken) values('" + \
                 weapon[1] + "',1,'" + str(weapon[4]) + "',0)"
    cursor.execute(insert_sql)

def add_material_book(mob, level):
    """增加角色/武器升级材料

    4星强化料*(1-2) 4%        紫色
    4星角色书*(1-2) 8%        紫色
    3星强化料*(1-3) 10%       蓝色
    3星角色书*(1-3) 40%       蓝色
    2星强化料*(2-5) 4.5%      白色
    2星角色书*(2-5) 25%       白色

    Returns:
        ret: 增加物品的文字说明
    """
    #根据等级增加
    if level==4:
        number = random.randint(1,2)
    elif level==3:
        number = random.randint(1,3)
    elif level==2:
        number = random.randint(2,5)
    if mob==1:
        name = "星强化料"
    elif mob==2:
        name = "星角色书"

    insert_sql = "update knapsack set number = number+" + str(number) + \
                 " where name = '" + str(level) + name + "'"
    cursor.execute(insert_sql)
    commitDB()
    #db.commit()     # 提交数据库
    return str(level) + name + str(number) + "个"

def query_how_long_to_5star_charc():
    """查询77次保底剩余次数

    由于抽奖log的id是递增的，根据id即可查询离上一次5星出货相差了几次

    Returns:
        77 - (current_id - last_id): 剩余保底的次数
    """
    query_sql = "Select count(grade) from log_lottery_charc where grade=5"
    cursor.execute(query_sql)
    count = cursor.fetchall()[0][0]
    query_sql = "select max(log_id) from log_lottery_charc"     #查找当前抽奖id
    cursor.execute(query_sql)
    current_id = cursor.fetchall()[0][0]
    if current_id==None:
        current_id = 0
    #从未出现5星时
    if count==0:
        return 77 - current_id
    else:
        query_sql = "select max(log_id) from log_lottery_charc where grade=5"
        cursor.execute(query_sql)
        last_id = cursor.fetchall()[0][0]
        return 77 - (current_id - last_id)

def query_how_many_exp_books():
    """查询背包角色经验书数量

    Returns:
        quantity_4: 背包中4星角色书数量
        quantity_3: 背包中3星角色书数量
        quantity_2: 背包中2星角色书数量
    """
    query_sql = "select number from knapsack where FIND_IN_SET(id,'3,4,5')" 
    cursor.execute(query_sql)
    query_ret = cursor.fetchall()
    quantity_4, quantity_3, quantity_2 = query_ret[0][0], query_ret[1][0], query_ret[2][0]
    return quantity_4, quantity_3, quantity_2

def adventure_end_material_acquisition(stuff_drop_rate=1):
    """冒险结束后获取材料

    #   事件          概率      颜色
    # 100水晶         10/1500   橙色
    # 50水晶          20/1500   橙色
    # 记忆晶元        30/1500   橙色
    # 4星强化料*(1-2) 70/1500   紫色
    # 4星角色书*(1-2) 70/1500   紫色
    # 3星强化料*(1-3) 100/1500  蓝色
    # 3星角色书*(1-3) 100/1500  蓝色
    # 2星强化料*(2-5) 300/1500  白色
    # 2星角色书*(2-5) 300/1500  白色
    # 无              500/1500

    Args:
        stuff_drop_rate: 高品质材料加成

    Returns:
        reward_text: 获得的材料
        color_ret: 获取材料品质颜色
    """
    # 长度为10
    prob = [1000*stuff_drop_rate, 2000*stuff_drop_rate, 3000*stuff_drop_rate, 
            7000*stuff_drop_rate, 7000*stuff_drop_rate, 10000*stuff_drop_rate, 
            10000*stuff_drop_rate, 30000, 30000, 50000]
    #5 橙色   4 紫色    3 蓝色    2 白色
    color = [5, 5, 5, 4, 4, 3, 3, 2, 2, 2]
    # 判断奖励
    game_point = random.randint(1, 150000)            #debug测试修改lhhcxxg 概率为2000

    if game_point <= sum(prob[:1]):
        reward_text = "100水晶"
        color_ret = color[0]
    elif game_point <= sum(prob[:2]):
        reward_text = "50水晶"
        color_ret = color[1]
    elif game_point <= sum(prob[:3]):
        reward_text = "记忆晶元"
        add_memory_element(1)
        color_ret = color[2]
    elif game_point <= sum(prob[:4]):
        reward_text = add_material_book(1, 4)
        color_ret = color[3]
    elif game_point <= sum(prob[:5]):
        reward_text = add_material_book(2, 4)
        color_ret = color[4]
    elif game_point <= sum(prob[:6]):
        reward_text = add_material_book(1, 3)
        color_ret = color[5]
    elif game_point <= sum(prob[:7]):
        reward_text = add_material_book(2, 3)
        color_ret = color[6]
    elif game_point <= sum(prob[:8]):
        reward_text = add_material_book(1, 2)
        color_ret = color[7]
    elif game_point <= sum(prob[:9]):
        reward_text = add_material_book(2, 2)
        color_ret = color[8]
    elif game_point <= sum(prob[:10]):
        reward_text = ""
        color_ret = color[9]

    return reward_text, color_ret

def add_memory_element(number=0):
    """增加记忆晶元

    Args:
        number: 增加的数量
    """
    insert_sql = "update knapsack set number = number+" + str(number) + \
                 " where name = '记忆晶元'"
    cursor.execute(insert_sql)
    commitDB()
    #db.commit()     # 提交数据库

def mission_complete(num):
    """任务完成奖励

    Args:
        num: 完成的missionid
    """

    #水晶奖励类
    dic_cys = {1:20, 2:25, 3:10, 5:35, 6:20, 9:80, 16:120, 17:1000, 20:1000, 21:5000}
    update_sql = ""
    ret_sen = ""
    if num==4:
        update_sql = "update knapsack set number=number+1 where name='3星角色书'"
        ret_sen = "3星角色书*1"
    elif num==7:
        update_sql = "update knapsack set number=number+5 where name='3星强化料'"
        ret_sen = "3星强化料*5"
    elif num==8:
        update_sql = "update knapsack set number=number+1 where name='记忆晶元'"
        ret_sen = "记忆晶元*1"
    elif num==10 or num==11 or num==12:
        update_sql = "update knapsack set number=number+3 where name='4星角色书'"
        ret_sen = "4星角色书*3"
    elif num==13 or num==14 or num==15:
        update_sql = "update knapsack set number=number+3 where name='4星强化料'"
        ret_sen = "4星强化料*3"
    elif num==18:
        update_sql = "update knapsack set number=number+7 where name='4星角色书'"
        ret_sen = "4星角色书*7"
    elif num==19:
        update_sql = "update knapsack set number=number+5 where name='记忆晶元'"
        ret_sen = "记忆晶元*5"
    else:
        update_sql = "update lottery set lottery_crystal=lottery_crystal+" + str(dic_cys[num])
        ret_sen = str(dic_cys[num]) + "水晶"
    cursor.execute(update_sql)
    update_sql = "update mission set getreward=1 where missionid=" + str(num)
    cursor.execute(update_sql)
    commitDB()
    return ret_sen