clc,clear;
%% 求目标函数最大值（最小值记得负号转化！）
targetfunction = @(x)-(10 + x(1) ^ 2 + x(2) ^ 2 - 10 * (cos(2 * pi * x(1)) + cos(2 * pi * x(2))));% 最大值-10
dimension = 2;
popmin=[-2,-2];      % 自变量lb,粒子位置范围下界
popmax=[2,2];        % 自变量ub,粒子位置范围上界
Vmin=[-0.5,-0.5];    % 粒子最小运动速度,要调试
Vmax=[0.5,0.5];      % 粒子最大运动速度,要调试
w=1;                 % 惯性因子,值较大，全局寻优能力强；值较小，局部寻优能力强
c1=1.5;              % 个体学习因子,重要调参对象！
c2=1.5;              % 社会学习因子,重要调参对象！
sizepop=20;          % 种群population规模
maxgen = 300;        % 进化次数  
%% 别忘多运行几次找最大值
[fitnesszbest,zbest] = PSO(targetfunction,dimension,popmin,popmax,Vmin,Vmax,w,c1,c2,sizepop,maxgen);
disp(['目标函数最大值:',num2str(fitnesszbest)]);
disp(['目标函数最大值点:',num2str(zbest)]);
