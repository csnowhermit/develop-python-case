import numpy as np


'''
    python图计算
'''

_ = float("inf")

dict = {}
dict["入口"] = 0
dict["丘陵"] = 1
dict["沼泽"] = 2
dict["河流"] = 3
dict["草地"] = 4
dict["出口"] = 5

# 入口，丘陵，沼泽，河流，草地，出口
map = [[_, 6, 3, _, _, _],
       [6, _, 2, 5, _, _],
       [3, 2, _, 3, 4, _],
       [_, 5, 3, _, 2, 3],
       [_, _, 4, 2, _, 5],
       [_, _, _, 3, 5, _]]

'''
    通过值找键值
'''
def get_key(value):
    k = [k for k, v in dict.items() if v==value]
    return k

# 1.找丘陵到沼泽有多远？
# print(map[get_key("丘陵")[0]][get_key(["沼泽"][0])])
# print(get_key("丘陵"))
# print(get_key("沼泽"))
print("丘陵-->沼泽的距离：", map[dict["丘陵"]][dict["沼泽"]])

# 2.丘陵到河流的距离
print("丘陵-->河流的距离：", map[dict["丘陵"]][dict["河流"]])

# 3.入口到出口的距离
print("入口-->出口的距离：", map[dict["入口"]][dict["出口"]])

# 4.从矩阵中找，丘陵之后能去哪里？
dest = map[dict["丘陵"]]
index = dict["丘陵"]
print(dest)
dest_cn = []
for i in range(len(dest)):
    if map[index][i] != _:
        dest_cn.append(get_key(i)[0])
print("丘陵之后能去哪里：", dest_cn)

# 5.从矩阵中找，哪里能到达河流？
print(type(map))
map = np.matrix(map)
print(type(map))
index = dict["河流"]
fromm = map[:, index]    # 得到哪些点能到达河流
dest_cn = []
for f in range(len(fromm)):
    # print(map[f, index], end=', ')
    if map[f, index] != _:
        dest_cn.append(get_key(f)[0])
print("哪里能到达河流：", dest_cn)

