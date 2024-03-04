import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
from citros_data_analysis import data_access as da
from citros_data_analysis import error_analysis as analysis
from prettytable import PrettyTable, ALL


class NavigationErrorCalculation:


    def _get_var_data(self, citros, i, topic, var_name, rid_ind=None):
       
        if rid_ind == None:
            var_data = citros.topic(topic).set_order({'sid':'asc','rid':'asc'}).sid(i).data(var_name)[var_name]
        else:
            var_data = citros.topic(topic).set_order({'sid':'asc','rid':'asc'}).sid(i).rid(start = rid_ind[0], end = rid_ind[1]).data(var_name)[var_name]

        return(var_data)

    #################

    def _array_2_cit_list(self, arr):

        cit_list = []
        for row in arr: 
            
            cit_list.append(list(row))

        return(cit_list)
    
    #################

    def _cit_list_2_array(self, cit_list):

        arr = []
        for row in cit_list: 
            arr.append(np.array(row))
            # print(np.array(row))
        arr = np.array(arr)
        return(arr)
    
    #################

    def _massage_count(self, citros, sid_list, topic):

        if (citros.info()['sid_count'] < len(sid_list)):
            sid_count = list(range(citros.info()['sid_count']))
        else:
            sid_count = sid_list

        msg_count = np.zeros(len(sid_count))

        for i in sid_count:
            
            inf = citros.sid(sid_count).info()
            
            msg_count[i] = inf['sids'][i]['topics'][topic]['message_count']

        return(msg_count)

    ##################

    def quat_diff(self, q1,q2):


        q1_conj = np.array([q1[0], -q1[1],-q1[2],-q1[3]])
        q_difference = np.zeros(4)
        
        q_difference[0] = q1_conj[0] * q2[0] - q1_conj[1] * q2[1] - q1_conj[2] * q2[2] - q1_conj[3] * q2[3]
        q_difference[1] = q1_conj[0] * q2[1] + q1_conj[1] * q2[0] + q1_conj[2] * q2[3] - q1_conj[3] * q2[2]
        q_difference[2] = q1_conj[0] * q2[2] - q1_conj[1] * q2[3] + q1_conj[2] * q2[0] + q1_conj[3] * q2[1]
        q_difference[3] = q1_conj[0] * q2[3] + q1_conj[1] * q2[2] - q1_conj[2] * q2[1] + q1_conj[3] * q2[0]

        angular_error = 2*np.arccos(abs(q_difference[0]))

        return(angular_error,q_difference)

        ###############

    def dcm_to_euler_angles(self, dcm):
    # Calculate pitch
        if dcm[2, 0] < 1:
            if dcm[2, 0] > -1:
                pitch = np.arcsin(-dcm[2, 0])
                yaw = np.arctan2(dcm[1, 0], dcm[0, 0])
                roll = np.arctan2(dcm[2, 1], dcm[2, 2])
            else:
                pitch = np.pi / 2
                yaw = -np.arctan2(-dcm[0, 1], dcm[0, 2])
                roll = 0
        else:
            pitch = -np.pi / 2
            yaw = np.arctan2(-dcm[0, 1], dcm[0, 2])
            roll = 0

        return(roll, pitch, yaw)

    ###############

    def quat2dcm(self, q):
    # Normalize the quaternion if necessary
        q /= np.linalg.norm(q)
        
        # Extract quaternion components
        w, x, y, z = q
        
        # Calculate rotation matrix elements
        r00 = 1 - 2*y*y - 2*z*z
        r01 = 2*x*y - 2*w*z
        r02 = 2*x*z + 2*w*y
        r10 = 2*x*y + 2*w*z
        r11 = 1 - 2*x*x - 2*z*z
        r12 = 2*y*z - 2*w*x
        r20 = 2*x*z - 2*w*y
        r21 = 2*y*z + 2*w*x
        r22 = 1 - 2*x*x - 2*y*y
        
        # Construct the rotation matrix
        matrix = np.array([[r00, r01, r02],
                        [r10, r11, r12],
                        [r20, r21, r22]])
        
        return(matrix)

    ###############

    def ecef2lla(self, r_ecef, r_planet):

        l = r_ecef.shape[0]
        lla = np.zeros([l, 3])
        r = np.linalg.norm(r_ecef, axis=1)  # Calculate the norm along axis 1

        lla[:, 0] = np.arcsin(r_ecef[:, 2] / r)
        lla[:, 1] = np.arctan2(r_ecef[:, 1], r_ecef[:, 0])
        lla[lla[:, 1] > np.pi, 1] -= 2 * np.pi

        lla[:, 2] = r - r_planet

        return lla


    ###############

    def lla2ned_dcm(self, lat, long):

        l = len(lat)

        csLAT = np.cos(lat)
        snLAT = np.sin(lat)
        csLONG = np.cos(long)
        snLONG = np.sin(long)

        row_array_0 = np.stack([-snLAT*csLONG , -snLAT*snLONG, csLAT], axis=-1)
        row_array_1 = np.stack([-snLONG,   csLONG,  np.zeros(l)], axis=-1)
        row_array_2 = np.stack([ -csLAT*csLONG, -csLAT*snLONG, -snLAT], axis=-1)

        dcm_lla_2_ned = np.stack((row_array_0, row_array_1, row_array_2), axis = -2)

        return(dcm_lla_2_ned)

    #################

    def roll_pitch_yaw_error(self, citros, gt_topic, est_topic, gt_data, est_data, quat_or_matrix='quat', sid_list=None, list_or_pd='list' ,name_of_angular_error = '',name_of_quat_error = '', start_ind=None, end_ind=None):

        if (sid_list == None) or (citros.info()['sid_count'] < len(sid_list)):
            sid_count = list(range(citros.info()['sid_count']))
        else:
            sid_count = sid_list
 
        
        if (start_ind == None) and (end_ind == None):
            ind_list = None
        elif (start_ind == None):
            start_ind = np.zeros(len(sid_count))
        else:
            end_ind = self._massage_count(citros, sid_count, gt_topic)

        quat_angular_error = []
        roll_pitch_yaw_error = []
        sid = []
        rid = []
        
        
        for i in sid_count:

            angular_error = []
            euler_angles = []

            if quat_or_matrix != 'dcm':
                
                if ind_list != None:
                    q_l2b_true = self._cit_list_2_array(self._get_var_data(citros, i, gt_topic, gt_data, [start_ind[i], end_ind[i]]))
                    q_l2b_est = self._cit_list_2_array(self._get_var_data(citros, i, est_topic, est_data, [start_ind[i], end_ind[i]]))
                else:
                    q_l2b_true = self._cit_list_2_array(self._get_var_data(citros, i, gt_topic, gt_data, ind_list))
                    q_l2b_est = self._cit_list_2_array(self._get_var_data(citros, i, est_topic, est_data, ind_list))
                
                if type(q_l2b_true[0][0]) != "<class 'numpy.float64'>":
                    q_l2b_true = np.array(q_l2b_true, dtype=np.float64)
                if type(q_l2b_est[0][0]) != "<class 'numpy.float64'>":
                    q_l2b_est = np.array(q_l2b_est, dtype=np.float64)
            
                l = len(q_l2b_true)

                for q_true,q_est in zip(q_l2b_true, q_l2b_est):

                    q_true = np.array(q_true)
                    q_est = np.array(q_est)

                    error_q_angle, q_error = self.quat_diff(q_true,q_est)

                    angular_error.append(error_q_angle)

                    error_dcm = self.quat2dcm(q_error)        

                    roll, pitch, yaw = self.dcm_to_euler_angles(error_dcm)

                    euler_angles.append([roll, pitch, yaw])

                quat_angular_error.append(np.array(angular_error))
                roll_pitch_yaw_error.append(np.array(euler_angles))

                sid.append(np.full(l, i, dtype=int))
                rid.append(list(range(0,l)))

                
            else:
                
                if ind_list != None:
                    l2b_dcm_true = self._get_var_data(citros, i, gt_topic, gt_data, [start_ind[i], end_ind[i]])
                    l2b_dcm_est = self._get_var_data(citros, i, est_topic, est_data, [start_ind[i], end_ind[i]])
                else:
                    l2b_dcm_true = self._get_var_data(citros, i, gt_topic, gt_data, ind_list)
                    l2b_dcm_est = self._get_var_data(citros, i, est_topic, est_data, ind_list)

            
                l = len(l2b_dcm_true)

                for dcm_true,dcm_est in zip(l2b_dcm_true, l2b_dcm_est):
                    
                    if type(dcm_true[0][0]) != "<class 'numpy.float64'>":
                        dcm_true = np.array(dcm_true, dtype=np.float64)
                    if type(dcm_est[0][0]) != "<class 'numpy.float64'>":
                        dcm_est = np.array(dcm_est, dtype=np.float64)


                    error_dcm = np.dot(np.transpose(dcm_true), dcm_est)        

                    roll, pitch, yaw = self.dcm_to_euler_angles(error_dcm)

                    euler_angles.append([roll, pitch, yaw])


                quat_angular_error = None
                roll_pitch_yaw_error.append(np.array(euler_angles))
                sid.append(np.full(l, i, dtype=int))
                rid.append(list(range(0,l)))

        if list_or_pd == 'list': 
            
            return(roll_pitch_yaw_error, quat_angular_error, sid, rid)

        else:
            sid = self._list_2_pd_data_frame(sid, 'sid')
            sid = self._list_2_pd_data_frame(rid, 'rid', sid)
            roll_pitch_yaw_error = self._list_2_pd_data_frame(roll_pitch_yaw_error, name_of_angular_error, sid)
            roll_pitch_yaw_error = self._list_2_pd_data_frame(quat_angular_error, name_of_quat_error, roll_pitch_yaw_error)
            return(roll_pitch_yaw_error)
        

    ###############

    def vec_error(self, citros, gt_topic, est_topic, gt_data, est_data, sid_list=None, list_or_pd='list' ,name_of_error = '', start_ind=None, end_ind=None):

        if (sid_list == None) or (citros.info()['sid_count'] < len(sid_list)):
            sid_count = list(range(citros.info()['sid_count']))
        else:
            sid_count = sid_list
    
        vec_error = []
        sid = []
        rid = []
        
        if (start_ind == None) and (end_ind == None):
            ind_list = None
        elif (start_ind == None):
            start_ind = np.zeros(len(sid_count))
        else:
            end_ind = self._massage_count(citros, sid_count, gt_topic)

        for i in sid_count:
            
            if ind_list != None:
                vec_true = self._cit_list_2_array(self._get_var_data(citros, i, gt_topic, gt_data, [start_ind[i], end_ind[i]]))
                vec_est = self._cit_list_2_array(self._get_var_data(citros, i, est_topic, est_data, [start_ind[i], end_ind[i]]))
            else:
                vec_true = self._cit_list_2_array(self._get_var_data(citros, i, gt_topic, gt_data, ind_list))
                vec_est = self._cit_list_2_array(self._get_var_data(citros, i, est_topic, est_data, ind_list))

            if type(vec_true[0][0]) != "<class 'numpy.float64'>":
                vec_true = np.array(vec_true, dtype=np.float64)
            if type(vec_est[0][0]) != "<class 'numpy.float64'>":
                vec_est = np.array(vec_est, dtype=np.float64)
            
            l = len(vec_true)

            vec_error.append(vec_true - vec_est)
 
            sid.append(np.full(l, i, dtype=int))
            rid.append(list(range(0,l)))

        if list_or_pd == 'list': 
            return(vec_error, sid,rid)
        else:
            sid = self._list_2_pd_data_frame(sid, 'sid')
            sid = self._list_2_pd_data_frame(rid, 'rid', sid)
            vec_error = self._list_2_pd_data_frame(vec_error, name_of_error, sid)
            return(vec_error)
        

    ###############

    def side_and_down_error(self, citros, vector_data, sid_list = None, list_or_pd='list', column_name=' '):
  
        if (sid_list == None) or (citros.info()['sid_count'] < len(sid_list)):
            sid_count = list(range(citros.info()['sid_count']))
        else:
            sid_count = sid_list


        cross_track_error = []
        down_track_error = []
        sid = []
        rid = []
        

        for i in sid_count:
            
            if isinstance(vector_data, pd.DataFrame): 
                arr = self._pd_data_frame_2_arr(i, vector_data, column_name)
                
            else:
                arr = np.array(vector_data[i])

            cross_track = list(np.linalg.norm(arr[:,:2], axis = 1)) 
            down_track = list(arr[:,2])
            l = len(arr)
 
            cross_track_error.append(cross_track)
            down_track_error.append(down_track)
            sid.append(np.full(l, i, dtype=int))
            rid.append(list(range(0,l)))

        if list_or_pd == 'list': 
            return(cross_track_error, down_track_error, sid, rid)
        else:
            sid = self._list_2_pd_data_frame(sid, 'sid')
            sid = self._list_2_pd_data_frame(rid, 'rid', sid)
            vec_side_down_error = self._list_2_pd_data_frame(cross_track_error, 'side_track_error', sid)
            vec_side_down_error = self._list_2_pd_data_frame(down_track_error, 'down_track_error', vec_side_down_error)

            return(vec_side_down_error)
        

    ###############

    def transform_ecef_2_ned(self, citros, lla_gt_topic, lla_gt_data, data_in_ecef, sid_list=None, list_or_pd='list', column_name=' ', start_ind=None, end_ind=None):

        if (sid_list == None) or (citros.info()['sid_count'] < len(sid_list)):
            sid_count = list(range(citros.info()['sid_count']))
        else:
            sid_count = sid_list

        
        if (start_ind == None) and (end_ind == None):
            ind_list = None
        elif (start_ind == None):
            start_ind = np.zeros(len(sid_count))
        else:
            end_ind = self._massage_count(citros, sid_count, lla_gt_topic)


        ned_data = []
        sid = []
        rid = []

        for i in sid_count:

            if ind_list != None:
                true_lla = self._cit_list_2_array(self._get_var_data(citros, i, lla_gt_topic, lla_gt_data, [start_ind[i], end_ind[i]]))
            else:
                true_lla = self._cit_list_2_array(self._get_var_data(citros, i, lla_gt_topic, lla_gt_data, ind_list))

                
            ecef_2_ned_dcm = self.lla2ned_dcm(true_lla[:,0], true_lla[:,1])
            if isinstance(data_in_ecef, pd.DataFrame): 
                arr = self._pd_data_frame_2_arr(i, data_in_ecef, column_name)
                reshaped_data = arr[:, :, np.newaxis]

            else:
                reshaped_data = data_in_ecef[i][:, :, np.newaxis]

            ned_data.append(np.sum(ecef_2_ned_dcm*reshaped_data, axis=1))

            l = len(true_lla)

            sid.append(np.full(l, i, dtype=int))
            rid.append(list(range(0,l)))

        if (list_or_pd == 'list'):
            return(ned_data, sid, rid)
        else:
            sid = self._list_2_pd_data_frame(sid, 'sid')
            sid = self._list_2_pd_data_frame(rid, 'rid', sid)
            if isinstance(data_in_ecef, list):       
                data_in_ecef = self._list_2_pd_data_frame(ned_data, "ned_" + column_name, sid)
            else:                
                data_in_ecef = self._list_2_pd_data_frame(ned_data, "ned_" + column_name, sid)
                # data_in_ecef.drop(columns=[column_name], inplace= True)
            return(data_in_ecef)
        

    ###############

    def _pd_data_frame_2_arr(self, i, pd_frame, column_name):

        
        data = pd_frame[pd_frame['sid'] == i]
        l = len((data[column_name]))
        m = len(data[column_name].iloc[0])
        arr = np.zeros((l,m))

        for i in range(0,l):
            arr[i,:] = data[column_name].iloc[i]

        return(arr)
    
    ###############

    def _list_2_pd_data_frame(self, data_list, data_name, data_frame=pd.DataFrame()):


        if isinstance(data_list[0], np.ndarray):
            data_frame = pd.concat([data_frame, pd.DataFrame({data_name: list(np.concatenate(data_list))})], axis=1)    
        else:
            data_frame = pd.concat([data_frame, pd.DataFrame({data_name: np.concatenate(data_list)})], axis=1) 


        return(data_frame)
    