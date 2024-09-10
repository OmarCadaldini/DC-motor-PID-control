clear all
clc

% init values
R_mot0      =4;
L_mot0      =0.002;
beta_mot0   =0.0001;
K_mot0      =0.09;
J_mot0      =0.009;
parameters={'R',R_mot0; 'L',L_mot0; 'beta',beta_mot0; 'K', K_mot0; 'J', J_mot0};

filename  = ['grey_result.csv'];
file_data = readtable(filename);
u = file_data{:, 1};
y_1 = file_data{:,2};%theta
y_2 = file_data{:, 3};%omega
y = [y_1,y_2];
data = iddata(y,u,0.1);
mu = getTrend(data,0);
data_d = detrend(data,mu);

% initialization of the parameter theta
init_sys = idgrey('motorFunction',parameters,'c')

init_sys.Structure.Parameters(1).Free=false;%R
init_sys.Structure.Parameters(2).Minimum=0.002;%L
init_sys.Structure.Parameters(3).Minimum=0;%beta
init_sys.Structure.Parameters(5).Free=false;%J

% estimate the grey-box model
opt = greyestOptions('InitialState','estimate','Display','on');
m_grey = greyest(data,init_sys)
compare(data,m_grey)