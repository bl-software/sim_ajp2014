% The program builds the diffusion matrices for single substances. The
% matrices inside and outside are coupled via the boundary coupling vector.
% The Structure of the matrix is
%
%          
%        [ L_in      | c_in |  0  ]
%   L =  [----------------------- ]
%        [ 0 | c_out |      L_out ]
%
%
%  INPUT   - n_in, n_out  : integers defining the discretization
%            R            : radius of the cell
%            R_inf        : radius of the computational domain
%            kappa_in/out : diffusion coefficients in/out
%            perm_alpha        : Fick's constant across the membrane
%--------------------------------------------------------------------------
% CALLS TO: DiffusionMatrixInsideDistr.m, DiffusionMatrixOutsideDistr.m
%--------------------------------------------------------------------------


function [L b_inf] = SingleSpeciesDiffMatDistr(n_in,n_out,R,R_inf,kappa_in,kappa_out,perm_alpha)

% Computing the inside diffusion matrix ...

[L_in c_in] = DiffusionMatrixInsideDistr(n_in,R,kappa_in,perm_alpha);

% ... and the outside diffusion matrix

[L_out c_out b_vec] = DiffusionMatrixOutsideDistr(n_out,R,kappa_out,perm_alpha,R_inf);

% Composing the matrix and the boundary vector

L12           = sparse(n_in+1,n_out);
L12(:,1)      = sparse(c_in);
L21           = sparse(n_out,n_in+1);
L21(:,n_in+1) = sparse(c_out);
L             = [L_in,L12;L21,L_out];
b_inf         = [zeros(n_in+1,1);b_vec];

