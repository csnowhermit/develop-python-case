
'''
    最短路径算法：Dijkstra迪杰斯特拉算法
    需求：从入口到出口，最短路径
'''

#定义不可达距离
_ = float('inf')

'''
    输入边关系手动构造map图
'''
def createmap():
    a, b = input("输入节点数和边数：").split()
    n = int(a)
    m = int(b)
    map = [[_ for i in range(n + 1)] for j in range(n + 1)]
    for i in range(m + 1):
        x, y, z = input("输入两边和长度：").split()
        point = int(x)
        edge = int(y)
        map[point][edge] = float(z)
        map[edge][point] = float(z)
    s, e = input("输入起点和终点：").split()
    start = int(s)
    end = int(e)
    dis, road = Dijkstra(n, m, map, start, end)
    print("最短距离：", dis)
    print("最短路径：", road)

def map():
    # 入口，丘陵，沼泽，河流，草地，出口
    map = [[_, 6, 3, _, _, _],
           [6, _, 2, 5, _, _],
           [3, 2, _, 3, 4, _],
           [_, 5, 3, _, 2, 3],
           [_, _, 4, 2, _, 5],
           [_, _, _, 3, 5, _]]

    s, e = input("输入起点和终点：").split()
    dis, road = Dijkstra(5, 8, map, int(s), int(e))
    print("最短距离：", dis)
    print("最长距离：", road)


'''
    Dijkstra算法：求最短路径
    :param points: 点个数
    :param edges: 边个数
    :param graph: 图
    :param start: 起点
    :param end: 终点
'''
def Dijkstra(points, edges, graph, start, end):
    # 各变量初始化
    map = [[_ for i in range(points + 1)] for j in range(points + 1)]
    pre = [0] * (points + 1)    # 记录先驱
    vis = [0] * (points + 1)    # 记录节点遍历状态
    dis = [_ for i in range(points + 1)]    # 保存最短距离
    road = [0] * (points + 1)   # 保存最短路径
    roads = []

    map = graph

    # 初始化起点到其他点的距离
    for i in range(points + 1):
        if i == start:
            dis[i] = 0
        else:
            dis[i] = map[start][i]

        # 如果两点间有连线，说明有路
        if map[start][i] != _:
            pre[i] = start
        else:
            pre[i] = -1

    vis[start] = 1
    for i in range(points + 1):    # 每循环一次确定一条最短路径
        min = _
        for j in range(points + 1):    # 寻找当前最短路
            if vis[j] == 0 and dis[j] < min:
                t = j
                min = dis[j]
        vis[t] = 1    # 找到最短的一条路径，标记
        for j in range(points + 1):
            if vis[j] == 0 and dis[j] > dis[t] + map[t][j]:
                dis[j] = dis[t] + map[t][j]
                pre[j] = t
    p = end
    len = 0
    while p >= 1 and len < points:
        road[len] = p
        p = pre[p]
        len += 1
    mark = 0
    len -= -1
    while len >= 0:
        roads.append(road[len])
        len -= 1
    return dis[end], roads

if __name__ == '__main__':
    map()