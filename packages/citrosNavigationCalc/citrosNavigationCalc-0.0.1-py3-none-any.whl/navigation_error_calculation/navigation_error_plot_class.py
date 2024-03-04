import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
from citros_data_analysis import data_access as da
from citros_data_analysis import error_analysis as analysis
from prettytable import PrettyTable, ALL
from navigation_error_class import NavigationErrorCalculation 

nec = NavigationErrorCalculation()

class NavigationErrorPlot:

    ###############

    def _create_data_bases(self, PdData, column_name, unit_lbl, scaling_method, scaling_size, scaling_parameter, re_scaling_factor):

        data_set = analysis.CitrosData(PdData, data_label = column_name, units = unit_lbl)
        if scaling_method == 'scale_data':
            db = data_set.scale_data(n_points = scaling_size, param_label= scaling_parameter)
        else: 
            db = data_set.bin_data(n_bins = scaling_size, param_label = scaling_parameter)

        db.addData = db.addData*re_scaling_factor
        
        return(db)

    def draw_data_base_stats(self, PdData, column_name, unit_lbl, scaling_method, scaling_size, scaling_parameter, dt, title, x_label, y_label, is_two_sigma):
        
        max_rid = max(PdData['rid'])*dt
        data_base = self._create_data_bases(PdData, column_name, unit_lbl, scaling_method, scaling_size, scaling_parameter, max_rid)
        fig, axs = data_base.show_statistics(return_fig = True)

        if isinstance(axs, np.ndarray):
            if (len(axs) > 1) and (y_label.find("Angle") == -1):
                labels = ['X  ','Y  ','Z  ']
            elif (len(axs) > 1) and (y_label.find("Angle") != -1):
                labels = ['Roll ','Pitch ','Yaw ']
            else:
                labels = ['','','']
            for ax,lbl in zip(axs,labels):
                ax.set_xlabel(x_label)
                ax.set_ylabel(lbl + y_label)
                ax.set_title('')
                if not is_two_sigma:
                    ax.lines[-1].remove()
        else:
            axs.set_xlabel(x_label)
            axs.set_ylabel(y_label)
            axs.set_title('')
            if not is_two_sigma:
                axs.lines[-1].remove()
                    
        fig.suptitle(title)
        fig.texts[0].set_visible(False)
        plt.show()
        return(fig)
    ###############

    def _lla_true_vs_est(self, citros, gt_lla_topic, est_ecef_topic, gt_lla_data, est_ecef_data, planet_radius, sid_list=None, start_ind=None, end_ind=None):

        if (sid_list == None) or (citros.info()['sid_count'] < len(sid_list)):
            sid_count = list(range(citros.info()['sid_count']))
        else:
            sid_count = sid_list

        
        if (start_ind == None) and (end_ind == None):
            ind_list = None
        elif (start_ind == None):
            start_ind = np.zeros(len(sid_count))
        else:
            end_ind = nec._massage_count(citros, sid_count, gt_lla_topic)

        est_lla = []
        sid = []
        rid = []

        if ind_list != None:
            true_lla = nec._cit_list_2_array(nec._get_var_data(citros, 0, gt_lla_topic, gt_lla_data, [start_ind, end_ind]))
        else:
            true_lla = nec._cit_list_2_array(nec._get_var_data(citros, 0, gt_lla_topic, gt_lla_data, ind_list))
        
        if type(true_lla[0][0]) != "<class 'numpy.float64'>":
                true_lla = np.array(true_lla, dtype=np.float64)

        for i in sid_count:
            
            if ind_list != None:
                r_ecef_est = nec._cit_list_2_array(nec._get_var_data(citros, i, est_ecef_topic, est_ecef_data, [start_ind[i], end_ind[i]]))
            else:
                r_ecef_est = nec._cit_list_2_array(nec._get_var_data(citros, i, est_ecef_topic, est_ecef_data, ind_list))


            if type(r_ecef_est[0][0]) != "<class 'numpy.float64'>":
                r_ecef_est = np.array(r_ecef_est, dtype=np.float64)


            l = len(r_ecef_est)
            
            est_lla.append(nec.ecef2lla(r_ecef_est, planet_radius))

            sid.append(np.zeros(l) + i)
            rid.append(list(range(0,l)))
        
        return(true_lla, est_lla, sid, rid)
    
    #################

    def draw_lla_routes(self, citros, gt_lla_topic, est_ecef_topic, gt_lla_data, est_ecef_data, planet_radius, sid_list=None, start_ind=None, end_ind=None):
    # Create a figure and axis for the plot

        true_lla,est_lla,_,_ = self._lla_true_vs_est(citros, gt_lla_topic, est_ecef_topic, gt_lla_data, est_ecef_data, planet_radius, sid_list, start_ind, end_ind)

        fig, ax = plt.subplots()

        # Plot the true latitude-longitude route in black
        ax.plot(true_lla[:, 1], true_lla[:, 0], c='black', label='True LLA')

        # Plot each array in est_lla
        for i, est_array in enumerate(est_lla):
            ax.plot(est_array[:, 1], est_array[:, 0])#, label=f'Estimate {i + 1}')

        # Set labels for the axes
        ax.set_xlabel('Longitude [Rad]')
        ax.set_ylabel('Latitude [Rad]')

        # Set the title of the plot
        ax.set_title('True LLA vs. Estimated LLA')

        # Add a legend to distinguish between true_lla and est_lla
        ax.legend(loc='upper right')

        # Show the plot
        plt.show()

    #################

