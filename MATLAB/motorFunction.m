function [A,B,C,D,K]=motorFunction(R_mot,L_mot,beta_mot,K_mot,J_mot,ts)

    A=[0 1 0;
        0 -beta_mot/J_mot K_mot/J_mot;
        0 -K_mot/L_mot -R_mot/L_mot];
    
    B=[0;
        0;
        1/L_mot];

    C=[1 0 0;
         0 1 0];

    D=[0;
        0];

    K=[0 0;
        0 0;
        0 0];