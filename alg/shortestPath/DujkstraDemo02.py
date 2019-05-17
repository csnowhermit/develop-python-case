import numpy as np

'''
    Dijkstra最短路径算法
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

'''
    当前节点之后能去哪里
'''
def toWhere(source):
    dest = map[dict[source]]
    index = dict[source]
    dest_cn = []
    for i in range(len(dest)):
        if map[index][i] != _:
            dest_cn.append(get_key(i)[0])
    return dest_cn

'''
    Dijkstra算法：
    :param map: 图
    :param start: 开始节点名称 
    :param end: 结束节点名称
'''
def Dijkstra(map, start, end):
    start = dict[start]
    end = dict[end]
    map = np.matrix(map)

    U = [k for k, v in dict.items()]    # 未遍历的节点
    points = len(U)    # 节点个数
    pre = [_ for i in range(points)]      # 相应位置表示每一个节点的前一个节点
    vis = [0 for i in range(points)]      # 记录节点遍历状态：0表示未遍历，1表示已遍历
    road = [0 for i in range(points)]     # 保存最短距离
    dis = [_ for i in range(points)]      # 从start点到所有点的长度

    # 整理从start点到所有点的长度
    for i in range(points):
        if i == start:
            dis[i] = 0
        else:
            dis[i] = map[start, i]

        if map[start, i] != _:    # 如果两点有连线，说明有路
            pre[i] = start
        else:
            pre[i] = -1
    print(dis)
    print(pre)

    vis[start] = 1    # 从start节点开始遍历
    for i in range(points):
        min = _    # 最短路径
        for j in range(points):
            # print("i：", i, ", j：", j, get_key(i), "-->", get_key(j), " 的距离为：", dis[j], min)
            if vis[j] == 0 and dis[j] < min:    # 如果当前节点没走过，且从起始点到当前点的距离小于min
                t = j         # 记录下当前的节点索引
                min = dis[j]
        vis[t] = 1    # 表示最短路径的节点被遍历过
        for j in range(points):
            if vis[j] == 0 and dis[j] > dis[t] + map[t, j]:
                dis[j] = dis[t] + map[t, j]
                pre[j] = t
    print("调整后：")
    print(dis)
    print(pre)

    # 将pre反转并从后往前对应节点输出，并除去初始点
    p = end
    leng = 0
    while p >= 1 and leng < points:
        road[leng] = p
        p = pre[p]
        leng += 1
    print("pre反转并对应节点输出：", road)

    # mark = 0
    # leng -= 1
    # while leng >= 0:
    #     roads.append(road[leng])
    #     leng -= 1
    roads = list(reversed(road))    # 将从后往前反转的list再次反转过来，形成真实的路线
    return dis[end], roads

def main():
    dis, roads = Dijkstra(map, "入口", "出口")
    print("最短距离：", dis)
    print(type(roads))
    print("最短路径：", roads)

    roads_cn = []
    print("Details：")
    for r in roads:
        roads_cn.append(get_key(r)[0])
    print(roads_cn)

if __name__ == '__main__':
    main()