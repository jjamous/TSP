import numpy as np

# 无向完全图：计算两点间的距离，即最短距离
def dis(node1, node2):
    node1 = np.array(node1)
    node2 = np.array(node2)
    return np.linalg.norm(node1 - node2)


# 有向图：Floyd多源最短距离
def Floyd(distance):
    n = len(distance)
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if distance[i, j] > distance[i, k] + distance[k, j]:
                    distance[i, j] = distance[i, k] + distance[k, j]


def TravelingSalesmanPromblem(coord):  # 这里输入每个城市的坐标点
    n = len(coord)  # 节点数
    inf = 1e6  # ∞
    num = 1 << (n - 1)  # 除起始点外(n - 1)个元素能产生2^(n-1)个子集
    def getdistancematrix():
        distance = np.zeros((n, n))  # 两点间最短距离矩阵
        for i in range(n):
            for j in range(n):
                distance[i, j] = dis(coord[i], coord[j])
        return distance
    distance = getdistancematrix()
    d = np.zeros((n, num))  # d(i, V’)表示从顶点i出发经过V’中各个顶点一次且仅一次，最后回到出发点s的最短路径长度
    d = d + inf  # 为min做准备
    # 思路：从左往右一列一列填完d表(遇上自环就不填),d[0, num - 1]即是最短距离
    # 1)第一列V’是空集，直接用两点间最短距离矩阵的第一列代替,起点0所在行一定会产生自环所以填inf
    d[1:, 0] = distance[1:, 0]

    # 2)从第二列开始，用之前得到的信息填出剩余部分
    # ①k位于二进制数的第k位：(S >> (k - 1)) & 1
    # ②删除顶点k: S ^ (1 << (k - 1))
    for state in range(1, num - 1):  # 0列已初值，从1列~2^(n-1)-2列循环,[0,2^(n-1)-1]为结果
        for node in range(1, n):  # 起始点0行因为自环不考虑，从结点1~结点n-1
            if (state >> (node - 1)) & 1:
                continue
            for k in range(1, n):  # 循环state中的n-1位状态
                if (state >> (k - 1)) & 1:
                    d[node, state] = min(
                        d[node, state],
                        distance[node, k] + d[k, state ^ (1 << (k - 1))]  # 状态转移方程
                    )

    # 3)获得d[0,2^(n-1)-1]处的最短距离（单独写是因为之前的循环中为避免右移负位数跳过了0行）
    node,state = 0,num-1
    for k in range(1, n):  # 循环state中的n-1位状态
        if (state >> (k - 1)) & 1:
            d[node, state] = min(
                d[node, state],
                distance[node, k] + d[k, state ^ (1 << (k - 1))]  # 状态转移方程
            )
    # 查看结果
    def output(d):
        for i in range(len(d)):
            for j in range(len(d[0])):
                if d[i, j]==inf:
                    print('INF', end='  ')
                else:
                    print("%.1f" % d[i, j], end='  ')
            print()
    # output(d)  # 注意这里输出仅保留1位小数
    return d[0,num-1]

def getdata(num=2):
    if num==1:
        return [[0, 0], [5, 0], [2, 4], [4, 3]]  # ans=14.87
    elif num==2:
        return [
            [38.24,20.42],
            [39.57,26.15],
            [40.56,25.32],
            [36.26,23.12],
            [33.48,10.54],
            [37.56,12.19],
            [38.42,13.11],
            [37.52,20.44],
            [41.23,9.1],
            [41.17,13.05],
            [36.08,-5.21],
            [38.47,15.13],
            [38.15,15.35],
            [37.51,15.17],
            [35.49,14.32],
            [39.36,19.56]
                ]  # ans=73.99
    else:
        return [
                [11003.611100, 42102.500000],
                [11108.611100, 42373.888900],
                [11133.333300, 42885.833300],
                [11155.833300, 42712.500000],
                [11183.333300, 42933.333300],
                [11297.500000, 42853.333300],
                [11310.277800, 42929.444400],
                [11416.666700, 42983.333300],
                [11423.888900, 43000.277800],
                [11438.333300, 42057.222200],
                [11461.111100, 43252.777800],
                [11485.555600, 43187.222200],
                [11503.055600, 42855.277800],
                [11511.388900, 42106.388900],
                [11522.222200, 42841.944400],
                [11569.444400, 43136.666700],
                [11583.333300, 43150.000000],
                [11595.000000, 43148.055600],
                [11600.000000, 43150.000000],
                [11690.555600, 42686.666700],
                [11715.833300, 41836.111100],
                [11751.111100, 42814.444400],
                [11770.277800, 42651.944400],
                [11785.277800, 42884.444400],
                [11822.777800, 42673.611100],
                [11846.944400, 42660.555600],
                [11963.055600, 43290.555600],
                [11973.055600, 43026.111100],
                [12058.333300, 42195.555600],
                [12149.444400, 42477.500000],
                [12286.944400, 43355.555600],
                [12300.000000, 42433.333300],
                [12355.833300, 43156.388900],
                [12363.333300, 43189.166700],
                [12372.777800, 42711.388900],
                [12386.666700, 43334.722200],
                [12421.666700, 42895.555600],
                [12645.000000, 42973.333300]
            ]  # ans=6656，MemoryError需启发式搜索


coord=getdata(num=2)
# 注：这里仅求解最小值，没有打印路线
print('TSP最短距离：',TravelingSalesmanPromblem(coord))
