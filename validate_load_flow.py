"""
This code is designed to retrieve load flow results from PowerFactory and generate a .csv file containing
the following parameters for each bus: bus_i, voltage magnitude, voltage angle, active power (P), and
reactive power (Q). The exported file can then be used for further analysis, validation, or comparison with
results obtained from other power system tools.
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
Project_name = 'Nine-bus System_JO'


error = app.ActivateProject(Project_name)

if error != 0:
    print('erro na ativação do projeto')
    print(error)
    quit()

all_buses = app.GetCalcRelevantObjects('ElmTerm')

bus_data =[]

##executar o loadflow
ldf = app.GetFromStudyCase('ComLdf')
ldf.Execute()

for bus in all_buses:
    # numero do barramneto
    barr = bus.GetAttribute('loc_name')
    bus_i = int(barr.split()[1])

    #magnitude em p.u.
    mag = round(bus.GetAttribute('m:u'),3)

    #ângulo em graus
    ang = round(bus.GetAttribute('m:phiurel'),3)

    pload = 0
    qload = 0

    all_cubs = bus.GetContents()
    Cubs = [cub for cub in all_cubs if cub.GetClassName() == 'StaCubic']
    for cub in Cubs:
        if (cub.GetAttribute('obj_id') != None):
            if (cub.GetAttribute('obj_id').GetClassName() == 'ElmSym'):
                pload = cub.GetAttribute('obj_id').GetAttribute('m:P:bus1')
                qload = cub.GetAttribute('obj_id').GetAttribute('m:Q:bus1')
            elif (cub.GetAttribute('obj_id').GetClassName() == 'ElmGenstat'):
                pload = cub.GetAttribute('obj_id').GetAttribute('m:P:bus1')
                qload = cub.GetAttribute('obj_id').GetAttribute('m:Q:bus1')

    bus_data.append([bus_i, mag,   ang, pload,  qload])


# ordenar os barramentos da lista de 1 a N
bus_data.sort(key=lambda x: x[0])
old_bus_numbers = [sublist[0] for sublist in bus_data]
for i in range(len(bus_data)):
    bus_data[i][0] = i + 1


# print(bus_data)

with open("dados_power.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(bus_data)
