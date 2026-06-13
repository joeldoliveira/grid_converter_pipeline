"""
This code is designed to extract network data from PowerFactory and organize it into three matrices: Bus
Data, Gen Data, and Branch Data. The resulting data is then exported to a MATLAB file compatible with the
MATPOWER library, enabling power flow calculations and further power system analysis.
"""

####Power factory related initializations
import math
import sys

import numpy as np

# Add the path to the PowerFactory Python folder (the folder containing powerfactory.pyd)
sys.path.append(r"C:\path\to\your\folder")
import powerfactory

try:
    app = powerfactory.GetApplicationExt('francisco.s.fernande')
except powerfactory.ExitError as error:
    print(error)
    print('error.code = %d' % error.code)

# Project_name = '39_Bus_Mix_PMU_JO_V2'
Project_name = 'Nine-bus System_JO'

error = app.ActivateProject(Project_name)

if error != 0:
    print('erro na ativação do projeto')
    print(error)
    quit()

sbase = 100 ##MVA  global variable
ndec = 5

############################################matriz de informações de barramnetros############################################


all_buses = app.GetCalcRelevantObjects('ElmTerm')

bus_data =[]

for bus in all_buses:

    #todos os barramentos i
    barr = bus.GetAttribute('loc_name')
    bus_i = int(barr.split()[1])

    #tipo de barramentos 1-PQ;2-PV;3-reference busM;4-isolated bus

    type = 1

    pd=0
    qd=0
    # potência da carga
    #pedir todos os objetos ou cubiculos do barramento:
    cubs = bus.GetContents()
    cubs_with_loads = []
    for cub in cubs:
        if (cub.GetAttribute('obj_id') != None):

            #----------reference busbar
            if(cub.GetAttribute('obj_id').GetClassName() == 'ElmSym' or cub.GetAttribute('obj_id').GetClassName() == 'ElmGenstat' ):
                if(cub.GetAttribute('obj_id').GetAttribute('ip_ctrl') == 1):
                    type = 3
                elif (cub.GetAttribute('obj_id').GetAttribute('av_mode') == 'constv'):
                    type = 2
                elif (cub.GetAttribute('obj_id').GetAttribute('av_mode') == 'constq'):
                    type = 1


            if(cub.GetAttribute('obj_id').GetClassName() == 'ElmLod'):
                lod_elm = cub.GetAttribute('obj_id')
                pd = round(lod_elm.GetAttribute('plini'), ndec)
                qd = round(lod_elm.GetAttribute('qlini'), ndec)


    # #shunt condutance
    gs = 0
    # #shunt susceptance
    bs = 0

    area = 1
    vm = 1
    va = 0


    #tensão nominal do barramento
    basekv = round(bus.GetAttribute('uknom'), ndec)


    zone = 1
    #tensão max
    vmax = 1.06
    #tensão min
    vmin = 0.94
    #print(bus_i,type,pd,qd,gs,bs,area,vm,va,basekv,zone,vmax,vmin)



    bus_data.append([bus_i, type,   pd, qd, gs, bs, area, vm, va, basekv, zone, vmax, vmin])





#ordenar os barramentos da lista de 1 a N
bus_data.sort(key=lambda x: x[0])
old_bus_numbers = [sublist[0] for sublist in bus_data]
for i in range(len(bus_data)):
    bus_data[i][0] = i + 1
bus_data = [[item for item in sublist] for sublist in bus_data]





# bus_data = np.array(bus_data).astype(float)
#print(bus_data)


############################################matriz de informações de gerador############################################

gen_data = []

all_genwind = app.GetCalcRelevantObjects('ElmGenstat')
for genwind in all_genwind:

    text = genwind.GetAttribute('bus1').GetAttribute('cterm').GetAttribute('loc_name')
    bus = int(text.split()[1])
    bus = old_bus_numbers.index(bus)+1

    #real output power
    pg = round(genwind.GetAttribute('pgini'), ndec)
    #reactive power output
    qg = round(genwind.GetAttribute('qgini'), ndec)
    #maximum reactive power output
    qmax = round(genwind.GetAttribute('cQ_max'), ndec)
    #minimum reactive power output
    qmin = round(genwind.GetAttribute('cQ_min'), ndec)
    #voltage magnitude setpoint
    vg = round(genwind.GetAttribute('usetp'), ndec)
    #total MVA base of this machine
    mbase = round(genwind.GetAttribute('sgn'), ndec)
    #> 0 - machine in service; <= 0 - machine out of service
    status = 1 #genwind.GetAttribute('outserv')
    #maximum real power output
    pmax = genwind.GetAttribute('Pmax_uc')
    #minimum real power output
    pmin = genwind.GetAttribute('Pmin_uc')
    pc1 = 0
    pc2 = 0
    qc1min = 0
    qc1max = 0
    qc2min = 0
    qc2max = 0
    ramp_agc = 0
    ramp_10 = 0
    ramp_30 = 0
    ramp_q = 0
    apf = 0

    #print(text,pg,qg,qmax,qmin,vg,mbase,status,pmax,pmin,pc1,pc2,qc1min,qc1max,qc2min,qc2max,ramp_agc,ramp_10,ramp_30,ramp_q,apf)


    gen_data.append([bus, pg, qg, qmax, qmin, vg, mbase, status, pmax, pmin, pc1, pc2, qc1min, qc1max, qc2min, qc2max, ramp_agc, ramp_10, ramp_30, ramp_q, apf])
    gen_data.sort(key=lambda x: x[0])



all_generator = app.GetCalcRelevantObjects('ElmSym')
for gen in all_generator:

    text = gen.GetAttribute('bus1').GetAttribute('cterm').GetAttribute('loc_name')
    bus = int(text.split()[1])

    # real output power
    pg = round(gen.GetAttribute('pgini'), ndec)
    # reactive power output
    qg = round(gen.GetAttribute('qgini'), ndec)
    # maximum reactive power output
    qmax = round(gen.GetAttribute('cQ_max'), ndec)
    # minimum reactive power output
    qmin = round(gen.GetAttribute('cQ_min'), ndec)
    # voltage magnitude setpoint
    vg = round(gen.GetAttribute('usetp'), ndec)
    # total MVA base of this machine
    mbase = round(gen.GetAttribute('typ_id').GetAttribute('sgn'), ndec)
    # > 0 - machine in service; <= 0 - machine out of service
    status = gen.GetAttribute('outserv')
    status = int(not(status))
    # maximum real power output
    pmax = gen.GetAttribute('Pmax_uc')
    # minimum real power output
    pmin = gen.GetAttribute('Pmin_uc')
    pc1 = 0
    pc2 = 0
    qc1min = 0
    qc1max = 0
    qc2min = 0
    qc2max = 0
    ramp_agc = 0
    ramp_10 = 0
    ramp_30 = 0
    ramp_q = 0
    apf = 0

    #print(text,pg,qg,qmax,qmin,vg,mbase,status,pmax,pmin,pc1,pc2,qc1min,qc1max,qc2min,qc2max,ramp_agc,ramp_10,ramp_30,ramp_q,apf)

    gen_data.sort(key=lambda x: x[0])
    gen_data.append([bus, pg, qg, qmax, qmin, vg, mbase, status, pmax, pmin, pc1, pc2, qc1min, qc1max, qc2min, qc2max,ramp_agc, ramp_10, ramp_30, ramp_q, apf])

#gen_data = np.array(gen_data)##.astype(float)
#print(gen_data)



############################################matriz de informacão de branch data############################################

branch_data =[]

all_lines = app.GetCalcRelevantObjects('ElmLne')
for line in all_lines:

    # from bus
    text1 = line.GetAttribute('bus1').GetAttribute('cterm').GetAttribute('loc_name')
    fbus = int(text1.split()[1])

    # to bus
    text2 = line.GetAttribute('bus2').GetAttribute('cterm').GetAttribute('loc_name')
    tbus = int(text2.split()[1])

    vbase = line.GetAttribute('typ_id').GetAttribute('uline')
    zbase = (vbase * vbase)/sbase

    #resistance(p.u.)
    r = round(line.GetAttribute('R1')/zbase, ndec)
    x = round(line.GetAttribute('X1')/zbase, ndec)
    b = round(line.GetAttribute('typ_id').GetAttribute('bline')*line.GetAttribute('dline')*10e-7*zbase, ndec)

    #MVA rating A
    rate_a = int(line.GetAttribute('typ_id').GetAttribute('uline') * line.GetAttribute('typ_id').GetAttribute('sline') * math.sqrt(3))
    rate_b = rate_a
    rate_c = rate_a
    #transformer off nominal turns ratio
    ratio = 0
    #transformer phase shift angle(degrees)
    angle = 0 #line.GetAttribute('phik0')
    #initial branch status (1-in service;0-out of service)
    status = 1 #line.GetAttribute('outserv')
    #minimum angle difference
    angmin = -360
    #maximum angle difference
    angmax = 360


    #print(fbus,tbus,r,x,b,rate_a,rate_b,rate_c,ratio,angle,status,angmin,angmax)

    branch_data.sort(key=lambda x: x[0])
    branch_data.append([fbus, tbus, r, x, b, rate_a, rate_b, rate_c, ratio, angle, status, angmin, angmax])

all_tr = app.GetCalcRelevantObjects('ElmTr2')
for tr in all_tr:

    n_par = tr.GetAttribute('ntnum')

    # from bus
    test1 = tr.GetAttribute('bushv').GetAttribute('cterm').GetAttribute('loc_name')
    fbus = int(test1.split()[1])

    # to bus
    test2 = tr.GetAttribute('buslv').GetAttribute('cterm').GetAttribute('loc_name')
    tbus = int(test2.split()[1])

    tbus = old_bus_numbers.index(tbus)+1


    vbase = tr.GetAttribute('typ_id').GetAttribute('utrn_h')
    sbasetr = tr.GetAttribute('typ_id').GetAttribute('strn')
    zbase1 = (vbase * vbase) / sbasetr

    rsi = tr.GetAttribute('typ_id').GetAttribute('r1pu') * zbase1
    xsi = tr.GetAttribute('typ_id').GetAttribute('x1pu') * zbase1

    zbase = (vbase * vbase) / sbase


    #resistance(p.u.)
    r = round((rsi / zbase)/n_par, ndec)
    x = round((xsi / zbase)/n_par, ndec)
    b = 0

    #MVA rating A
    rate_a = int(tr.GetAttribute('typ_id').GetAttribute('strn')*n_par)
    rate_b = rate_a
    rate_c = rate_a
    # transformer off nominal turns ratio
    vf = tr.GetAttribute('typ_id').GetAttribute('utrn_h')
    vt = tr.GetAttribute('typ_id').GetAttribute('utrn_l')
    ratio = 1
    # transformer phase shift angle(degrees)
    angle_aux = tr.GetAttribute('typ_id').GetAttribute('nt2ag')
    angle = angle_aux * 30
    angle = 0
    # initial branch status (1-in service;0-out of service)
    status = 1 #tr.GetAttribute('outserv')

    # minimum angle difference
    angmin = -360
    # maximum angle difference
    angmax = 360

    branch_data.sort(key=lambda x: x[0])
    branch_data.append([fbus, tbus, r, x, b, rate_a, rate_b, rate_c, ratio, angle, status, angmin, angmax])

#branch_data = np.array(branch_data)##.astype(float)
#print(branch_data)


## para escrever para um ficheiro em Matlab
matlab_file = "case_bus_joel.m"

with open (matlab_file, "w", encoding="utf-8") as f:
    # escrever conteudo
    f.write("function mpc = case_bus_joel")
    f.write("\n""%CASE39M")
    f.write("\n""\n""%% MATPOWER Case Format : Version 2")
    f.write("\n""mpc.version = '2';")
    f.write("\n""\n""%%-----  Power Flow Data  -----%%")
    f.write("\n""%% system MVA base")
    f.write("\n""mpc.baseMVA = 100;")

    # escrever matriz de informações de barramnetros em .m
    f.write("\n""\n""%% bus data")
    f.write("\n""%    bus_i    type    Pd  Qd  Gs  Bs  area    Vm  Va  baseKV  zone    Vmax    Vmin")
    f.write("\n""mpc.bus = [""\n")
    for bus_line in bus_data:
        aux_string1 = ""
        for elm in bus_line:
            aux_string1 = aux_string1 +'  '+ str(elm)

        f.write(aux_string1 + ";"+"\n")
    f.write("];""\n")

    #escrever matriz de informações de gerador em .m
    f.write("\n%% generator data")
    f.write("\n""%    bus Pg  Qg  Qmax    Qmin    Vg  mBase   status  Pmax    Pmin    Pc1 Pc2 Qc1min  Qc1max  Qc2min  Qc2max  ramp_agc    ramp_10 ramp_30 ramp_q  apf")
    f.write("\n""mpc.gen = [""\n")
    for gen_line in gen_data:
        aux_string2 = ""
        for elm in gen_line:
            aux_string2 = aux_string2 +'  '+ str(elm)

        f.write(aux_string2 + ";"+"\n")
    f.write("];""\n")


    #escrevermatriz de informacão de branch data em .m
    f.write("\n""%% branch data")
    f.write("\n""%  fbus    tbus    r   x   b   rateA   rateB   rateC   ratio   angle   status  angmin  angmax")
    f.write("\n""mpc.branch = [""\n")
    for branch_line in branch_data:
        aux_string3 = ""
        for elm in branch_line:
            aux_string3 = aux_string3 +'  '+ str(elm)

        f.write(aux_string3 + ";"+"\n")
    f.write("];""\n")
