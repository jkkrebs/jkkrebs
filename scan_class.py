# -*- coding: utf-8 -*-
"""
Created on Wed May 26 08:37:30 2021

@author: kkrebs
"""
import time
import numpy as np

start_lambda = 400 # from user input
end_lambda = 420 # from user input
step_size = 5 # from user input
tau_code = 9 # time constant code from lock-in (up to 3.0 seconds)

# key-value pairs for tau conversion from tau_code
time_constants = {0:0.00001,1:.000030,2:0.0001,3:0.0003,4:0.001,5:0.003,6:0.010,7:0.030,8:0.100,9:0.300,10:1,11:3}
tau = time_constants[tau_code] # converted through dictionary to value in seconds

class Emission_scan:
    
    def __init__(self, instr, start_lambda, end_lambda, step_size, tau):
        self.instr = instr
        self.start_lambda = start_lambda
        self.end_lambda = end_lambda
        self.step_size = step_size
        self.tau = tau
        
    def scan(self):
        
        l = self.start_lambda
        wavlen=[] #initialize data wavelength
        xch=[] #initialize data x channel
        ych=[] #initialize data y channel
        
        while l < self.end_lambda + 1:
            wavlen= np.append(wavlen,l)
            # send instrument (McPherson or Cornerston) to l
            time.sleep(5*self.tau)
            #read x_ch_data
            #read y_ch_data
            xch= np.append(xch,x_ch_data)
            ych= np.append(ych,y_ch_data)
            # update plot
            l += self.step_size

        