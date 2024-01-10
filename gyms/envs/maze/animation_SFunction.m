%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Name : animation_SFunction.m
%%
%% Description : Take and give all parametres from the simulink simulation
%%               to the animation.
%%
%% Date : 27/03/2018
%% Release : 1.0
%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



%%
function animation_SFunction(block)

% Level-2 MATLAB file S-function for visualizing an animation.
  setup(block)
  
end


%% Called when the block is added to a model.
function setup(block)

  % 1 input port, no output ports
  block.NumInputPorts  = 3;
  block.NumOutputPorts = 0;
  
  % Setup functional port properties
  block.SetPreCompInpPortInfoToDynamic;
  
  % For load the "size_map"
  load('data.mat');
  
  % The input is a position of the Thymio, data sensors, a picture maze and
  % a record control
  block.InputPort(1).Dimensions = 3;
  block.InputPort(2).Dimensions = 20;
  block.InputPort(3).Dimensions = [size_map size_map];

  
  % Register block methods
  block.RegBlockMethod('Start',   @Start);
  block.RegBlockMethod('Outputs', @Output);
  
  % To work in external mode
  block.SetSimViewingDevice(true);
  
end


%% Called when the simulation starts.
function Start(block)
  
  % Check to see if we already have an instance of animation
  ud = get_param(block.BlockHandle,'UserData');
  
  if isempty(ud)
    vis = [];
  else
    vis = ud.vis;
  end
  
  %If not, create one
  if isempty(vis) || ~isa(vis,'animation') || ~vis.isAlive
    vis = animation(block.InputPort(3).Data);
  else
%     vis.clearPoints();
  end
  
  ud.vis = vis;
  
  % Save it in UserData
  set_param(block.BlockHandle,'UserData',ud);

  
end


%% Called when the simulation time changes.
function Output(block)

  if block.IsMajorTimeStep
    
    % Every time step, call ...
    ud  = get_param(block.BlockHandle,'UserData');
    vis = ud.vis;
    
    if isempty(vis) || ~isa(vis,'animation') || ~vis.isAlive
      return;
    end
    
    vis.set_Position(block.InputPort(1).Data(1), ...    % x
                     block.InputPort(1).Data(2), ...    % y
                     block.InputPort(1).Data(3), ...    % theta
                     block.InputPort(3).Data, ...       % maze
                     block.InputPort(2).Data);          % record_on_off
   
  end
  
end

