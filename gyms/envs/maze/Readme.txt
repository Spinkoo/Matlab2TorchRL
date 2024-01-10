 
 -----------------------------/----------------------------\-----------------------------
         ----------------------|    A Thymio in a maze    |----------------------
 -----------------------------\----------------------------/-----------------------------



This is the Readme for a simulation of a Thymio runing through and solving mazes,   implemented in Matlab's Simulink.



 -------------------------------------
    ----|    Prerequisites    |----   
 -------------------------------------

   Matlab and Simulink - 2018a or 2015b or 2015a


 -------------------------------------
    ----|    Running tests    |----   
 -------------------------------------

   1 - Run setup.m
   2 - Run simulation_1_Random_Mouse.slx        or
           Simulation_2_Wall_Follower_v1.slx    or
           Simulation_2_Wall_Follower_v2.slx    or
           Simulation_3_Pledge_v1               or
           Simulation_3_Pledge_v2


 -------------------------------------
    ----|    Record tests    |----   
 -------------------------------------

For record an animation, do the following tasks :

   1 - In a simulink file, turn on the switch.
   2 - Run a simulation.
   3 - For end the record befor the end, turn off the switch, than
       Stop the simulation.
   5 - Change the name of the of the "Thymio_in_a_maze.avi" for
       make sure will be not replace with another simulation record.


 --------------------------------------
    ----|     Files     |----   
 --------------------------------------

   [setup.m] : Load end initialize all parametres we need for a simulation.

   [constante.m] : Contients the main caracteristiques of the robot.

   [thresholding_image] : Scales the pixels values of a picture.

   [animation] : Creat a figure where the Thymio can move.

   [animation_SFunction] : Take and give all parametres from the simulink simulation
                           to the animation.

   [Simulation_1_Random_Mouse] : Simulate the a Thymio solving a maze with random
                                 decisions.

   [Simulation_2_Wall_Follower_v1] : Simulate the a Thymio solving a maze following
                                     a wall. (It notreally follow a wall)

   [Simulation_2_Wall_Follower_v2] : Simulate the a Thymio solving a maze following
                                     a wall. (It can really follow a wall)

   [Simulation_3_Pledge_v1] : Simulate the a Thymio solving a maze with the Pledge
                              algorithm. (It not really follow a wall)

   [Simulation_3_Pledge_v2] : Simulate the a Thymio solving a maze with the Pledge
                              algorithm. (It can really follow a wall)


   [maze_0] : Map where the Thymio have to travel.

   [données_maze_0] : Contients the start position of the Thymio.



   [.\Simulation_2015a] : Contients all simulations for Matlab 2015a.

   [.\Simulation_2015b] : Contients all simulations for Matlab 2015b.

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

created  : 06 Feb 2018
modified : 20 may 2018


 -----------------------------\----------------------------/-----------------------------