function PSO_MulTarget()
%% ��ջ���
clear;
clc;

%% ��������
w=0.9;%Ȩֵ ��Ӱ��PSO ��ȫ����ֲ����������� ֵ�ϴ�ȫ����������ǿ���ֲ�����������;��֮����ֲ�����������ǿ����ȫ����������������
c1=0.1;%���ٶȣ�Ӱ�������ٶ�
c2=0.1;
dim=6;%6ά����ʾ��ҵ����
swarmsize=100;%����Ⱥ��ģ����ʾ��100����Ŀռ�
maxiter=200;%���ѭ��������Ӱ��ʱ��
minfit=0.001;%��С��Ӧֵ
vmax=0.01;
vmin=-0.01;
ub=[0.2,0.2,0.2,0.2,0.2,0.2];%���������������
lb=[0.01,0.01,0.01,0.01,0.01,0.01];%����������С����

%% ��Ⱥ��ʼ��
range=ones(swarmsize,1)*(ub-lb);
swarm=rand(swarmsize,dim).*range+ones(swarmsize,1)*lb;%����Ⱥλ�þ���
Y1=[33.08;
   21.85; 
   6.19; 
   11.77; 
   9.96; 
   17.15;]; 
Y=Y1./100;%���ٷ�����ΪС��
[ym,yn]=size(Y);
for i=1:swarmsize  %% YX��Լ��
    s=swarm(i,:);
    ss=s';
    while sum(Y.*ss)<0.1*sum(Y)
        ss=rand(dim,1).*((ub-lb)')+ones(dim,1).*((lb)');
    end
    swarm(i,:)=ss';
end
vstep=rand(swarmsize,dim)*(vmax-vmin)+vmin;%����Ⱥ�ٶȾ���
fswarm=zeros(swarmsize,1);%Ԥ��վ��󣬴����Ӧֵ
for i=1:swarmsize
    X=swarm(i,:);
    [SUMG,G]=jn(X);
    fswarm(i,:)=SUMG;
    %fswarm(i,:)=feval(jn,swarm(i,:));%������Ⱥλ�õĵ�i��Ϊ���룬����ֵ����Ӧ�������Ӧֵ
end

%% ���弫ֵ��Ⱥ�弫ֵ
[bestf,bestindex]=min(fswarm);%�����Ӧֵ�е���С��Ӧֵ���ͣ������ڵ�����
gbest=swarm;%��ʱ�ĸ������Ž�Ϊ�Լ�
fgbest=fswarm;%��ʱ�ĸ���������Ӧֵ
zbest=swarm(bestindex,:);%�������еĶ�Ӧ�Ľ�������У�ȫ����ѽ�
fzbest=bestf;%ȫ��������Ӧֵ


%% ����Ѱ��
iter=0;
yfitness=zeros(1,maxiter);%1��100�о��󣬴��100������ֵ�Ŀռ����
x1=zeros(1,maxiter);%���x�Ŀռ�
x2=zeros(1,maxiter);
x3=zeros(1,maxiter);
x4=zeros(1,maxiter);
x5=zeros(1,maxiter);
x6=zeros(1,maxiter);
while((iter<maxiter)&&(fzbest>minfit))
    for j=1:swarmsize
        % �ٶȸ���
        vstep(j,:)=w*vstep(j,:)+c1*rand*(gbest(j,:)-swarm(j,:))+c2*rand*(zbest-swarm(j,:));
        if vstep(j,:)>vmax  
            vstep(j,:)=vmax;%�ٶ�����
        end
        if vstep(j,:)<vmin
            vstep(j,:)=vmin;
        end
        % λ�ø���
        swarm(j,:)=swarm(j,:)+vstep(j,:);
        for k=1:dim
            if swarm(j,k)>ub(k)
                swarm(j,k)=ub(k);%λ������
            end
            if swarm(j,k)<lb(k)
                swarm(j,k)=lb(k);
            end
        end
       
        % ��Ӧֵ        
         X=swarm(j,:);
         [SUMG,G]=jn(X);
         fswarm(j,:)=SUMG;
        % ���ڴ˴�����Լ��������������Լ���������������Ӧֵ����
        
        %
        % �������Ÿ���
        if fswarm(j)<fgbest(j) %�����ǰ�ĺ���ֵ�ȸ�������ֵС
            gbest(j,:)=swarm(j,:);%�������Ž����
            fgbest(j)=fswarm(j);%��������ֵ����
        end
        % Ⱥ�����Ÿ���
        if fswarm(j)<fzbest%�����ǰ�ĺ���ֵ��Ⱥ������ֵ��
            zbest=swarm(j,:);%Ⱥ�����Ž����
            fzbest=fswarm(j);%Ⱥ������ֵ����
        end
    end
    iter=iter+1;
    yfitness(1,iter)=fzbest;
    x1(1,iter)=zbest(1);%��ȫ�����Ž�ĵ�1��Ԫ�أ����δ洢������MAXITER��
    x2(1,iter)=zbest(2);
    x3(1,iter)=zbest(3);
    x4(1,iter)=zbest(4);
    x5(1,iter)=zbest(5);
    x6(1,iter)=zbest(6);
end

fzbest
zbest
X=zbest;
[SUMG,G]=jn(X);
GGbest=G;GGbest
%% ��ͼ
figure(1)
plot(yfitness,'linewidth',2)
title('���Ż���ϵ���Ż�����','fontsize',14);
xlabel('��������','fontsize',14);
ylabel('����ϵ��','fontsize',14);

figure(2)
plot(x1,'b')
hold on
plot(x2,'g')
hold on
plot(x3,'r')
hold on
plot(x4,'c')
hold on
plot(x5,'m')
hold on
plot(x6,'y')
title('x�Ż�����','fontsize',14);
xlabel('��������','fontsize',14);
ylabel('����ֵ','fontsize',14);
legend({'x1','x2','x3','x4','x5','x6'},'Location','best');



%% ��Ӧ�Ⱥ���,��ΪĿ�꺯��������Ϊ����ϵ������
function [SUMG,G]=jn(X)
%% ��֪����
% A�����б�ʾ��ҵ��ţ��б�ʾԱ����Ӫҵ���롢˰���ܶ��������λ�ٷ���
A1=[ 30.8 59.2 39.92;
    17.6 9.5  31.42;
    13.6 7.1  6.62;
    9.5  7    5.64;
    23.8 5.8  4.79;
    4.7  11.4 11.6;];
A=A1./100;%���ٷ�����ΪС��
[am,an]=size(A);
% Y�����б�ʾ��ҵ��ţ��б�ʾ������̼�ٷֱȣ�����Ϊ�ٷ���
Y1=[33.08;
   21.85; 
   6.19; 
   11.77; 
   9.96; 
   17.15;]; 
Y=Y1./100;%���ٷ�����ΪС��
[ym,yn]=size(Y);
%% ����X��������X
XX=X';%������ת��
one=ones(ym,yn);
newx=one-XX;
%% �������ϵ��G
G=zeros(an,1);
for j=1:an
    aj=A(:,j);
    yx1=Y.*newx;
    yx=yx1./sum(yx1);
    ya=yx./aj;
    compose=[ya,aj,yx;];
    newm=sortrows(compose,1);% ��ya�����С�����������У�
    ajnew=newm(:,2);
    yxnew=newm(:,3);
    yxnewsum=zeros(ym,yn);
    for ii=1:ym
        yxnewsum(ii,yn)=sum(yxnew(1:ii));
    end   
    yxnewsum2=zeros(ym,yn);
    for iii=1:ym
        if iii==1
            yxnewsum2(iii,yn)=yxnewsum(iii,yn);
        else 
        yxnewsum2(iii,yn)=yxnewsum(iii-1,yn)+yxnewsum(iii,yn);
        end
    end   
    ay=ajnew.*yxnewsum2;
    gj=1-sum(ay);
    G(j)=gj;
end
GMAX=[0.3;0.3;0.2;];
if ((G(1)-GMAX(1)>0)||(G(2)-GMAX(2)>0)||(G(3)-GMAX(3)>0))
    G=GMAX;
end
SUMG=0.61*G(1)+0.19*G(2)+0.2*G(3);
%���G������ϵ��








