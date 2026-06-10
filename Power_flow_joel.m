clc
clear


mpc = loadcase('case_bus_joel');
% mpc = loadcase('case39M');
% mpc = loadcase('case9');


%verificar se P dos geradores está entre o limites, caso contrário alterar
for i = 1:size(mpc.gen,1)
    %limites
    Pmax = mpc.gen(i,9);
    Pmin = mpc.gen(i,10);

    %valores atuais 
    Pg = mpc.gen(i,2);

    %verificar o P
    if Pg > Pmax
        mpc.gen(i,2) = Pmax; 
    elseif Pg < Pmin
        mpc.gen(i,2) = Pmin;
    end
end


     
% correr o power flow
mpopt = mpoption('verbose', 0, 'pf.enforce_q_lims',1);
results = runpf(mpc, mpopt);

% Guardar valores principais
V = results.bus(:,8);        % magnitude (p.u.)
ang = results.bus(:,9);      % ângulo (graus)

% Potência gerada
Pg = results.gen(:,2);       % MW
Qg = results.gen(:,3);       % MVAr

% Fluxo nas linhas
Pij = results.branch(:,14);  % MW (de -> para)

% Perdas totais
Ploss = sum(results.branch(:,14) + results.branch(:,16));

% Potência líquida injetada

P_inj = zeros(size(results.bus,1),1);

Q_inj = zeros(size(results.bus,1),1);


gen_bus = results.gen(:,1);

for i = 1:length(gen_bus)
    bus_idx = gen_bus(i);
    P_inj(bus_idx) = Pg(i) - P_inj(bus_idx);
    Q_inj(bus_idx) = Qg(i) - Q_inj(bus_idx);
end
% Mostrar resultados
disp('--- Tensões nas barras (p.u.) ---');
disp(V)

disp('--- Ângulos (graus) ---')
disp(ang)

disp('--- Potência gerada (MW) ---')
disp(Pg)

disp('--- Perdas Totais (MW) ---')
disp(Ploss)

%Ficheiro CSV
V = V(:);
ang = ang(:);

aux = (1:length(V))';

aux_2_file = [aux, V, ang, P_inj, Q_inj];

% Guardar ficheiro
writematrix(aux_2_file, 'dados_mat.csv');