%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Name : setup.m
%%
%% Description : Load end initialize all parametres we need for
%%               a simulation.
%%
%% Date : 27/03/2018
%% Release : 1.0
%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



%% Initialization
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  clc
  close all
  clear all


%% Initialization Thymio constants
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

constante;


%% Load a maze
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

name_maze = 'maze_3';

addpath('maze');

map = imread(strcat(name_maze,'.png'));
map = map(:,:,1);


% Thresholding image
maze = thresholding_image(map,100);

% Invert the y-axis
maze = flipud(maze);

% 
number_add = 50;
for c = 0:number_add
  
  size_map = length(maze);
  add_line = zeros(1,size_map);
  maze = cat(1,add_line,maze);
  maze = cat(1,maze,add_line);

  size_map   = length(maze);
  add_column = zeros(size_map,1);
  maze = cat(2,add_column,maze);
  maze = cat(2,maze,add_column);
  
end

% Test
%   imagesc(maze), colormap(flipud(gray)), caxis([0 1]);hold all 


%% Load position data of the Thymio in the maze
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Ex : Position in x, y et theta of the Thymio

load(strcat('data_',name_maze,'.mat'))

% Test
%   Xd = 70;
%   Yd = 170;
%   Theta_d = -pi/2;


%% Initialization of the speed
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Vg = 0.05;   % 0.05
Vd = 0.05;


%% Initialization of the seed
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% rng(3,'twister');
% s = rng;


%% Start simulation
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

save('data.mat');

% sim('Simulation_1_Random_Mouse')



%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%