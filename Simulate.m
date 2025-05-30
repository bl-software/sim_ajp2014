% Copyright © 2015 Dale Huffman, Walter Boron
% SPDX-License-Identifier: GPL-3.0-or-later
% Original files this is derived from Copyright © 2015,2024 Rossana Occhipinti

% % This file runs simulations for CO2 addition 
% % Moreover it computes:
% % 1) delta_pHs = changes in steady-state pHs
% % 2) delta_pHi = changes in steady-state pHi
% % 3) dpHi/dt = initial rate of pHi change 
% % 4) tau_p = time to peak for pHs
% % 5) t_d = time delay for pHi changes (if we have it)
% 
% % R. Occhipinti
%
% Setting up the model, computing the parameter structure for the rhs in
% the ODE solver

% Can be run by hand in Matlab
%run('rbc2024a/rbc2024a_paramsIn.m')
%Simulate('JTB','Blah','test_JTB_fig3','testJ3')

% Simulate 
%  --> DiffusionMatrixDistr
%       --> SingleSpeciesDiffMatDistr
%            --> DiffusionMatrixInsideDistr
%            --> DiffusionMatrixOutsideDistr
%  
function [time,X] = Simulate(sim_type,prog_title,sim_dir,sim_filename_base)
fprintf('*******************************************\n')
fprintf('* In Simulate.m *\n')
fprintf('*******************************************\n')

% Read in user parameters from gui equivalent file
gui_param_file = strcat(sim_dir,'/',sim_filename_base,'_paramsIn.m');
fprintf('* GUI Param File =\n  %s *\n', gui_param_file )
fprintf('*** Running GUI Param File *\n')
run(gui_param_file);
fprintf('*** Successfully Ran GUI Param File *\n')

fprintf('*******************************************\n')
fprintf('\n*** SimType= %s ***\n', sim_type)

ModelParameters_All;
%ModelParametersDistr_DE_paper_3_buff
%Raif_ModelParametersDistr_Different_IC_Flow % Model parameters for the distributed model

fprintf('* Calling DiffusionMatrixDistr *\n')
[A W] = DiffusionMatrixDistr(n_in,n_out,R,R_inf, ...
             kappa_in,kappa_out,perm_alpha,n_buff);

fprintf('* Setting Parms.X *\n')
Params.DiffusionMatrix = A;
Params.BoundaryVector  = W;
Params.ReactionRates   = k;
Params.BoundaryValues  = X_inf;
Params.N               = N;
Params.n_out           = n_out;
Params.n_in            = n_in;

Params.NumberOfBuffers = n_buff;

USE_ODSTIME=1;

% Solving the system 
tic

fprintf('* Calling odeset *\n')
options = odeset('RelTol',1e-12,'AbsTol',1e-12,'Stats','off');

fprintf('simtype=%s\n',sim_type)

fprintf('*************************************************\n')
fprintf('* Calling ode15s with ReactionDiffusionDistrRHS *\n')
fprintf('*************************************************\n')
[time,X] = ode15s(@ReactionDiffusionDistrRHS,[0,tmax],X0,options,Params);

toc

outparams=strcat(sim_dir,'/',sim_filename_base,'_paramsOut')
matlab.io.saveVariablesToScript(outparams)
save(strcat(sim_dir,'/',sim_filename_base,'.mat'))

return

