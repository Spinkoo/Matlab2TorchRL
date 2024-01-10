%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% image_out = thresholding_image(image_in,NNdG,S)
%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Name : thresholding_image.m
%%
%% Description : Scales the pixels values of a picture in binary values.
%%
%% Input  : image_in (matrice) = No scaled image
%%          S (scalar) = Separation threshold
%%
%% Output : image_out (matrice) = Scaled image in binary values
%%
%% Date : 27/03/2018
%% Release : 2.0
%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



function image_out = thresholding_image(image_in, S)

  % Initialization
  image_out = image_in;
  
  image_out(image_in <= S) = 1;    % Put to 1 the values uper to S
  image_out(image_in > S)  = 0;    % Put to 0 the values lower to S

end



%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%