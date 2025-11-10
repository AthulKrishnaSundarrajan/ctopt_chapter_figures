import pickle
import os
import matplotlib.pyplot as plt
import numpy as np
from rosco.toolbox.ofTools.util.spectral import fft_wrap
plt.rcParams['font.family'] = 'DeJavu Serif'
plt.rcParams['font.serif'] = ['Times New Roman']

# plot properties
markersize = 10
linewidth = 0.8
buff = 7
fontsize_legend = 16-buff
fontsize_axlabel = 18-buff
fontsize_tick = 16-buff



def plot_range(sum_stats_of,sum_stats_dfsm,key_qtys,CS):

    '''
    Function to loop through and plot the mean value and range of the signals in the key_qtys list
    '''

    

    fig,ax = plt.subplots(1,3,figsize = (10,3))

    range_dict = {}
    range_dict['CS'] = CS

    for i,qty in enumerate(key_qtys):


        # get mean, min and max, reshape and find the average
        mean_of_array = sum_stats_of[qty]['mean'];mean_of_array = np.reshape(mean_of_array,[n_seeds,n_cs],order = 'F');mean_of_array = np.mean(mean_of_array,axis = 0)
        min_of_array = sum_stats_of[qty]['min'];min_of_array = np.reshape(min_of_array,[n_seeds,n_cs],order = 'F');min_of_array = np.mean(min_of_array,axis = 0)
        max_of_array = sum_stats_of[qty]['max'];max_of_array = np.reshape(max_of_array,[n_seeds,n_cs],order = 'F');max_of_array = np.mean(max_of_array,axis = 0)

        mean_dfsm_array = sum_stats_dfsm[qty]['mean'];mean_dfsm_array = np.reshape(mean_dfsm_array,[n_seeds,n_cs],order = 'F');mean_dfsm_array = np.mean(mean_dfsm_array,axis = 0)
        min_dfsm_array = sum_stats_dfsm[qty]['min'];min_dfsm_array = np.reshape(min_dfsm_array,[n_seeds,n_cs],order = 'F');min_dfsm_array = np.mean(min_dfsm_array,axis = 0)
        max_dfsm_array = sum_stats_dfsm[qty]['max'];max_dfsm_array = np.reshape(max_dfsm_array,[n_seeds,n_cs],order = 'F');max_dfsm_array = np.mean(max_dfsm_array,axis = 0)

        # find lower and upper error limits
        qty_of_lower = mean_of_array - min_of_array
        qty_of_upper = max_of_array - mean_of_array
        qty_of_mean = mean_of_array

        qty_dfsm_lower = mean_dfsm_array - min_dfsm_array
        qty_dfsm_upper = max_dfsm_array - mean_dfsm_array
        qty_dfsm_mean = mean_dfsm_array

        array_ = [{'qty_of_mean':qty_of_mean,'qty_of_lower':qty_of_lower,'qty_of_upper':qty_of_upper,
            'qty_dfsm_mean':qty_dfsm_mean,'qty_dfsm_lower':qty_dfsm_lower,'qty_dfsm_upper':qty_dfsm_upper}]

        if qty == 'BldPitch1':

            range_dict['bladepitch_array'] = array_

        elif qty == 'GenPwr':
            range_dict['genpwr_array'] = array_

        elif qty == 'TwrBsMyt':
            range_dict['twrbsmyt_array'] = array_

        
        # plot
        
        ax[i].errorbar(CS,qty_of_mean,
                                    yerr = [qty_of_lower,qty_of_upper],
                                    fmt =fmt, capsize=capsize, alpha = alpha,color = 'k')
            
        ax[i].errorbar(CS,qty_dfsm_mean,
                                    yerr = [qty_dfsm_lower,qty_dfsm_upper],
                                    fmt =fmt, capsize=capsize, alpha = alpha,color = 'r')
            
        ax[i].scatter(CS,qty_of_mean,marker = 'o',
                            s = 20, color = 'k')
            
        ax[i].scatter(CS,qty_dfsm_mean,marker = 'o',
                            s = 20, color = 'r')
        
        ax[i].set_xlabel('Current Speed [m/s]',fontsize = fontsize_axlabel)
        ax[i].tick_params(labelsize=fontsize_tick)

        if qty == 'BldPitch1':
            title = 'Blade Pitch [deg]'

        elif qty == 'GenPwr':
            title = 'Generator Power [kW]'

        elif qty == 'TwrBsMyt':
            title = 'Tower-Base FA Moment [MNm]'

        else:
            title = qty
        ax[i].set_title(title,fontsize = fontsize_axlabel)

    fig.savefig('range.pdf')
    plt.close(fig)

    return range_dict


if __name__ == '__main__':

    # path to this directory
    this_dir= os.path.dirname(os.path.abspath(__file__))
    save_flag = True

    # path to the directory with the closed-loop validation results
    results_folder = this_dir +os.sep+ 'outputs'+ os.sep +'CL_val1'

    # stored results
    results_file =results_folder + os.sep+'DFSM_validation_results.pkl'
    timeseries_file = results_folder + os.sep+'ts_dict.pkl'


    with open(results_file,'rb') as handle:
        results_dict = pickle.load(handle)

    with open(timeseries_file,'rb') as handle:
        ts_dict = pickle.load(handle)

    color_of = 'k'
    color_dfsm = 'r'
    fig,ax = plt.subplots(2,3,figsize=(10, 5))
    plt.subplots_adjust(hspace=0.3)
    time = ts_dict['time']

    #-------------------------------------------------------------
    curr_speed = ts_dict['currspeed_array'][0]['RtVAvgxh']
    i,j = 0,0
    ax[i,j].plot(time,curr_speed,color = color_of,linewidth = linewidth)
    ax[i,j].set_title('Current Speed [m/s]',fontsize = fontsize_axlabel)
    
    ax[i,j].tick_params(labelsize=fontsize_tick)
    ax[i,j].set_xlim([0,600])

    j = 1
    bp_of = ts_dict['bladepitch_array'][0]['OpenFAST']
    bp_dfsm = ts_dict['bladepitch_array'][0]['DFSM']
    ax[i,j].plot(time,bp_of,color = color_of,linewidth = linewidth)
    ax[i,j].plot(time,bp_dfsm,color = color_dfsm,linewidth = linewidth)
    ax[i,j].set_title('Blade Pitch [deg]',fontsize = fontsize_axlabel)
    
    ax[i,j].tick_params(labelsize=fontsize_tick)
    ax[i,j].set_xlim([0,600])

    j = 2
    bp_of = ts_dict['genpwr_array'][0]['OpenFAST']
    bp_dfsm = ts_dict['genpwr_array'][0]['DFSM']
    ax[i,j].plot(time,bp_of,color = color_of,linewidth = linewidth)
    ax[i,j].plot(time,bp_dfsm,color = color_dfsm,linewidth = linewidth)
    ax[i,j].set_title('Generator Power [kW]',fontsize = fontsize_axlabel)
    
    ax[i,j].tick_params(labelsize=fontsize_tick)
    ax[i,j].set_xlim([0,600])


    i = 1;j = 0
    bp_of = ts_dict['ptfmpitch_array'][0]['OpenFAST']
    bp_dfsm = ts_dict['ptfmpitch_array'][0]['DFSM']
    ax[i,j].plot(time,bp_of,color = color_of,linewidth = linewidth)
    ax[i,j].plot(time,bp_dfsm,color = color_dfsm,linewidth = linewidth)
    ax[i,j].set_title('Platform Pitch [deg]',fontsize = fontsize_axlabel)
    ax[i,j].set_xlabel('Time [s]',fontsize = fontsize_axlabel)
    ax[i,j].tick_params(labelsize=fontsize_tick)
    ax[i,j].set_xlim([300,550])

    j = 1
    bp_of = ts_dict['ptfmheave_array'][0]['OpenFAST']
    bp_dfsm = ts_dict['ptfmheave_array'][0]['DFSM']
    ax[i,j].plot(time,bp_of,color = color_of,linewidth = linewidth)
    ax[i,j].plot(time,bp_dfsm,color = color_dfsm,linewidth = linewidth)
    ax[i,j].set_title('Platform Heave [m]',fontsize = fontsize_axlabel)
    ax[i,j].set_xlabel('Time [s]',fontsize = fontsize_axlabel)
    ax[i,j].tick_params(labelsize=fontsize_tick)
    ax[i,j].set_xlim([300,550])

    j = 2
    bp_of = ts_dict['twrbsmyt_array'][0]['OpenFAST']
    bp_dfsm = ts_dict['twrbsmyt_array'][0]['DFSM']
    ax[i,j].plot(time,bp_of,color = color_of,linewidth = linewidth)
    ax[i,j].plot(time,bp_dfsm,color = color_dfsm,linewidth = linewidth)
    ax[i,j].set_title('Tower-Base FA Moment [MNm]',fontsize = fontsize_axlabel)
    ax[i,j].set_xlabel('Time [s]',fontsize = fontsize_axlabel)
    ax[i,j].tick_params(labelsize=fontsize_tick)
    ax[i,j].set_xlim([300,550])

    fig.savefig('timeseries.pdf')

    PSD_dict = {}
    #-------------------------------------------------------------
    fig,ax = plt.subplots(1,3,figsize = (10,3))

    bp_of = ts_dict['bladepitch_array'][0]['OpenFAST']
    bp_dfsm = ts_dict['bladepitch_array'][0]['DFSM']

    

    xf,FFT_of,_ = fft_wrap(time,bp_of,averaging = 'Welch',averaging_window= 'hamming')
    xf,FFT_dfsm,_ = fft_wrap(time,bp_dfsm,averaging = 'Welch',averaging_window= 'hamming')

    PSD_dict['xf'] = xf
    bladepitch_array = [{'OpenFAST':FFT_of,'DFSM':FFT_dfsm}]
    PSD_dict['bladepitch_array'] = bladepitch_array

    i = 0;j = 0
    ax[j].loglog(xf,np.sqrt(FFT_of),color = color_of,label = 'OpenFAST')
    ax[j].loglog(xf,np.sqrt(FFT_dfsm),color = color_dfsm,label = 'DFSM')
    ax[j].set_xlabel('Freq [Hz]',fontsize = fontsize_axlabel)
    ax[j].set_title('Blade Pitch PSD',fontsize = fontsize_axlabel)
    #ax[j].legend(ncol = 2,fontsize = fontsize_legend)
    ax[j].tick_params(labelsize=fontsize_tick)

    #-------------------------------------------------------------
    bp_of = ts_dict['genpwr_array'][0]['OpenFAST']
    bp_dfsm = ts_dict['genpwr_array'][0]['DFSM']

    xf,FFT_of,_ = fft_wrap(time,bp_of,averaging = 'Welch',averaging_window= 'hamming')
    xf,FFT_dfsm,_ = fft_wrap(time,bp_dfsm,averaging = 'Welch',averaging_window= 'hamming')

    genpwr_array = [{'OpenFAST':FFT_of,'DFSM':FFT_dfsm}]
    PSD_dict['genpwr_array'] = genpwr_array

    j = 1
    ax[j].loglog(xf,np.sqrt(FFT_of),color = color_of,label = 'OpenFAST')
    ax[j].loglog(xf,np.sqrt(FFT_dfsm),color = color_dfsm,label = 'DFSM')
    ax[j].set_xlabel('Freq [Hz]',fontsize = fontsize_axlabel)
    ax[j].set_title('Generator Power PSD',fontsize = fontsize_axlabel)
    #ax[j].legend(ncol = 2,fontsize = fontsize_legend)
    ax[j].tick_params(labelsize=fontsize_tick)
    #-------------------------------------------------------------
    bp_of = ts_dict['twrbsmyt_array'][0]['OpenFAST']
    bp_dfsm = ts_dict['twrbsmyt_array'][0]['DFSM']

    xf,FFT_of,_ = fft_wrap(time,bp_of,averaging = 'Welch',averaging_window= 'hamming')
    xf,FFT_dfsm,_ = fft_wrap(time,bp_dfsm,averaging = 'Welch',averaging_window= 'hamming')

    twrbsmyt_array = [{'OpenFAST':FFT_of,'DFSM':FFT_dfsm}]
    PSD_dict['twrbsmyt_array'] = twrbsmyt_array

    j = 2
    ax[j].loglog(xf,np.sqrt(FFT_of),color = color_of,label = 'OpenFAST')
    ax[j].loglog(xf,np.sqrt(FFT_dfsm),color = color_dfsm,label = 'DFSM')
    ax[j].set_xlabel('Freq [Hz]',fontsize = fontsize_axlabel)
    ax[j].set_title('Tower-Base FA Moment PSD',fontsize = fontsize_axlabel)
    #ax[j].legend(ncol = 2,fontsize = fontsize_legend)
    ax[j].tick_params(labelsize=fontsize_tick)

    fig.savefig('PSD.pdf')

    #---------------------------------------------------------

    # key quantities
    key_qtys = ['BldPitch1','GenPwr','TwrBsMyt']
    
    sum_stats_of = results_dict['summary_stats_of']
    sum_stats_dfsm = results_dict['summary_stats_dfsm']


    n_cs = 7
    n_seeds = 6

    CS = [1.5,1.75,2.0,2.25,2.5,2.75,3.0]

    range_dict = plot_range(sum_stats_of,sum_stats_dfsm,key_qtys,CS)

    results_dict = {'ts_dict':ts_dict,'PSD_dict':PSD_dict,'range_dict':range_dict}

    with open('simulation_results.pkl','wb') as handle:
        pickle.dump(results_dict,handle)



    

