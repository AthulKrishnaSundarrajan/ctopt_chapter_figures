import numpy as np
import matplotlib.pyplot as plt
import dill
import os
from scipy.interpolate import CubicSpline as cs


plt.rcParams['font.family'] = 'DeJavu Serif'
plt.rcParams['font.serif'] = ['Times New Roman']

# plot properties
markersize = 10
linewidth = 0.8
buff = 7
fontsize_legend = 16-buff
fontsize_axlabel = 18-buff
fontsize_tick = 16-buff

if __name__ == '__main__':

    # get path to this directory
    this_dir = os.path.dirname(os.path.realpath(__file__))

    # 2. OpenFAST directory that has all the required files to run an OpenFAST simulations
    OF_dir = this_dir 
    lf_warmstart_file = OF_dir + os.sep +'lf_ws_file_zeta.dill'
    hf_warmstart_file = OF_dir + os.sep +  'hf_ws_file_zeta.dill'

    with open(lf_warmstart_file,'rb') as handle:
        lf_res = dill.load(handle)

    with open(hf_warmstart_file,'rb') as handle:
        hf_res = dill.load(handle)

    DV_lf = lf_res['desvars']
    DV_lf  =np.squeeze(np.array(DV_lf))

    DV_hf = hf_res['desvars']
    DV_hf  = np.squeeze(np.array(DV_hf))

    ind_hf = np.argsort(DV_hf)
    ind_lf = np.argsort(DV_lf)

    #DV_hf = hf_res['desvars']
    outputs_hf = hf_res['outputs']
    outputs_lf = lf_res['outputs']
    
    DEL_hf = []
    DEL_lf = []

    gs_max_lf = []
    gs_max_hf = []

    res_mf = 1.8606
    res_lf = 1.853

    res_mf2 = 1.22
    res_lf2 = 1.99020098

    

    for i in range(len(DV_hf)):
        del_hf = outputs_hf[i]['TwrBsMyt_DEL']
        gs_hf = outputs_hf[i]['GenSpeed_Max']
        DEL_hf.append(del_hf)
        gs_max_hf.append(gs_hf)

    for i in range(len(DV_lf)):
        del_lf = outputs_lf[i]['TwrBsMyt_DEL']
        gs_lf = outputs_lf[i]['GenSpeed_Max']
        DEL_lf.append(del_lf)
        gs_max_lf.append(gs_lf)
        
    DEL_hf = np.array(DEL_hf)
    DEL_lf = np.array(DEL_lf)

    gs_max_hf = np.array(gs_max_hf)
    gs_max_lf = np.array(gs_max_lf)

    if False:
        DV_hf = DV_hf[ind_hf]
        DEL_hf = DEL_hf[ind_hf]
        gs_max_hf = gs_max_hf[ind_hf]

        DV_lf = DV_lf[ind_lf]
        DEL_lf = DEL_lf[ind_lf]
        gs_max_lf = gs_max_lf[ind_lf]


        del_hf_l = cs(DV_hf,DEL_hf)([res_lf,res_lf2])
        gs_hf_l = cs(DV_hf,gs_max_hf)([res_lf,res_lf2])

        del_hf_m = cs(DV_hf,DEL_hf)([res_mf,res_mf2])
        gs_hf_m = cs(DV_hf,gs_max_hf)([res_mf,res_mf2])

    
    
    
    fig,ax = plt.subplots(2,1)
    plt.subplots_adjust(hspace=0.3)
    ax[0].plot(DV_hf[:5],DEL_hf[:5],'ko-',label = 'OpenFAST')
    ax[0].plot(DV_lf[:5],DEL_lf[:5],'ro-',label = 'DFSM')
    #ax[0].set_ylim([2.5,10])
    ax[0].set_xlabel('Zeta PC',fontsize = fontsize_axlabel)
    ax[0].set_ylabel('DEL',fontsize = fontsize_axlabel)

    ax[1].plot(DV_hf[:5],gs_max_hf[:5],'ko-',label = 'OpenFAST')
    ax[1].plot(DV_lf[:5],gs_max_lf[:5],'ro-',label = 'DFSM')
    #ax[1].set_ylim([1.15,1.5])
    
    ax[1].text(-0.01,1.23,'constraint = 1.20')
    ax[1].axhline(1.20,ls = '--',color = 'k',alpha = 0.5)
    ax[1].set_xlabel('Zeta PC',fontsize = fontsize_axlabel)
    ax[1].set_ylabel('GenSpeed Max',fontsize = fontsize_axlabel)

    fig.savefig('DVvsVar2.pdf')
    


