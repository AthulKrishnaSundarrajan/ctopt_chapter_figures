import numpy as np;
import matplotlib.pyplot as plt
from mat4py import loadmat
import fatpack

# parameters
bins = 100
slope = 4

# plot properties
markersize = 10
linewidth = 1.5
fontsize_legend = 16
fontsize_axlabel = 18
fontsize_tick = 15

plt.rcParams['font.family'] = 'DeJavu Serif'
plt.rcParams['font.serif'] = ['Times New Roman']

if __name__ == '__main__':

    filename = 'oloc_results.mat'

    results = loadmat(filename)

    Time = np.array(results['T'])
    GP_array = np.array(results['GP_array'])
    Myt_array = np.array(results['Myt_array'])

    GP_mean = np.mean(GP_array,axis = 0)

    elapsed = Time[-1] - Time[0]

    ncases = len(GP_mean)

    DEL = np.zeros((ncases,))

    for i in range(ncases):

        my = Myt_array[:,i]

        F_of, Fmean_of = fatpack.find_rainflow_ranges(my, return_means=True)
        Nrf_of, Frf_of = fatpack.find_range_count(F_of, bins)
        DELs_ = Frf_of ** slope * Nrf_of / elapsed

        DEL[i] = DELs_.sum() ** (1.0 / slope)

    fig,ax = plt.subplots(1)

    ax.plot(GP_mean,DEL,'o-',color = 'k',linewidth = linewidth, markersize = markersize)
    ax.set_ylabel('DEL [kNm]',fontsize = fontsize_axlabel)
    ax.set_xlabel('Avg. Generator Power [kW]',fontsize = fontsize_axlabel)
    ax.grid(alpha = 0.4)
    ax.tick_params(labelsize=fontsize_tick)

    fig.savefig('DELvsPavg.pdf')

    dict_keys  = np.array(['BP_array','GP_array','GS_array','Myt_array','CS_array','WE_array'])
    ylabel_list  = np.array(['Blade Pitch [deg]','Generator Power [kW]','Generator Speed [rpm]','Tower-Base FA Moment [kNM]','Current Speed [m/s]','Wave Elevation [m]'])
    plot_name  = np.array(['bp_mhk','gp_mhk','gs_mhk','myt_mhk','ws_mhk','we_mhk'])
    T = results['T']
    for i,key in enumerate(dict_keys):

        ts_array = np.array(results[key])

        fig,ax = plt.subplots(1,1)

        ax.plot(T,ts_array[:,0],linewidth = linewidth)
        ax.plot(T,ts_array[:,-1],linewidth = linewidth)
        ax.set_xlabel('Time [s]',fontsize = fontsize_axlabel)
        ax.set_xlim([0,800])
        ax.set_ylabel(ylabel_list[i],fontsize = fontsize_axlabel)
        ax.tick_params(labelsize=fontsize_tick)

        fig.savefig(plot_name[i]+'.pdf')



    plt.show()
