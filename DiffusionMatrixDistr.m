% Diffusion matrix for the model including CO2, H+ and n_buff buffers. The 
% first buffer is always present and is tha carbonic acid/bicarbonate pair.
%
% Structure of the output sparse matrices:
%
%        [ Du0  0    0  0  ]          [ Dv0  0    0  0  ]
%   Du = [      Du1  0  0  ],    Dv = [      Dv1  0  0  ]
%        [       ..  ..    ]          [       ..  ..    ]
%        [              Dun]          [              Dvn]
%   
%   A =   [Du     0 ]
%         [0      Dv]
%
%  W is constructed similarly, but the matrices Duj, Dvj are relaced by 
%  the vectors buj, bvj, respectively.
%
% D. Calvetti, E. Somersalo

function [A W] = DiffusionMatrixDistr(n_in,n_out,R,R_inf, ...
                 kappa_in,kappa_out,perm_alpha,n_buff)

N = n_in + n_out + 1;
A = sparse(N*(2 + 2*n_buff),N*(2 + 2*n_buff));
W = sparse(N*(2 + 2*n_buff),2 + 2*n_buff);

% CO2:

[Du0 bu0] = SingleSpeciesDiffMatDistr(n_in,n_out,R,R_inf,kappa_in(1,:), ...
    kappa_out(1,:),perm_alpha(1));

A(1:N,1:N) = Du0;
W(1:N,1) = bu0;

% H+:

[Dv0 bv0] = SingleSpeciesDiffMatDistr(n_in,n_out,R,R_inf,kappa_in(2,:), ...
    kappa_out(2,:),perm_alpha(2));

% Substituting in the matrices
A(N*(n_buff+1)+1:N*(n_buff+2),N*(n_buff+1)+1:N*(n_buff+2)) = Dv0;
W(N*(n_buff+1)+1:N*(n_buff+2),n_buff + 2) = bv0;

% Adding buffers

indj = 2;
for j = 1:n_buff
    % HA_j
    indj = indj + 1;
    [Duj buj] = SingleSpeciesDiffMatDistr(n_in,n_out,R,R_inf,kappa_in(indj,:), ...
        kappa_out(indj,:),perm_alpha(indj));
    % A_j
    indj = indj + 1;
    [Dvj bvj] = SingleSpeciesDiffMatDistr(n_in,n_out,R,R_inf,kappa_in(indj,:), ...
        kappa_out(indj,:),perm_alpha(indj));
    % Substituting in the matrices
    A(N*j+1:N*(j+1),N*j+1:N*(j+1)) = Duj;
    W(N*j+1:N*(j+1),j+1) = buj;
    A(N*(n_buff+j+1)+1:N*(n_buff+j+2),N*(n_buff+j+1)+1:N*(n_buff+j+2)) ...
        = Dvj;
    W(N*(n_buff+j+1)+1:N*(n_buff+j+2),n_buff+2+j) = bvj;
end


    
