 
 -----------------------------/----------------------------\-----------------------------
         ----------------------|    A Thymio in a maze    |----------------------
 -----------------------------\----------------------------/-----------------------------



This is the Readme for a simulation of a Thymio runing through and solving mazes,   implemented in Matlab's Simulink.



 -------------------------------------
    ----|    Prerequisites    |----   
 -------------------------------------

   Matlab and Simulink - > 2015a


 -------------------------------------
    ----|    Running tests    |----   
 -------------------------------------

   1 - Run setup.m
   2 - Run Simulation_2_Wall_Follower_v1.slx


 --------------------------------------
    ----|     Simulink model     |----   
 --------------------------------------

 ![Architecture of the simulation](./Overall_arch.png)



 --------------------------------------
    ----|     Files     |----   
 --------------------------------------

   [setup.m] : Load end initialize all parametres we need for a simulation.

   [constante.m] : Contients the main caracteristiques of the robot.

   [thresholding_image] : Scales the pixels values of a picture.

   [animation] : Creat a figure where the Thymio can move.

   [animation_SFunction] : Take and give all parametres from the simulink simulation
                           to the animation.

   [Simulation_2_Wall_Follower_v1] : Simulate the a Thymio solving a maze following
                                     a wall. (It notreally follow a wall)


   [maze_0] : Map where the Thymio have to travel.

   [donn�es_maze_0] : Contients the start position of the Thymio.

   [.\maze] : Contients all maps and positions for a simulation.

 
 ----------------------------------
    ----|    References    |----   
 ----------------------------------

 (1) Robotics, Vision and Control - Fundamental algorithms in Matla Peter Corke

 (2) Using MATLAB Graphics from Simulink, Mike Garrity
     https://blogs.mathworks.com/graphics/2014/10/21/double_pendulum/

 (3) simple_2D_steering_animation_v2, Marc Compere, comperem@gmail.com
     https://fr.mathworks.com/matlabcentral/fileexchange/54852-simple-2d-kinematic-vehicle-steering-model-and-animation


 -------------------------------
    ----|    Abouts    |----   
 -------------------------------

Made by students of Aix-Marseille University

BAMOUDOU Nassouif - issa.nassouif@gmail.com
ATIAS Sophian - triedge558@gmail.com
CHARPENTIER Jonathan - j.the-foam@hotmail.com

Modified by Wail HARROUZ

created  : 06 Feb 2018
modified : 10 OCt 2023


 -----------------------------\----------------------------/-----------------------------