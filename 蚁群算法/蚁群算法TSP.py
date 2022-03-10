import numpy as np
import random
import math
def getdata(num=3):
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
            ]  # ans=6656

def dis(node1, node2):
    node1 = np.array(node1)
    node2 = np.array(node2)
    return np.linalg.norm(node1 - node2)

def getdistancematrix(coord):
    n = len(coord)
    distance = np.zeros((n, n))  # 两点间最短距离矩阵
    for i in range(n):
        for j in range(n):
            distance[i, j] = dis(coord[i], coord[j])
    return distance

def RussianRoulette(posibilities):  # 注意不能到达的地方概率为0，轮盘赌一定不会选到
    cumposibilities = np.nancumsum(posibilities)
    tmp = np.where(cumposibilities >=np.random.uniform(low=0.0, high=1.0))[0]
    return tmp[0] if len(tmp) else len(posibilities)-1


def AntColony(coord,
              # 以下超参数常量初始化：
                m = 24,          # 蚂蚁数量，一般是城市数量的1~1.5倍
                alpha = 2,       # 信息素的量在指导蚂蚁搜索中的相对重要程度，[1,4]之间,值越大，则蚂蚁选择之前走过的路径可能性就越大，值越小，则蚁群搜索范围就会减少，容易陷入局部最优
                beta = 1,        # 启发式信息在指导蚂蚁搜索中的相对重要程度，[0,5]之间,值越大，收敛速度会越快，但容易选择局部较短路径，值越小，越接近随机搜索
                rho = 0.3,       # 信息素的挥发水平，[0.2,0.5],值越大，容易排除较优路径，值越小，各路径上信息素含量差别小收敛速度慢
                Q = 100,         # 蚂蚁留下的信息素常量，值越大，搜索范围小容易尽早收敛局部最优，值越小，每条路径信息素含量差别小容易陷入混沌状态
                iteration = 500  # 迭代次数，观察输出结果如果已经收敛就不用过多调整
              ):
    # 1.参数设置(常量初始化由参数传递)
    # 变量初始化
    n = len(coord)

    cnt = 0
    globalminima = 1e8
    globalpath = np.zeros(n)

    distanceMatrix = getdistancematrix(coord)
    pheromoneMatrix = np.ones((n, n))
    pathMatrix = np.zeros((m,n),dtype=np.int64)-1


    while 1:
        # 2.构建路径
        # 初始化位置
        pathMatrix[:,0] = np.array(random.sample([i for i in range(n)],m)) if m<=n else np.array([random.randint(0, n - 1) for i in range(m)])

        # 第k只蚂蚁从cur到next的概率
        localdistance = np.zeros(m)
        for k in range(m):
            possibility = np.zeros(n)
            for i in range(n-1):
                curpos = pathMatrix[k,i]
                for nextpos in range(n):
                    possibility[nextpos] = 0 if nextpos in pathMatrix[k] \
                        else math.pow(pheromoneMatrix[curpos,nextpos],alpha)/math.pow(distanceMatrix[curpos,nextpos],beta)
                possibility = possibility/sum(possibility)
                # 根据概率轮盘赌，确定下一个目标位置，便可求出距离
                pathMatrix[k,i+1] = RussianRoulette(possibility)
                localdistance[k]+=distanceMatrix[pathMatrix[k,i],pathMatrix[k,i+1]]
            localdistance[k] += distanceMatrix[pathMatrix[k, i + 1], pathMatrix[k,0]]  # 勿忘还有最后一段成回路

        # 3.更新信息素(完成一次路径循环后)
        # pheromoneMatrix = rho * pheromoneMatrix  先挥发rho
        # 根据pathMatrix所存轨迹计算新增的信息素
        info = np.zeros_like(pheromoneMatrix)
        for k in range(m):
            for i in range(n-1):
                info[pathMatrix[k,i],pathMatrix[k,i+1]]+=Q/localdistance[k]
                info[pathMatrix[k, i + 1], pathMatrix[k, i]] += Q / localdistance[k]  # 对称阵
            info[pathMatrix[k, i + 1], pathMatrix[k, 0]] += Q/localdistance[k]
            info[pathMatrix[k, 0], pathMatrix[k, i + 1]] += Q / localdistance[k]  # 对称阵
        pheromoneMatrix = pheromoneMatrix*(1-rho)+info

        # 4.迭代终止判断
        localshortest,localshortestpath = min(localdistance),pathMatrix[np.argmin(localdistance)]
        if globalminima>localshortest:
            globalminima = localshortest
            globalpath = localshortestpath
        if cnt<iteration:
            pathMatrix = np.zeros((m,n),dtype=np.int64)-1  # 每次循环唯一需要初始化的就是清空路径记录表，注意信息素是不停在更新的
            cnt+=1
            print(f'第{cnt}次迭代,平均距离:{np.mean(localdistance)},最短距离:{globalminima},最短路径:{globalpath}')
        else:
            return globalminima,globalpath

if __name__ == '__main__':
    coord = getdata(3)
    m = 24
    minimum_distance,minimum_path = AntColony(coord,m)
    print(f'm = {m}\nminimum distance = {minimum_distance}\nminimum path = {minimum_path}')