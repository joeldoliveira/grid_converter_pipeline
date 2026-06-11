"""
This code is designed to extract the data from an ElmSym object in PowerFactory and store its parameters. It
then creates a corresponding ElmGenStat object, assigns the same parameter values to the new element,
and finally removes the original ElmSym object from the network model.
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

# Primeiro retirar todos as maquinas sincronas e depois tudo o que e referente a elas

gen_data = []

all_generator = app.GetCalcRelevantObjects('ElmSym')
for gen in all_generator:
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
    mbase = round(gen.GetAttribute('typ_id').GetAttribute('sgn'), 4)
    #maximum real power output
    pmaxuc = gen.GetAttribute('Pmax_uc')
    #minimum real power output
    pminuc = gen.GetAttribute('Pmin_uc')

    pmax = gen.GetAttribute('P_max')
    ratingfactor = gen.GetAttribute('pmaxratf')
    grid = gen.GetAttribute('cpGrid')
    ratedpow = gen.GetAttribute('typ_id').GetAttribute('cosn')
    refer = gen.GetAttribute('ip_ctrl')


#     gen_data.append([aux, cub, grid, pg, qg, qmax, qmin, vg, mbase, pmaxuc, pminuc, ratingfactor, vrated, ratedpow, refer])
#
# print(gen_data)

    old_gen = gen
    cub = gen.GetAttribute('bus1')
    parent = old_gen.GetParent()

    namegenstat = aux.replace('sym', 'genstat')

    newgenstat = parent.CreateObject('ElmGenstat', namegenstat)
    print(parent.GetAttribute('loc_name'))


    if newgenstat is not None:
        newgenstat.SetAttribute('bus1', cub)
        newgenstat.SetAttribute('pgini', pg)
        newgenstat.SetAttribute('qgini', qg)
        newgenstat.SetAttribute('usetp', vg)
        newgenstat.SetAttribute('cQ_max', qmax)
        newgenstat.SetAttribute('cQ_min', qmin)
        newgenstat.SetAttribute('Pmax_uc', pmaxuc)
        newgenstat.SetAttribute('Pmin_uc', pminuc)
        newgenstat.SetAttribute('P_max', pmax)
        newgenstat.SetAttribute('pmaxratf', ratingfactor)
        newgenstat.SetAttribute('cosn', ratedpow)
        newgenstat.SetAttribute('sgn', mbase)
        newgenstat.SetAttribute('ip_ctrl', refer)

    old_gen.Delete()
