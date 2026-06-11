"""
This code is designed to extract the data from an ElmGenStat object in PowerFactory and store its parameters. It
then creates a corresponding ElmSym object, assigns the same parameter values to the new element,
and finally removes the original ElmGenStat object from the network model.
"""

import pandas as pd
####Power factory related initializations
import math
import sys
import csv
import numpy as np

sys.path.append(r"C:\Program Files\DIgSILENT\PowerFactory 2025 SP3\Python\3.9")
import powerfactory

try:
    app = powerfactory.GetApplicationExt('francisco.s.fernande')
except powerfactory.ExitError as error:
    print(error)
    print('error.code = %d' % error.code)

# Project_name = '39_Bus_Mix_PMU_JO_V2'
# Project_name = 'Nine-bus System_JO'
Project_name = 'IEEE_240bus_system_JO(1)'


error = app.ActivateProject(Project_name)

if error != 0:
    print('erro na ativação do projeto')
    print(error)
    quit()



#Primeiro retirar todos as maquinas sincronas e depois tudo o que e referente a elas

gen_data = []

all_genwind = app.GetCalcRelevantObjects('ElmGenstat')
for gen in all_genwind:

    aux = gen.GetAttribute('loc_name')


    #real output power
    pg = round(gen.GetAttribute('pgini'), 4)
    #reactive power output
    qg = round(gen.GetAttribute('qgini'), 4)
    #maximum reactive power output
    qmax = round(gen.GetAttribute('cQ_max'), 4)
    #minimum reactive power output
    qmin = round(gen.GetAttribute('cQ_min'), 4)
    #voltage magnitude setpoint
    vg = round(gen.GetAttribute('usetp'), 4)
    #total MVA base of this machine
    mbase = round(gen.GetAttribute('sgn'), 4)
    #maximum real power output
    pmaxuc = gen.GetAttribute('Pmax_uc')
    #minimum real power output
    pminuc = gen.GetAttribute('Pmin_uc')

    pmax = gen.GetAttribute('P_max')
    ratingfactor = gen.GetAttribute('pmaxratf')
    grid = gen.GetAttribute('cpGrid')
    vrated = 20
    ratedpow = gen.GetAttribute('cosn')


#     gen_data.append([namesym, grid, pg, qg, qmax, qmin, vg, mbase, pmaxuc, pminuc, ratingfactor, vrated, ratedpow])
#
# print(gen_data)

    old_gen = gen
    cub = gen.GetAttribute('bus1')
    parent = old_gen.GetParent()

    namesym = aux.replace('genstat', 'sym')
    nametyp = aux.replace('genstat', 'tsym')

    newsym = parent.CreateObject('ElmSym', namesym)
    print(parent.GetAttribute('loc_name'))
    newtyp = parent.CreateObject('TypSym', nametyp)


    if newtyp is not None:
        newtyp.SetAttribute('sgn', mbase)
        newtyp.SetAttribute('ugn', vrated)
        newtyp.SetAttribute('cosn', ratedpow)

    if newsym is not None:
        if newtyp is not None:
            newsym.SetAttribute('typ_id', newtyp)

        newsym.SetAttribute('bus1', cub)
        newsym.SetAttribute('pgini', pg)
        newsym.SetAttribute('qgini', qg)
        newsym.SetAttribute('usetp', vg)
        newsym.SetAttribute('cQ_max', qmax)
        newsym.SetAttribute('cQ_min', qmin)
        newsym.SetAttribute('Pmax_uc', pmaxuc)
        newsym.SetAttribute('Pmin_uc', pminuc)
        newsym.SetAttribute('P_max', pmax)
        newsym.SetAttribute('pmaxratf', ratingfactor)
        # newsym.SetAttribute('cpGrid', grid)

    old_gen.Delete()
