%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Name : animation.m
%%
%% Description : Creat a figure where the Thymio can move.
%%
%% Date : 08/05/2018
%% Release : 2.0
%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



classdef animation < handle
  
  properties (SetAccess = private)
    
    Vehicule = gobjects;            % Creat an graphique objet
    Traces   = gobjects;
    
    Longeur  = 11;                  % [cm]     Real = 11 cm
    Largeur  = 11;                  % [cm]     Real = 11.2 cm
    
    Position = [0 0];
    Angle    = 0;
    
%     size_map = 205;
    maze     = gobjects;
    
    Sensor_0 = gobjects;
    Sensor_1 = gobjects;
    Sensor_2 = gobjects;
    Sensor_3 = gobjects;
    Sensor_4 = gobjects;
    
  %             [Xs Ys Xc Yc]
    Position_S = [ 0 0 0 0         % Signal and Sensor 0
                   0 0 0 0         % Signal and Sensor 1
                   0 0 0 0         % Signal and Sensor 2
                   0 0 0 0         % Signal and Sensor 3
                   0 0 0 0 ];      % Signal and Sensor 4
    movie  = 0;
    record = 0;
    
  end

  %%
  methods
    
    % Called by animation_SFunction when the simulation starts.
    function obj = animation(map)
      
      obj.maze = map;
      obj.create_Graphics(length(map));
      obj.update_Transforms();
%       obj.addTracePoints();

%       obj.record = record;
%       obj.set_record(record);
      
    end

    % Call this to change the Position.
    function set_Position(obj, x, y, a, map, pos)
      
      obj.Position(1) = x;
      obj.Position(2) = y;
      obj.Angle       = a;
      
      obj.Position_S(1,1) = pos(1);                % x1
      obj.Position_S(1,2) = pos(6);                % y1
      obj.Position_S(1,3) = pos(11);
      obj.Position_S(1,4) = pos(16);
      
      obj.Position_S(2,1) = pos(2);                % x1
      obj.Position_S(2,2) = pos(7);                % y1
      obj.Position_S(2,3) = pos(12);
      obj.Position_S(2,4) = pos(17);
      
      obj.Position_S(3,1) = pos(3);                % x1
      obj.Position_S(3,2) = pos(8);                % y1
      obj.Position_S(3,3) = pos(13);
      obj.Position_S(3,4) = pos(18);
      
      obj.Position_S(4,1) = pos(4);                % x1
      obj.Position_S(4,2) = pos(9);                % y1
      obj.Position_S(4,3) = pos(14);
      obj.Position_S(4,4) = pos(19);
      
      obj.Position_S(5,1) = pos(5);                % x1
      obj.Position_S(5,2) = pos(10);               % y1
      obj.Position_S(5,3) = pos(15);
      obj.Position_S(5,4) = pos(20);
      
      obj.update_Transforms();
      obj.update_map(map);
      

      
    end
    
    % Call this to reset the traces.
    function clearPoints(obj)
%       obj.Traces.clearpoints();
    end

    %Call this to check whether the figure window is still alive.
    function r = isAlive(obj)
      r = isvalid(obj) && ...
          isvalid(obj.Vehicule) && ...
          isvalid(obj.Sensor_0) && ...
          isvalid(obj.Sensor_1) && ...
          isvalid(obj.Sensor_2) && ...
          isvalid(obj.Sensor_3) && ...
          isvalid(obj.Sensor_4);
%           isvalid(obj.Traces);
    end
    
    % Creates a mouvie of the animation
    function set_record(obj,record_on_off)
      
      obj.record = record_on_off;
          

      
    end

  end
  
  
  %%
  methods (Access = private)

    % 
    function create_vehicule(obj, v, color_fond)
      
      % Initialization
      Long = obj.Longeur / (11/6);      % = 6
      Larg = obj.Largeur;
      X    = obj.Position(1);
      Y    = obj.Position(2);
      
      forme_1 = rectangle('Parent',v, ...
                          'Position',[X-Long/2 Y-Larg/2 Long Larg], ...
                          'Curvature',[0.2 0.2], ...
                          'FaceColor',color_fond, ...
                          'EdgeColor','none');
      
      forme_2 = rectangle('Parent',v, ...
                          'Position',[X+Long/2-2 Y-Larg/2 3.8+2 Larg], ...
                          'Curvature',[0.4 0.4], ...
                          'FaceColor',color_fond, ...
                          'EdgeColor','none');
      
    end
    
    % 
    function create_vector_sensors(obj, v, Num_S, color)
      
      % Initialization
      X1 = obj.Position_S(Num_S+1,1);
      Y1 = obj.Position_S(Num_S+1,2);
      X2 = obj.Position_S(Num_S+1,3);
      Y2 = obj.Position_S(Num_S+1,4);
      
      Signal = line('Parent',v, ...
                    'XData',[X1 X2], ...
                    'YData',[Y1 Y2], ...
                    'Color',color);
      
    end
    
    % Adds the current end points of the two pendulums to the traces.
    function addTracePoints(obj)
      
%       x = obj.Position(1);
%       y = obj.Position(2);
      
%       obj.Traces.addpoints(x,y);

    end
    
    % Creates all of the graphics objects for the visualization.
    function create_Graphics(obj, size_fig)

      % Create the map
      map = imagesc(obj.maze);
      map.Visible = 'off';
      
      % Recover the figure
      fig = gcf;
      
      % Initialize the figure
      fig.Color    = 'white';
      fig.MenuBar  = 'none';   %'figure'
      fig.NumberTitle   = 'off';
      fig.Name     = 'Thymio in a Maze';
      fig.ToolBar  = 'none';   %'figure';
%       fig.Position(3) = size_fig + 105;         %450;       %x
%       fig.Position(4) = size_fig + 100;         %420;       %y
%       fig.Position = [780 430 450 400];
      
      % Recover the axes
      ax = gca;
      
      % Initialize the axes.
      ax.Visible = 'on';
      ax.YDir  = 'normal';
%       ax.XLim  = [1 obj.size_map];
%       ax.YLim  = [1 obj.size_map];
%       ax.XTick = 0:20:obj.size_map;
%       ax.YTick = 0:20:obj.size_map;
%       grid(ax,'on');
%       ax.Units = 'pixels';
%       ax.Position = [10 10 430 390];
%       ax.Position(1) = 10; ax.Position(2) = 10;
      ax.DataAspectRatio = [1 1 1];
      ax.SortMethod      = 'childorder';
      
      % Create the traces
%       obj.Traces = animatedline('Parent', ax, 'Color', 'red');

      % Create the transforms
      obj.Vehicule = hgtransform('Parent', ax);
      obj.Sensor_0 = hgtransform('Parent', ax);
      obj.Sensor_1 = hgtransform('Parent', ax);
      obj.Sensor_2 = hgtransform('Parent', ax);
      obj.Sensor_3 = hgtransform('Parent', ax);
      obj.Sensor_4 = hgtransform('Parent', ax);

      % Create the vehicule
      create_vehicule(obj, obj.Vehicule, 'blue');
      
      % Create the signals
      create_vector_sensors(obj, obj.Sensor_0, 0, 'red');
      create_vector_sensors(obj, obj.Sensor_1, 1, 'green');
      create_vector_sensors(obj, obj.Sensor_2, 2, 'blue');
      create_vector_sensors(obj, obj.Sensor_3, 3, 'cyan');
      create_vector_sensors(obj, obj.Sensor_4, 4, 'magenta');
      
    end
    
    % Updates the transform matrices.
    function update_Transforms(obj)
    
      x = obj.Position(1);
      y = obj.Position(2);
      a = obj.Angle;
      
      X1 = obj.Position_S(:,1);
      Y1 = obj.Position_S(:,2);
      
      X2 = obj.Position_S(:,3);
      Y2 = obj.Position_S(:,4);
      
      obj.Vehicule.Matrix = makehgtform('translate', [x y 0], ...
                                        'zrotate', a);
      
      obj.Sensor_0.Children.XData = [X1(1) X2(1)];
      obj.Sensor_0.Children.YData = [Y1(1) Y2(1)];

      obj.Sensor_1.Children.XData = [X1(2) X2(2)];
      obj.Sensor_1.Children.YData = [Y1(2) Y2(2)];
      
      obj.Sensor_2.Children.XData = [X1(3) X2(3)];
      obj.Sensor_2.Children.YData = [Y1(3) Y2(3)];

      obj.Sensor_3.Children.XData = [X1(4) X2(4)];
      obj.Sensor_3.Children.YData = [Y1(4) Y2(4)];
      
      obj.Sensor_4.Children.XData = [X1(5) X2(5)];
      obj.Sensor_4.Children.YData = [Y1(5) Y2(5)];

    end
    
    % Save each frame of the animation
    function record_anim(obj)
      
      
      
    end
    
    % Updates the image from of the curent figure.
    function update_map(obj, map)
    
      if sum(sum(map)) > 0 && sum(sum(obj.maze)) == 0

        im = findobj(gca,'Type','image');

        caxis([0 1]), colormap(flipud(gray));
        im.CData = map;

        im.Visible = 'on';
        obj.maze = map;

      end
      
    end
    
  end
    
end



%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%