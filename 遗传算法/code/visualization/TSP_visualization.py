import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from GA import TSP
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

'''初始化'''
class Visulization():
    def __init__(self,path):
        self.path=path
        # 坐标信息
        self._locations = [(116.46, 39.92), (117.2, 39.13), (121.48, 31.22), (106.54, 29.59), (91.11, 29.97), (87.68, 43.77),
                  (106.27, 38.47), (111.65, 40.82), (108.33, 22.84), (126.63, 45.75), (125.35, 43.88), (123.38, 41.8),
                  (114.48, 38.03), (112.53, 37.87), (101.74, 36.56), (117.0, 36.65), (113.6, 34.76), (118.78, 32.04),
                  (117.27, 31.86), (120.19, 30.26), (119.3, 26.08), (115.89, 28.68), (113.0, 28.21), (114.31, 30.52),
                  (113.23, 23.16), (121.5, 25.05), (110.35, 20.02), (103.73, 36.03), (108.95, 34.27), (104.06, 30.67),
                  (106.71, 26.57), (102.73, 25.04), (114.1, 22.2), (113.33, 22.13)]# _locations:34个省市坐标，p1、p2是34个经纬度
        self.places = ['北京','天津','上海','重庆','拉萨','乌鲁木齐','银川','呼和浩特','南宁','哈尔滨','长春','沈阳','石家庄','太原','西宁','济南','郑州','南京','合肥','杭州','福州','南昌','长沙','武汉','广州','台北','海口','兰州','西安','成都','贵阳','昆明','香港','澳门']
        self.p1 = [l[0] for l in self._locations]
        self.p2 = [l[1] for l in self._locations]
        self.num = len(self._locations)+1
        # 绘图
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.xdata, self.ydata = [], []  # 初始化两个数组
        self.ln, = self.ax.plot([], [], 'c-',linewidth=2, animated=True)  # 第三个参数表示画曲线的颜色和线型
        self.cnt = 0  # 已经绘图个数
        self.ani =None
    def init(self):
        self.ax.set_xlim(85, 130)  # 设置x轴的范围pi代表3.14...圆周率，
        self.ax.set_ylim(17, 50)  # 设置y轴的范围
        plt.xticks(fontsize = 18)
        plt.yticks(fontsize = 18)
        plt.xlabel('longitude\n',fontsize = 18)
        plt.ylabel('latitude\n',fontsize = 18)
        self.ax.plot(self.p1, self.p2, 'ro', ms=8)
        for i in range(self.num-1):
            plt.text(self.p1[i]-1.4, self.p2[i]-1.4,f'{i+1}', weight="bold", color="k",size=18,alpha=0.9)
        plt.title('全国34个省市TSP问题求解可视化动图\n',fontsize=22,fontweight='semibold',verticalalignment='top',horizontalalignment='center')
        self.ax.grid(True)  # 画网格线
        return self.ln,  # 返回曲线

    def update(self,n):
        self.xdata.append(self._locations[self.path[n]][0])
        self.ydata.append(self._locations[self.path[n]][1])
        self.ln.set_data(self.xdata, self.ydata)  # 重新设置曲线的值
        self.cnt += 1
        return self.ln,

    def visulize(self):
        self.ani = FuncAnimation(fig=self.fig,
                            func=self.update,
                            frames=self.num,       # 一次循环包含的帧数,这里的frames在调用update函数是会将frames作为实参传递给“n”
                            init_func=self.init,  # 自定义开始帧
                            blit=True,       # 仅更新产生变化的点
                            interval=200,    # 更新频率，以ms计
                            # fargs=cnt,       # update传入的第二参数
                            )
        self.ani.save('TSP.gif')



if __name__ == '__main__':
    tsp = TSP()
    tsp.run(100)
    mindistance = tsp.distance(tsp.ga.best.gene)
    path = tsp.ga.best.gene + [tsp.ga.best.gene[0]]
    v = Visulization(path)
    print('--------------------------------------------------------------------------------------------------------------------------')
    print(f'最短路径如下：')
    for i in range(len(path)):
        if i != len(path)-1:
            print(f'{v.places[path[i]]}->',end='')
        else:
            print(v.places[path[i]])
    print(f'最短距离和：{mindistance}')
    v.visulize()  # 保存gif动图

