R=4;%4
L=0.002;%2e-3
beta=0;%0
K=0.09325;%0.09
J=0.009;%0.009

A=[0 1 0;
   0 -beta/J K/J;
   0 -K/L -R/L];
    
b=[0;
   0;
   1/L];

c=[0 1 0];

d=0;

sys=ss(A,b,c,d)
G=tf(sys)

sisotool(G)