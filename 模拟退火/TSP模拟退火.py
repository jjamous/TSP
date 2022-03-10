"旅行商问题 ( TSP , Traveling Salesman Problem )"
import numpy as np
import random
import matplotlib.pyplot as plt

# 变量准备
coordinates = np.array([[565.0, 575.0], [25.0, 185.0], [345.0, 750.0], [945.0, 685.0], [845.0, 655.0],
                        [880.0, 660.0], [25.0, 230.0], [525.0, 1000.0], [580.0, 1175.0], [650.0, 1130.0],
                        [1605.0, 620.0], [1220.0, 580.0], [1465.0, 200.0], [1530.0, 5.0], [845.0, 680.0],
                        [725.0, 370.0], [145.0, 665.0], [415.0, 635.0], [510.0, 875.0], [560.0, 365.0],
                        [300.0, 465.0], [520.0, 585.0], [480.0, 415.0], [835.0, 625.0], [975.0, 580.0],
                        [1215.0, 245.0], [1320.0, 315.0], [1250.0, 400.0], [660.0, 180.0], [410.0, 250.0],
                        [420.0, 555.0], [575.0, 665.0], [1150.0, 1160.0], [700.0, 580.0], [685.0, 595.0],
                        [685.0, 610.0], [770.0, 610.0], [795.0, 645.0], [720.0, 635.0], [760.0, 650.0],
                        [475.0, 960.0], [95.0, 260.0], [875.0, 920.0], [700.0, 500.0], [555.0, 815.0],
                        [830.0, 485.0], [1170.0, 65.0], [830.0, 610.0], [605.0, 625.0], [595.0, 360.0],
                        [1340.0, 725.0], [1740.0, 245.0]])
coordinates = np.array(
[
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
            ])


def initparameter():  # 初始化参数
    alpha = 0.99
    T_range = (1, 100)
    markovlen = 1000
    return alpha, T_range, markovlen


alpha, (T_low, T_high), markovlen = initparameter()


def TravelingSalesmanProblem(
        coordinates,
        alpha=alpha,
        T_low=T_low,  # 收敛条件
        T_high=T_high,  # 初值
        markovlen=markovlen
):
    def getdistmat(coordinates):  # 得到距离矩阵的函数
        n = coordinates.shape[0]  # n个坐标点
        distmat = np.zeros((n, n))  # n×n距离矩阵
        for i in range(n):
            for j in range(i, n):
                distmat[i][j] = distmat[j][i] = np.linalg.norm(coordinates[i] - coordinates[j])
        return distmat

    inf = 1e6
    n = coordinates.shape[0]
    t = T_high  # 开始设最高温度
    distmat = getdistmat(coordinates)  # 得到距离矩阵
    solutionnew = np.arange(n)
    solutioncurrent = solutionnew.copy()
    solutionbest = solutionnew.copy()
    valuecurrent = inf
    valuebest = inf
    result = []  # 记录迭代过程中的最优解
    while t > T_low:  # 这里用最低温度作为收敛条件，也可以用相邻5个温度下bestvalue的方差作为收敛条件
        for i in range(markovlen):  # 在一个温度下要重复markovlen次
            # 产生新解:常用两交换法或三交换法
            if np.random.rand() > 0.5:  # 两交换:交换u和v
                loc1, loc2 = sorted(random.sample(range(n), 2))
                solutionnew[loc1], solutionnew[loc2] = solutionnew[loc2], solutionnew[loc1]
            else:  # 三交换:任选序号u,v和ω(u≤v≤ω)，将u和v之间的路径插到ω之后访问
                loc1, loc2, loc3 = sorted(random.sample(range(n), 3))
                # 将[loc1,loc2)区间的数据插入到loc3之后
                tmplist = solutionnew[loc1:loc2].copy()
                solutionnew[loc1:loc3 - loc2 + 1 + loc1] = solutionnew[loc2:loc3 + 1].copy()
                solutionnew[loc3 - loc2 + 1 + loc1:loc3 + 1] = tmplist.copy()

            valuenew = 0
            for i in range(n - 1):
                valuenew += distmat[solutionnew[i]][solutionnew[i + 1]]
            valuenew += distmat[solutionnew[0]][solutionnew[n - 1]]  # 勿忘首尾！
            if valuenew < valuecurrent:  # 接受该解
                valuecurrent = valuenew
                solutioncurrent = solutionnew.copy()
                if valuenew < valuebest:  # 维护最优
                    valuebest = valuenew
                    solutionbest = solutionnew.copy()
            else:  # 按Metropolis接受准则
                if np.random.rand() < np.exp(-(valuenew - valuecurrent) / t):
                    valuecurrent = valuenew
                    solutioncurrent = solutionnew.copy()
                else:
                    solutionnew = solutioncurrent.copy()  # 没保存valuecurrent，即不接受该solution算出的距离
        t *= alpha  # 降温
        result.append(valuebest)  # 收集每个温度下的当前最小距离
        print(t)  # 监视程序进展速度

    # 可视化显示：随着温度不断降低,启发式找到的最短距离越来越小
    plt.plot(np.array(result))
    plt.ylabel("bestvalue")
    plt.xlabel("T")
    plt.show()

    return min(result),solutionbest


bestvalue,bestsolution = TravelingSalesmanProblem(coordinates, alpha, T_low, T_high, markovlen)
print('最短距离：',bestvalue)
print('路径：',bestsolution)
