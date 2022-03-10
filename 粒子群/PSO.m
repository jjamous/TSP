function [fitnesszbest,zbest] = PSO(targetfunction,dimension,popmin,popmax,Vmin,Vmax,w,c1,c2,sizepop,maxgen)
%% 函数文档
% targetfunction ：目标函数，形式f(x),注意求的是最大值，最小值要负号转化
% dimension      ：自变量x的维度
% popmin         ：x的lb
% popmax         ：x的ub
% Vmin           ：粒子最小运动速度
% Vmax           ：粒子最大运动速度
% w              ：惯性因子，值较大，全局寻优能力强；值较小，局部寻优能力强
% C1/C2          ：加速常数，C1为粒子的个体学习因子，C2为粒子的社会学习因子，一般c1=c2=2，一般C1 = C2 ∈[0,4]
% sizepop        ：粒子数量，这里默认20
% maxgen         ：进化迭代次数，这里默认300
%% 产生初始粒子和速度
for i=1:sizepop
    for j=1:dimension
        %随机产生一个种群
        pop(i,j)=(popmax(j)-popmin(j))*rand+popmin(j);    %初始种群
        V(i,j)=(Vmax(j)-Vmin(j))*rand+Vmin(j);  %初始化速度
    end
    %计算适应度
    fitness(i)=targetfunction(pop(i,:));   %染色体的适应度
end

%% 个体极值和群体极值
[bestfitness,bestindex]=max(fitness);
zbest=pop(bestindex,:);   %全局最佳
gbest=pop;    %个体最佳
fitnessgbest=fitness;   %个体最佳适应度值
fitnesszbest=bestfitness;   %全局最佳适应度值

%% 迭代寻优
for i=1:maxgen
    for j=1:sizepop 
        %速度更新
        V(j,:) = w*V(j,:) + c1*rand*(gbest(j,:) - pop(j,:)) + c2*rand*(zbest - pop(j,:));
        for k = 1:dimension
            if V(j,k)>Vmax(k)
                V(j,k) = Vmax(k);
            end
        end
        for k = 1:dimension
            if V(j,k)<Vmin(k)
                V(j,k) = Vmin(k);
            end
        end
        %种群更新
        pop(j,:)=pop(j,:)+V(j,:);
        for k = 1:dimension
            if pop(j,k)>popmax(k)
                pop(j,k) = popmax(k);
            end
        end
        for k = 1:dimension
            if pop(j,k)<popmin(k)
                pop(j,k) = popmin(k);
            end
        end 
        %适应度值
        fitness(j)=targetfunction(pop(j,:)); 
    end
    for j=1:sizepop
        %个体最优更新
        if fitness(j) > fitnessgbest(j)
            gbest(j,:) = pop(j,:);
            fitnessgbest(j) = fitness(j);
        end 
        %群体最优更新
        if fitness(j) > fitnesszbest
            zbest = pop(j,:);
            fitnesszbest = fitness(j);
        end
    end 
    yy(i)=fitnesszbest;        
end
%% 结果分析
plot(yy)
title('最优个体适应度(最大值)迭代变化情况','fontsize',12);
xlabel('进化代数','fontsize',12);ylabel('适应度','fontsize',12);
end

