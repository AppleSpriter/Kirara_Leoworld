import json

init_girl_list = [
    {'name': '高板桐乃', 'root': '我的妹妹哪有这么可爱', 'grade': 'S',
     'level': 1,  'weapon': 'none', 'sound': '竹达彩奈', 'skilllevel': 1,
     'love': 50, 'eyecolor': '蓝绿色', 'haircolor': '浅棕色'},
    {'name': '五更琉璃', 'root': '我的妹妹哪有这么可爱', 'grade': 'A',
     'level': 1, 'weapon': 'none', 'sound': '花泽香菜', 'skilllevel': 1,
     'love': 0, 'eyecolor': '蓝色', 'haircolor': '黑色'},
    {'name': '岁纳京子', 'root': '摇曳百合', 'grade': 'S', 'level': 1,
     'weapon': 'none', 'sound': '大坪由佳', 'skilllevel': 1,
     'love': 50, 'eyecolor': '蓝色', 'haircolor': '黄色'}
]



with open('GIRLS.txt', 'w') as file_object:
    json.dump(init_girl_list, file_object)