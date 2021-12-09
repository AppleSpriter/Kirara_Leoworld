'''
本文件储存一些通用计算公式

注释规范:
    """函数作用

    详细说明；需要注意的用法

    Args:
        输入参数

    Returns:
        返回值

    Raises:
        抛出的异常
    """

'''
import sys
def formula_level_exp_limit(level):
    """根据等级计算当前等级对应的经验值上限

    当前等级大于80时，达到满级，返回0

    Args:
        level: 当前等级

    Returns:
        exp_limit: 经验值上限
    """
    exp_limit = 10
    if level==1:
        return exp_limit
    elif level==80:
        return 0
    for i in range(2, level):
        exp_limit = int(exp_limit*1.1)
    return exp_limit

def formula_grade_fragment_limit(grade):
    """根据品质计算碎片上限

    Args:
        grade: 角色品质/阶级

    Returns:
        grade_dict[grade]: 当前角色品质对应的碎片上限
    """
    grade_dict = {"A":30, "S":100, "SS":200, "SSS":300, "EX":sys.maxsize}
    return grade_dict[grade]

def formula_grade_four_dismension_limit(grade):
    """根据品质计算四维加成

    Args:
        grade: 角色品质/阶级

    Returns:
        grade_dict[grade]: 当前角色品质对应的四维属性加成
    """
    grade_dict = {"A":0, "S":108, "SS":180, "SSS":252, "EX":360}
    return grade_dict[grade]

def formula_grade_love_limit(grade):
    """根据品质计算好感度上限

    Args:
        grade: 角色品质/阶级

    Returns:
        grade_love_dict[grade]: 当前角色品质对应的好感度上限
    """
    grade_love_dict = {"A":50, "S":200, "SS":500, "SSS":1000, "EX":2000}
    return grade_love_dict[grade]

def formula_four_dismension_add(basic, coefficient, grade, level, passive=0):
    """根据四维属性、经验值、品质、被动计算四维加成

    换算公式 y=basic+level^2*0.05*coefficient+grade*coefficient+passive
    
    Args:
        basic: 角色基础属性
        coefficient: 角色属性提升系数
        grade: 角色品质/阶级
        level: 角色的等级
        passive: 角色特性的被动加成比例*1000的值

    Returns:
        add: 增加的比例
    """
    add = basic + level*level*coefficient*0.05 + \
        formula_grade_four_dismension_limit(grade)*coefficient + passive
    return int(add)

def formula_get_str_byte_len(word):
    """计算显示字符串长度

    Args:
        word: 需要计算的字符串

    Returns:
        ret: 字符串长度，中文为1，其他字符串为0.5
    """
    ret = 0
    for s in word:
        if '\u4e00' <= s <= '\u9fff':
            ret += 2
        else:
            ret += 1
    return ret/2

def formula_str_to_interval_list(string, interval):
    """字符串根据间隔分离成多个子串

    函数用于长文字自动换行的显示，例如：角色特性说明

    Args:
        string: 需要分割的字符串
        interval: 间隔

    Returns:
        ret_list: 分割后的子串列表
    """
    string_len = int(formula_get_str_byte_len(string) * 2)
    ret_list = [string[i:i+interval] for i in range(0, string_len, interval)]
    return ret_list

def formula_grade_up(before_grade):
    """提升一级当前品质/升阶操作

    Args:
        before_grade: 提升前的品质

    Returns:
        gradeUp_dict[before_grade]: 提升一阶后的品质
    """
    gradeUp_dict = {"A":"S", "S":"SS", "SS":"SSS", "SSS":"EX"}
    return gradeUp_dict[before_grade]

def formula_levelUp_with_expbook(level, before_exp, quantity_4=0, quantity_3=0, quantity_2=0):
    """角色升级计算

    根据消耗经验书的数量以及现在的等级经验，计算消耗后的等级经验

    Args:
        level: 升级前的等级
        before_exp: 升级前的经验值
        quantity_4: 4级角色书的数量
        quantity_3: 3级角色书的数量
        quantity_2: 2级角色书的数量

    Returns:
        ret_1: 升级之后的等级
        ret_2: 升级之后的经验值
    """
    exp_book_dict = {4:1200, 3:400, 2:100}
    exp_all = quantity_4*exp_book_dict[4] + quantity_3*exp_book_dict[3] + \
              quantity_2*exp_book_dict[2]
    while(1):
        if level==80:   
            return 80, 0    #满级时返回0exp
        exp_limit = formula_level_exp_limit(level)
        if exp_all < (exp_limit - before_exp):      #如果经验未超过当前等级上限
            return level, before_exp + exp_all
        else:
            exp_all -= exp_limit
            level += 1
            before_exp = 0

def formula_format_add0(word, number=3):
    """添加0的操作

    根据给与的数字

    Args:
        word: 需要加0的字符串
        number: 加完之后变为多少位

    Returns:
        word: format加0后的字符串
    """
    while(number>=len(word)):
        number -= 1
        word = "0" + word
    return word

def formula_weapon_awaken_value(weapon):
    """根据武器的突破返回对应属性值

    Args:
        weapon: 武器对象

    Returns:
        value: 对应的属性值
    """
    if weapon.awaken==0:
        return weapon.value1
    elif weapon.awaken==1:
        return weapon.value2
    elif weapon.awaken==2:
        return weapon.value3
    elif weapon.awaken==3:
        return weapon.value4
    elif weapon.awaken==4:
        return weapon.value5
    else:
        return 0