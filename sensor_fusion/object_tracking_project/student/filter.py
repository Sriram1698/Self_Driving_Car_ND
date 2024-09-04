# ---------------------------------------------------------------------
# Project "Track 3D-Objects Over Time"
# Copyright (C) 2020, Dr. Antje Muntzinger / Dr. Andreas Haja.
#
# Purpose of this file : Kalman filter class
#
# You should have received a copy of the Udacity license together with this program.
#
# https://www.udacity.com/course/self-driving-car-engineer-nanodegree--nd013
# ----------------------------------------------------------------------
#

# imports
import numpy as np

# add project directory to python path to enable relative imports
import os
import sys
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
import misc.params as params 

class Filter:
    '''Kalman filter class'''
    def __init__(self):
        pass

    def F(self):
        ############
        # TODO Step 1: implement and return system matrix F
        ############
        F = np.matrix(np.eye(6))
        F[0, 3] = F[1, 4] = F[2, 5] = params.dt
        return F
        
        ############
        # END student code
        ############ 

    def Q(self):
        ############
        # TODO Step 1: implement and return process noise covariance Q
        ############

        q   = params.q
        dt  = params.dt
        q1  = ((dt**3)/3) *  q
        q2  = ((dt**2)/2) *  q
        q3  = dt * q
        q1_3_3 = np.matrix(np.eye(3) * q1)
        q2_3_3 = np.matrix(np.eye(3) * q2)
        q3_3_3 = np.matrix(np.eye(3) * q3)
        
        Q = np.matrix(np.zeros((6, 6)))
        Q[0:3, 0:3] = q1_3_3
        Q[0:3, 3:6] = Q[3:6, 0:3] = q2_3_3
        Q[3:6, 3:6] = q3_3_3

        return Q
        
        ############
        # END student code
        ############ 

    def predict(self, track):
        ############
        # TODO Step 1: predict state x and estimation error covariance P to next timestep, save x and P in track
        ############
        F = self.F()
        x = F * track.x
        P = F * track.P * F.transpose() + self.Q()

        track.set_x(x)
        track.set_P(P)
        
        ############
        # END student code
        ############ 

    def update(self, track, meas):
        ############
        # TODO Step 1: update state x and covariance P with associated measurement, save x and P in track
        ############
        residual = self.gamma(track, meas)
        H = meas.sensor.get_H(track.x)
        K = track.P * H.transpose() * np.linalg.inv(self.S(track, meas, H))
        x = track.x + K * residual
        I = np.identity(params.dim_state)
        P = (I - K*H) * track.P

        track.set_x(x)
        track.set_P(P)
        ############
        # END student code
        ############ 
        track.update_attributes(meas)
    
    def gamma(self, track, meas):
        ############
        # TODO Step 1: calculate and return residual gamma
        ############
        return meas.z - meas.sensor.get_hx(track.x)
        
        ############
        # END student code
        ############ 

    def S(self, track, meas, H):
        ############
        # TODO Step 1: calculate and return covariance of residual S
        ############
        return H * track.P * H.transpose() + meas.R
        
        ############
        # END student code
        ############ 