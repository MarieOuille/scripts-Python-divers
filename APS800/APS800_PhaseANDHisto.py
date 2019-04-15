# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 17:38:52 2017

@author: ouille
"""

import numpy as np
from matplotlib import pyplot as plt

# FIRST : EXTRACT DATA 
print ('Where is the file located?')
filepath = input('The path of the file is :')
print ('What is the name of the .dat file?')
filename = input('The name of the file is :')

file= str(filename) + '.dat'
output_dir=filepath
files = str(filepath) + "\\" + str(file)
times = np.loadtxt(files, dtype='str', usecols = (0,)) # probe timing (ns)
phases = np.loadtxt(files, dtype='str', usecols = (1,))

nb = np.size(times) - 2.
time = np.arange(0,nb)
phase = np.arange(0,nb)
squared_phase = np.arange(0,nb)
for i in np.arange(0,nb):
    time[i]=float(times[i][2:7])/60.
    phase[i]=float(phases[i][2:7])
    squared_phase[i]=phase[i]*phase[i]
#time is in min
    
#Phase deviation rms
mean_phase = sum(phase)/np.size(phase)
mean_squared_phase = sum(squared_phase)/np.size(squared_phase)
ecart_type = int(round(np.sqrt(mean_squared_phase - mean_phase*mean_phase),3)*1000)

#center values on 0
for i in np.arange(0,nb):
    phase[i]=phase[i]-mean_phase
         
#Histogram
plt.hist(phase, bins=100, orientation='horizontal')  #bins =.... number of columns
plt.ylabel('phase (rad)')
plt.xlabel('occurrence')
plt.ylim([-3,3])
plt.title(str(ecart_type) + ' mrad rms')
plt.savefig(str(output_dir) + '\\' + str(filename)+ '_histo.png')
plt.close()

#CEP as a function of time
plt.plot(time,phase)
plt.xlabel('time (min)')
plt.ylabel('phase (rad)')
plt.ylim([-3,3])
plt.savefig(str(output_dir) + '\\' + str(filename) + '_phase.png')
plt.close()