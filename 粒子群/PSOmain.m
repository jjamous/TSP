clc,clear;
%% ��Ŀ�꺯�����ֵ����Сֵ�ǵø���ת������
targetfunction = @(x)-(10 + x(1) ^ 2 + x(2) ^ 2 - 10 * (cos(2 * pi * x(1)) + cos(2 * pi * x(2))));% ���ֵ-10
dimension = 2;
popmin=[-2,-2];      % �Ա���lb,����λ�÷�Χ�½�
popmax=[2,2];        % �Ա���ub,����λ�÷�Χ�Ͻ�
Vmin=[-0.5,-0.5];    % ������С�˶��ٶ�,Ҫ����
Vmax=[0.5,0.5];      % ��������˶��ٶ�,Ҫ����
w=1;                 % ��������,ֵ�ϴ�ȫ��Ѱ������ǿ��ֵ��С���ֲ�Ѱ������ǿ
c1=1.5;              % ����ѧϰ����,��Ҫ���ζ���
c2=1.5;              % ���ѧϰ����,��Ҫ���ζ���
sizepop=20;          % ��Ⱥpopulation��ģ
maxgen = 300;        % ��������  
%% ���������м��������ֵ
[fitnesszbest,zbest] = PSO(targetfunction,dimension,popmin,popmax,Vmin,Vmax,w,c1,c2,sizepop,maxgen);
disp(['Ŀ�꺯�����ֵ:',num2str(fitnesszbest)]);
disp(['Ŀ�꺯�����ֵ��:',num2str(zbest)]);
