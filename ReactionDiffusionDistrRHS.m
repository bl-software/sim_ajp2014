% The RHS for ode solver corresponding to a distributed model, i.e., the
% diffusion and reaction velocities need not be constants
%
% D. Calvetti, E. Somersalo
%
function Y = ReactionDiffusionDistrRHS(t,X,Params)

%disp(['time = ' num2str(t)]);

% Disentangling the model parameters
A      = Params.DiffusionMatrix;
W      = Params.BoundaryVector;
k      = Params.ReactionRates;
X_inf  = Params.BoundaryValues;
N      = Params.N;
n_buff = Params.NumberOfBuffers;

% Diffusion part, including dirichlet boundary values at outer boundary
Y = A*X + W*X_inf;     
                    

% Adding the CO2 feed
Y(1:N)     = Y(1:N)     - k(1,:)'.*X(1:N) + k(2,:)'.*X(N+1:2*N);
Y(N+1:2*N) = Y(N+1:2*N) + k(1,:)'.*X(1:N) - k(2,:)'.*X(N+1:2*N);

% Adding the equilibrium reactions

indj = 2; 
XH = X(N*(n_buff+1)+1:N*(n_buff+2));     % H+ concentration
for j = 1:n_buff
    indj = indj + 1;
    aux = -k(indj,:)'.*X(N*j+1:N*(j+1));
    indj = indj + 1;
    aux = aux + k(indj,:)'.*XH.*X(N*(n_buff+1+j)+1:N*(n_buff+2+j));
    Y(N*j+1:N*(j+1)) = Y(N*j+1:N*(j+1)) + aux;
    Y(N*(n_buff+1+j)+1:N*(n_buff+2+j)) =  ...
        Y(N*(n_buff+1+j)+1:N*(n_buff+2+j)) - aux;
    Y(N*(n_buff+1)+1:N*(n_buff+2)) = Y(N*(n_buff+1)+1:N*(n_buff+2)) - aux;
end
    

