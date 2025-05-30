% Diffusion matrix in spherical coordinates, radial symmetry. The vector
% coupling multiplies the first component of the diffusion solution outside
% the cell, thus serving as a coupling between the inside and outside
% solutions
%
% OUTPUT -   D        : sparse (n+1)x(n+1) matrix
%            coupling : coupling vector of length (n+1)
%
% D. Calvetti, E. Somersalo

function [D coupling] = DiffusionMatrixInsideDistr(n,R,kappa,perm_alpha)

h = R/n;

% Interior points
r      = [1:n]'*h;
rplus  = r + h/2;
rminus = r - h/2;
km     = 0.5*(kappa(2:n+1)+kappa(1:n))';
e      = ones(n-1,1);
Lplus  = spdiags([-e e],[1 2],n-1,n+1);
Lminus = spdiags([-e e],[0 1],n-1,n+1);
D_int   = spdiags([km(2:n).*rplus(1:n-1).^2],0,n-1,n-1)*Lplus - ...
    spdiags([km(1:n-1).*rminus(1:n-1).^2],0,n-1,n-1)*Lminus;
D_int = (1/h^2)*spdiags([1./r(1:n-1).^2],0,n-1,n-1)*D_int;

% Boundary point at r = 0

D_0    = zeros(1,n+1);
D_0(1) = -2/h^2;
D_0(2) =  2/h^2;
D_0    = kappa(1)*sparse(D_0);

% Boundary point at r = R

D_R      = zeros(1,n+1);
aux1 = kappa(n+1)*(rminus(n)/r(n))^2/h^2;
aux2 = ((rplus(n)/r(n))^2)/(h*perm_alpha); 
D_R(n+1) = -(aux1 + aux2);
D_R(n)   = aux1;
D_R      = sparse(D_R);

% Combining the pieces

D = [D_0;D_int;D_R];

% Boundary term defining the coupling

coupling      = zeros(n+1,1);
coupling(n+1) =  aux2;





