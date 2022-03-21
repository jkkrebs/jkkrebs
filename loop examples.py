# -*- coding: utf-8 -*-
"""
Created on Thu May 27 13:09:46 2021

@author: kkrebs
"""
import time
import numpy as np

lambda_start = 400 # from user input
lambda_end = 420 # from user input
step_size = 5 # from user input
tau_code = 9 # time constant code from lock-in
wavlen=[] #initialize data wavelength 
xch=[] #initialize data x channel
ych=[] #initialize data y channel

# key-value pairs for tau conversion from tau_code
time_constants = {0:0.00001,1:.000030,2:0.0001,3:0.0003,4:0.001,5:0.003,6:0.010,7:0.030,8:0.100,9:0.300,10:1,11:3}
tau= time_constants[tau_code] # converted through dictionary to value in seconds


l = lambda_start

while l < lambda_end +1:
    wavlen= np.append(wavlen,l)
    # send McPherson to l
    time.sleep(5*tau)
    #read x_ch_data
    #read y_ch_data
    # xch= np.append(xch,x_ch_data)
    # ych= np.append(ych,y_ch_data)
    # update plot
    l += step_size

    
