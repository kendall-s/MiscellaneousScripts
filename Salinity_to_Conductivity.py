""" Script to convert the practical salinity values to conductivity """
# Scrapped code off of https://salinometry.com/stp-conductivity-calculator/

import pandas as pd

def calc_cond(salinity, temperature):
    # Constants
    a0 = 2.86231E-02
    a1 = -1.52423E-04
    a2 = -1.73606E-04
    a3 = 3.82416E-05
    a4 = -4.51350E-06
    a5 = 2.07000E-07
    
    l0 = 1.4970000E-02
    l1 = 3.1700000E-04
    l2 = -4.0000000E-07
    
    b0 = -6.0650000E-07
    b1 = 1.2970000E-06
    b2 = 2.8370000E-07
    b3 = 5.5240000E-08
    b4 = -1.3440000E-08
    b5 = 6.4700000E-10
    
    c0 = 0.6766097
    c1 = 0.0200564
    c2 = 0.0001104259
    c3 = -0.00000069698
    c4 = 0.0000000010031
    
    e1 = 0.03426
    e2 = 4.464E-4
    e3 = 0.4215
    e4 = -0.003107
    
    d1 = 0.002070
    d2 = -6.370e-6
    d3 = 3.989e-9
    
    Salinity = 35.0000  # PSS-78
    Temperature = 24  # ITS-90
    Pressure = 0  # dbar
    
    p = Pressure / 100
    t = 1.00024 * temperature
    
    Rt = 1 + (salinity - 35) * (a0 + a1 * (salinity ** 0.5) + a2 * salinity + a3 * (salinity ** 1.5) + a4 *
                (salinity ** 2) + a5 * (salinity ** 2.5) - ((temperature-15)/(1 + (10 + 11 * (salinity ** 0.5) +
                12 * salinity) * (temperature-15)) * (b0 + b1 * (salinity**0.5) + b2 * salinity + b3 * (salinity**1.5) +
                b4 * (salinity ** 2) + b5 * (salinity**2.5))))
    # 1
    rt = (c0 + c1 * temperature + c2 * temperature * temperature + c3 * temperature * temperature * temperature + c4 *
        temperature * temperature * temperature * temperature)
    
    Rrt = Rt * rt
    # 1.2124058111712948
    
    alpha = (1 * e1 * temperature + e2 * temperature * temperature) / ((e3 + e4 * temperature) * Rrt)
    alpha1 = 1 + alpha
    
    beta = alpha1 * alpha1 + (4 * Pressure * (d1 + d2 * Pressure + d3 * Pressure * Pressure))/((e3 + e4 * temperature) * Rrt)
    
    R = 0.5 * Rrt * (1-alpha + ((beta ** 0.5)))
    C = R * 42.914

    return C

path = 'S:/Marine Technology and Equipment/Hydrochemistry/Hydrochemistry Current/Projects/Salinity Analysis Temperature/Data/CSV/hob2019sal046 - Cal lab.csv'

df = pd.read_csv(path)
conds = []
for x in df['Calculated Salinity']:
    conds.append(calc_cond(x, 24))

print(conds)