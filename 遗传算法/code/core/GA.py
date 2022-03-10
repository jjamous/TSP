# 利用遗传算法求解TSP问题
import matplotlib.pyplot as plt
import random
import math
import numpy as np
record_distance = []
class Life(object):
    """个体类"""

    def __init__(self, aGene=None):
        self.gene = aGene
        self.score = -1


class GA(object):
    """遗传算法类"""

    def __init__(self, aCrossRate, aMutationRage, aLifeCount, aGeneLenght, aMatchFun):
        self.croessRate = aCrossRate        # 交叉概率
        self.mutationRate = aMutationRage   # 突变概率
        self.lifeCount = aLifeCount         # 种群中个体数量
        self.geneLenght = aGeneLenght       # 基因长度
        self.matchFun = aMatchFun           # 适配函数
        self.lives = []                     # 种群
        self.best = None                    # 保存这一代中最好的个体
        self.generation = 1                 # 第几代
        self.crossCount = 0                 # 交叉计数
        self.mutationCount = 0              # 变异计数
        self.bounds = 0.0                   # 适配值之和，用于选择是计算概率
        self.mean = 1.0                     # 适配值平均值
        self.initPopulation()

    def initPopulation(self):
        """初始化种群"""
        self.lives = []
        for i in range(self.lifeCount):
            gene = [x for x in range(self.geneLenght)]
            random.shuffle(gene)  # 用来对一个元素序列进行重新随机排序
            life = Life(gene)
            self.lives.append(life)

    def judge(self):
        # 评估每一个个体的适应度
        self.bounds = 0.0
        self.best = self.lives[0]
        for life in self.lives:
            life.score = self.matchFun(life)
            self.bounds += life.score               # 每个个体的适应度是距离和倒数
            if self.best.score < life.score:
                self.best = life                    # 选出最佳适应度个体
        self.mean = self.bounds / self.lifeCount    # 计算平均个体适应度

    def cross(self, parent1, parent2, T=120, crossmode=2):
        # 交叉
        n = 0
        while 1:
            newGene = []
            if crossmode == 1:
                index = random.randint(0, self.geneLenght - 1)
                crossGene = parent2.gene[index:]
                for i in parent1.gene[:index]:
                    while i in crossGene:
                        i = parent1.gene[index:][crossGene.index(i)]
                    newGene.append(i)
                newGene.extend(crossGene)

            if crossmode == 2:
                index1 = random.randint(0, self.geneLenght - 1)  # 用于生成一个指定范围内的整数
                index2 = random.randint(index1, self.geneLenght - 1)
                tempGene = parent2.gene[index1:index2]  # 取p2交叉部分的基因片段
                # 新基因片段 = [p1原基因左片段 p2交叉部分 p1原基因右片段]
                p1len = 0
                for g in parent1.gene:
                    if p1len == index1:
                        newGene.extend(tempGene)  # p2交叉部分的基因片段直接成为新基因片段
                        p1len += 1
                    if g not in tempGene:
                        newGene.append(g)
                        p1len += 1

            # 直到选出比p1和p2适应度都高的新基因
            if (self.matchFun(Life(newGene)) > max(self.matchFun(parent1), self.matchFun(parent2))):
                self.crossCount += 1
                return newGene

            if (n > T):
                self.crossCount += 1
                return newGene
            n += 1

    def mutation(self, egg, mutationmoce=2):
        # 突变
        newGene = egg.gene[:]  # 产生一个新的基因序列，以免变异的时候影响父种群
        if mutationmoce == 1:  # 均匀变异
            for i in range(len(newGene)):
                if np.random.uniform() < self.mutationRate:
                    j = random.randint(0, self.geneLenght - 1)
                    newGene[i], newGene[j] = newGene[j], newGene[i]
        if mutationmoce == 2:  # 二元变异
            index1 = random.randint(0, self.geneLenght - 1)
            index2 = random.randint(0, self.geneLenght - 1)
            newGene[index1], newGene[index2] = newGene[index2], newGene[index1]  # 随机交换两个染色体
        if self.matchFun(Life(newGene)) > self.matchFun(egg):
            self.mutationCount += 1
            return newGene
        else:
            rate = random.random()
            if rate < math.exp(-10 / math.sqrt(self.generation)):
                self.mutationCount += 1
                return newGene
            return egg.gene

    def getOne(self):
        # 轮盘赌选择子代个体
        r = random.uniform(0, self.bounds)  # 均匀分布中随机采样
        for life in self.lives:
            r -= life.score
            if r <= 0:
                return life
        raise Exception("选择错误", self.bounds)

    def newChild(self):
        # 产生子代个体
        parent1 = self.getOne()     # 用适应度作为概率，轮盘赌选择
        rate = random.random()
        # 按概率交叉
        if rate < self.croessRate:  # 概率执行交叉互换
            # 交叉
            parent2 = self.getOne()
            gene = self.cross(parent1, parent2,crossmode=2)
        else:
            gene = parent1.gene     # 不交叉就直接返回根据适应度轮盘赌选择出来的个体

        # 按概率突变
        rate = random.random()
        if rate < self.mutationRate:
            gene = self.mutation(Life(gene))
        return Life(gene)

    def next(self):
        # 评估当前一代每一个个体的适应度
        self.judge()
        # 产生下一代
        newLives = []
        newLives.append(self.best)  # 把适应度最好的个体加入下一代
        while len(newLives) < self.lifeCount:
            newLives.append(self.newChild())
        self.lives = newLives
        self.generation += 1


class TSP(object):
    def __init__(self, aLifeCount=100,):
        self.initCitys()
        self.lifeCount = aLifeCount
        self.ga = GA(aCrossRate=0.7,
                     aMutationRage=0.02,
                     aLifeCount=self.lifeCount,
                     aGeneLenght=len(self.citys),
                     aMatchFun=self.matchFun())

    def initCitys(self):
        self.citys = []

        # 中国34个省会城市的经纬度坐标
        self.citys.append((116.46, 39.92))
        self.citys.append((117.2, 39.13))
        self.citys.append((121.48, 31.22))
        self.citys.append((106.54, 29.59))
        self.citys.append((91.11, 29.97))
        self.citys.append((87.68, 43.77))
        self.citys.append((106.27, 38.47))
        self.citys.append((111.65, 40.82))
        self.citys.append((108.33, 22.84))
        self.citys.append((126.63, 45.75))
        self.citys.append((125.35, 43.88))
        self.citys.append((123.38, 41.8))
        self.citys.append((114.48, 38.03))
        self.citys.append((112.53, 37.87))
        self.citys.append((101.74, 36.56))
        self.citys.append((117, 36.65))
        self.citys.append((113.6, 34.76))
        self.citys.append((118.78, 32.04))
        self.citys.append((117.27, 31.86))
        self.citys.append((120.19, 30.26))
        self.citys.append((119.3, 26.08))
        self.citys.append((115.89, 28.68))
        self.citys.append((113, 28.21))
        self.citys.append((114.31, 30.52))
        self.citys.append((113.23, 23.16))
        self.citys.append((121.5, 25.05))
        self.citys.append((110.35, 20.02))
        self.citys.append((103.73, 36.03))
        self.citys.append((108.95, 34.27))
        self.citys.append((104.06, 30.67))
        self.citys.append((106.71, 26.57))
        self.citys.append((102.73, 25.04))
        self.citys.append((114.1, 22.2))
        self.citys.append((113.33, 22.13))

    def distance(self, order):
        # 计算一个个体编码代表的哈密顿圈路径和
        distance = 0.0
        for i in range(-1, len(self.citys) - 1):
            index1, index2 = order[i], order[i + 1]
            city1, city2 = self.citys[index1], self.citys[index2]
            distance += math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)
        return distance

    def matchFun(self):
        return lambda life: 1.0 / self.distance(life.gene)

    def run(self, n=0,printprocess=True):
        while n > 0:
            self.ga.next()
            distance = self.distance(self.ga.best.gene)
            record_distance.append(distance)
            if printprocess:
                print(("Generation: %4d \t\t Distance: %f") % (self.ga.generation - 1, distance))  # 输出当前代数和路径长度
                print("Optimal path: ", self.ga.best.gene)
            n -= 1

if __name__ == '__main__':
    tsp = TSP()
    result=tsp.run(80)
    # 输出结果
    print(tsp.ga.crossCount,tsp.ga.mutationCount)  # 打印交叉互换和变异使得产生更高适应度个体的次数
    # 绘图
    plt.plot(record_distance)                      # 反映当前搜索到的最短距离的变化趋势
    plt.xlabel('iteration',fontsize=14)
    plt.ylabel('minimum distance',fontsize=14)
    plt.grid()
    plt.show()