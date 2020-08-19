import json

work_list = [
    {'name': '我的妹妹哪有这么可爱', 'year': '2010', 'company': 'AIC'},
    {'name': '轻音少女', 'year': '2010', 'company': 'Kyoto Animation'},
    {'name': '野良神', 'year': '2014', 'company': 'Bones'},
    {'name': '中二病也要谈恋爱', 'year': '2014', 'company': 'Kyoto Animation'},
    {'name': '冰菓', 'year': '2012', 'company': 'Kyoto Animation'},
    {'name': '吹响吧！上低音号', 'year': '2015', 'company': 'Kyoto Animation'},
    {'name': '珈百璃的堕落', 'year': '2016', 'company': 'Animation Studio'},
    {'name': 'New Game!', 'year': '2016', 'company': 'Animation Studio'},
    {'name': 'New Game!!', 'year': '2017', 'company': 'Animation Studio'}
]

with open('WORKS.txt', 'w') as file_object:
    json.dump(work_list, file_object)