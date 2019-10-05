'''
Author = Leo
Date = 19.10.04
Description = 用来学习入门书籍
'''


filename = "pi_million.txt"
with open(filename) as file_object:
    lines = file_object.readlines()

pi_string = ''
for line in lines:
    pi_string += line.strip()

rs = pi_string.find("120372")

if rs == -1:
    print("sorry")
else:
    print("Your birthday appears in " + str(rs) + " position")




