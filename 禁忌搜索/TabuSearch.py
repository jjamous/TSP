# https://wenku.baidu.com/view/7b27e6e881c758f5f61f67f0.html
# https://blog.csdn.net/zuochao_2013/article/details/72292466

import numpy as np
import random
import math
from scipy.spatial.distance import cdist  # 用来构建距离矩阵：元素表示从任意i到j的距离
from scipy.spatial.distance import pdist  # 用来构建一个坐标列表两两距离，输出列表长度comb(n,2)
from scipy.special import comb  # 组合数
from itertools import permutations  # 生成一个全排列的迭代器
from MyQueue import MyQueue  # 定长队列

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
            ]  # ans=6656
def dis(A,B):
    return math.sqrt(sum(np.square(np.array(A)-np.array(B))))
def evaluate(path):
    length = len(path)
    res = dis(coord[path[length-1]],coord[path[0]])
    for i in range(length-1):
        res += dis(coord[path[i]],coord[path[i+1]])
    return res
def findneighbor(path,k,rule = 3):
    neighbor = np.tile(path,(k,1))  # 按自定义size复制向量
    for i in range(k):
        if rule == 2:
            s0, s1 = random.sample(np.arange(n).tolist(), rule)
            neighbor[i,s0],neighbor[i,s1] = neighbor[i,s1],neighbor[i,s0]
        if rule == 3:
            s0, s1,s2 = random.sample(np.arange(n).tolist(), rule)
            neighbor[i, s0], neighbor[i, s1], neighbor[i, s2] = neighbor[i, s2], neighbor[i, s0], neighbor[i, s1]
        neighbor[i] = tuple(neighbor[i])
    return neighbor
def TabuSearch(
        # coord为全局变量
        tabusize = None,       # 禁忌表长，默认sqrt(comb(n,2))，与数据量挂钩
        candidatesize = None,  # 候选新解个数，与数据量挂钩,大了会减慢运算速度
        iteration = 500,       # 迭代次数
        ):
    globalminima = 1e6
    globalminpath = np.zeros(n)
    if tabusize == None:
        tabusize = round(comb(n,2)**0.5)
    if candidatesize == None:
        candidatesize = n*n
    Q = MyQueue(maxlength=tabusize)

    # 随机构建初值
    path0 = random.sample(np.arange(n).tolist(), n)
    curpath = path0
    for _ in range(iteration):
        # 在邻域中找出k个新解
        neighbors = findneighbor(curpath, candidatesize)
        neighbors = set([tuple(each) for each in neighbors])  # 去重
        sortedneighbors = sorted(neighbors,key=lambda x:evaluate(x),reverse=False)
        for neighbor in sortedneighbors:
            # 如果距离小于globalminima，不管有没有在禁忌表内破禁加入
            tmpdistance = evaluate(neighbor)
            if tmpdistance<globalminima:
                globalminima = tmpdistance
                globalminpath = neighbor
                break
            # 如果没有在禁忌表内，加入（可能接纳更差解）
            elif not Q.exist(neighbor):
                break
        Q.add(neighbor)
        curpath = neighbor
        print(evaluate(curpath))

    return globalminpath,globalminima
if __name__ == '__main__':
    coord = getdata()
    n = len(coord)  # 两个全局变量
    globalminpath,globalminima = TabuSearch()
    print(f"最短距离{globalminima}\n最短路径{globalminpath}")