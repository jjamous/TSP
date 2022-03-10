function [fitnesszbest,zbest] = PSO(targetfunction,dimension,popmin,popmax,Vmin,Vmax,w,c1,c2,sizepop,maxgen)
%% �����ĵ�
% targetfunction ��Ŀ�꺯������ʽf(x),ע����������ֵ����СֵҪ����ת��
% dimension      ���Ա���x��ά��
% popmin         ��x��lb
% popmax         ��x��ub
% Vmin           ��������С�˶��ٶ�
% Vmax           ����������˶��ٶ�
% w              ���������ӣ�ֵ�ϴ�ȫ��Ѱ������ǿ��ֵ��С���ֲ�Ѱ������ǿ
% C1/C2          �����ٳ�����C1Ϊ���ӵĸ���ѧϰ���ӣ�C2Ϊ���ӵ����ѧϰ���ӣ�һ��c1=c2=2��һ��C1 = C2 ��[0,4]
% sizepop        ����������������Ĭ��20
% maxgen         ��������������������Ĭ��300
%% ������ʼ���Ӻ��ٶ�
for i=1:sizepop
    for j=1:dimension
        %�������һ����Ⱥ
        pop(i,j)=(popmax(j)-popmin(j))*rand+popmin(j);    %��ʼ��Ⱥ
        V(i,j)=(Vmax(j)-Vmin(j))*rand+Vmin(j);  %��ʼ���ٶ�
    end
    %������Ӧ��
    fitness(i)=targetfunction(pop(i,:));   %Ⱦɫ�����Ӧ��
end

%% ���弫ֵ��Ⱥ�弫ֵ
[bestfitness,bestindex]=max(fitness);
zbest=pop(bestindex,:);   %ȫ�����
gbest=pop;    %�������
fitnessgbest=fitness;   %���������Ӧ��ֵ
fitnesszbest=bestfitness;   %ȫ�������Ӧ��ֵ

%% ����Ѱ��
for i=1:maxgen
    for j=1:sizepop 
        %�ٶȸ���
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
        %��Ⱥ����
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
        %��Ӧ��ֵ
        fitness(j)=targetfunction(pop(j,:)); 
    end
    for j=1:sizepop
        %�������Ÿ���
        if fitness(j) > fitnessgbest(j)
            gbest(j,:) = pop(j,:);
            fitnessgbest(j) = fitness(j);
        end 
        %Ⱥ�����Ÿ���
        if fitness(j) > fitnesszbest
            zbest = pop(j,:);
            fitnesszbest = fitness(j);
        end
    end 
    yy(i)=fitnesszbest;        
end
%% �������
plot(yy)
title('���Ÿ�����Ӧ��(���ֵ)�����仯���','fontsize',12);
xlabel('��������','fontsize',12);ylabel('��Ӧ��','fontsize',12);
end

