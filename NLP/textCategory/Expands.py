# -*- coding:utf-8 -*-

import random

'''
    扩展特征集，调用此脚本生成./keywords_intention_all.txt文件
'''

data = []
with open("./keywords_intention.txt", encoding="utf-8", errors="ignore") as fo:
    for line in fo.readlines():
        data.append(line.strip())
random.shuffle(data)    # 随机打乱

# for d in data:
#     print(d)

new_data = []
for d in data:
    for i in range(random.randint(4, 10)):
        # fo.writelines(d + "\n")
        new_data.append(d)
random.shuffle(new_data)

with open("./keywords_intention_all.txt", encoding="utf-8", errors="ignore", mode="w+") as fo:
    for d in new_data:
        fo.writelines(d + "\n")

print("finished")
