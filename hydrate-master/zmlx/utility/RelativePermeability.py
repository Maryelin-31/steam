# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

"""
Three-Phase Relative Permeability:

The gas/oil and water/oil relative permeability was represented by Corey correlations
The Stone II model was chosen for the three-phase relative permeability correlation because of its simplicity and its bivariate nature, since
the computed oil relative permeability depends on two saturation values: gas and water relative permeabilities.

"""

def stone_model_II(swi, sgc, sorw, sorg, krowe, krwe, kroge, krge, nsorw, nw, nog, ng):
    assert swi < 1
    assert sorw == sorg #Condition for Stone Model
    assert krowe == kroge #Condition for Stone Model
    
    #variables
    slc = swi + sorg
    sw = np.linspace(swi, 1 - sorw, 20, endpoint=True)
    sg = np.linspace(sgc, slc, 20, endpoint=True)
    so = 1 - sg
    
    #Models Corey, 1954
    #Water - Oil System
    krow = krowe * ((1 - sw - sorw) / (1 - swi - sorw))**nsorw
    krw = krwe * ((sw - swi) / (1 - swi - sorw))**nw

    #Plot
    # plt.plot(sw, krw, '--', color='tab:blue', label='krw')
    # plt.plot(sw, krow, '--', color='tab:orange', label='krow')
    # plt.legend()
    
    #Gas - Oil System    
    krog = kroge * ((1 - sg - slc) / (1 - sgc - slc))**nog
    krg = krge * ((sg - sgc) / (1 - slc - sgc))**ng
    krg[krg > 1] = 1
    
    # print(sg)
    # print(krg)
    # plt.plot(sg, krg, '--', color='tab:blue', label='krg')
    # plt.plot(sg, krog, '--', color='tab:orange', label='krog')
    # plt.legend()

    #Stone Model I normalized by Aziz and Settari, 1979
    #swc = swir
    #Fayers and Mattews 1984
    a = 1 - (sg / (1 - swi - sorg))
    som= (a * sorw) + ((1 - a) * sorg)
    s_o = np.abs(so - som) / (1 - swi - som)  # so>= som
    s_w = np.abs(sw - swi) / (1 - swi - som)  # sw >= swir
    s_g = (sg) / (1 - swi - som)

    s_o[s_o >= 1.0] = 1 - swi
    s_w[s_w >= 1.0] = 1 - sorw
    s_g[s_g >= 1.0] = 1 - sorg

       
    kro = krowe * ( (krow / krowe + krw) * (krog / kroge + krg) - (krw + krg) )
    kro[kro < 0] = 0
    # print(kro)
    return sw, krw, sg, krg, so, kro
# sw, krw, sg, krg, so, kro = stone_model_II(swi = 0.25, sgc = 0.05, sorw = 0.35, sorg = 0.35, krowe = 0.85, krwe = 0.4, kroge = 0.85, krge = 2, nsorw = 2, nw = 2, nog = 6, ng = 4)


# plt.plot(sg, kro,'--', color='tab:blue',label='$\mathregular{K_{rw}}$')
# plt.plot(sg, kro,'--', color='tab:orange',label='$\mathregular{K_{rg}}$')
# plt.grid()
# plt.ylabel('Relative Permeability')
# plt.xlabel('Gas Saturation')
# plt.legend()



