% Diffusion matrix in spherical coordinates, radial symmetry
%
% OUTPUT -   D        : sparse nxn matrix
%            coupling : vector of length n
%            boundary : vector of length n
%
% D. Calvetti, E. Somersalo



function [D coupling boundary] = DiffusionMatrixOutsideDistr(n,R,kappa,alpha,R_inf)
fprintf('*          In DiffusionMatrixOutsideDistr_RBC.m *\n')

h = (R_inf - R)/n;

% Interior points
r      = R + [1:n-1]'*h;
rplus  = r + h/2;
rminus = r - h/2;

km     = 0.5*(kappa(2:n)+kappa(1:n-1))';

e      = ones(n-2,1);
Lplus  = spdiags([-e e],[1 2],n-2,n);
Lminus = spdiags([-e e],[0 1],n-2,n);
D_int  = spdiags([km(2:n-1).*rplus(1:n-2).^2],0,n-2,n-2)*Lplus - ...
    spdiags([km(1:n-2).*rminus(1:n-2).^2],0,n-2,n-2)*Lminus;
D_int = (1/h^2)*spdiags([1./r(1:n-2).^2],0,n-2,n-2)*D_int;

% Boundary condition at r = R_inf

D_inf      = zeros(1,n);
D_inf(n)   = -((rplus(n-1)/r(n-1))^2 +(rminus(n-1)/r(n-1))^2)/h^2;
D_inf(n-1) = (rminus(n-1)/r(n-1))^2/h^2;
D_inf      = kappa(n)*sparse(D_inf);

% Boundary point at r = R

D_R  = zeros(1,n);
aux1 = kappa(1)*((R+h/2)/R)^2/h^2;
aux2 = (((R-h/2)/R)^2)/(h*alpha); 

D_R(1) = -(aux1 + aux2);
D_R(2)   = aux1;
D_R      = sparse(D_R);

% Combining the pieces

D = [D_R;D_int;D_inf];

% Boundary terms

coupling = zeros(n,1);
coupling(1) =  aux2;

boundary = zeros(n,1);
boundary(n) = kappa(n)*(1/h^2)*(rplus(n-1)/r(n-1))^2;

fprintf('*          Out DiffusionMatrixOutsideDistr_RBC.m *\n')

