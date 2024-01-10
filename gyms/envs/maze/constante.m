%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Name : constante.m
%%
%% Description : Contients the main caracteristiques of the robot.
%%
%% Date : 28/03/2018
%% Release : 1.0
%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



%% Thymio dimention
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Long = 11;               % [cm]     Réel = 11 cm
Larg = 11;               % [cm]     Réel = 11.2 cm

% Distance centre / wheels
L = 5;                   % [cm]     Réel = 4.7 cm


%% Sensors features
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

S_max  = 20;             % [cm]     Réel = 5.5 cm
S_sens = 0.1;            % [cm]


%% Position of the sensors since the Thymio center
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

D0 = 8;                 % [cm]
K0 = pi/3;              % [rad]

D1 = 8;                 % [cm]
K1 = pi/6;              % [rad]

D2 = 8;                 % [cm]

D3 = D1;                % [cm]
K3 = -K1;               % [rad]

D4 = D0;                % [cm]
K4 = -K0;               % [rad]


K = [ K0 K1  0 K3 K4 ];
D = [ D0 D1 D2 D3 D4 ];



%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%