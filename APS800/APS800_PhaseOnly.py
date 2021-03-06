# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 17:38:52 2017

@author: ouille
"""

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
import os
from itertools import takewhile

# FIRST : EXTRACT DATA 
#print ('Where is the file located? e.g : Z:\Laser\CEP\20190311')
#filepath = input('The path of the file is :')
#print ('What is the name of the .dat file? e.g : 20190301_CEPdata ')
#filename = input('The name of the file is :')


filepath = r'Z:\Laser\CEP\20191121'
filename ='DM50off-noPockelsCell-CEPafterGratings'


file= str(filename) + '.dat'

#output directory = new directory created where this python file is located
path = os.getcwd()
if not os.path.exists('analyzed_data'):
    os.mkdir('analyzed_data')
output_dir=path+'\\analyzed_data'

files = str(filepath) + "\\" + str(file)
times = np.loadtxt(files, dtype='str', usecols = (0,),skiprows=8) # probe timing (ns)
phases = np.loadtxt(files, dtype='str', usecols = (1,),skiprows=8) # Phase (radian)
amps = np.loadtxt(files, dtype='str', usecols = (3,),skiprows=8)
nb = np.size(times) - 2.
indices = []
for i in np.arange(0,nb):
    if 'Meas' in times[i]:
        print (i, 'end of a measurement')  
        indices.append(i)
        nb = indices[0]-1

time = np.arange(0,nb) ; phase = np.arange(0,nb) ; squared_phase = np.arange(0,nb) ; amp = np.arange(0,nb) #creation of the lists 
for i in np.arange(0,nb):
    time[i]=float(times[i][2:7])/1.     #time is in sec (/1.) or min (/60.)
    phase[i]=float(phases[i][2:7])
    squared_phase[i]=phase[i]*phase[i]
    amp[i]=float(amps[i][2:7])

    
#Phase deviation rms in mrad
mean_phase = sum(phase)/np.size(phase)
mean_squared_phase = sum(squared_phase)/np.size(squared_phase)
ecart_type = int(round(np.sqrt(mean_squared_phase - mean_phase*mean_phase),3)*1000)


#center values on 0
for i in np.arange(0,nb):
    phase[i]=phase[i]-mean_phase

       
#Figure parameters
fig=plt.figure(figsize=(10,3))
gs = gridspec.GridSpec(1, 2, wspace = 0,  width_ratios=[3, 1])
s=12


#CEP as a function of time
CEPvsT = plt.subplot(gs[0,0])
plt.plot(time,phase, '.', markersize=1.2,  color='navy')
plt.xlabel('time (sec)', size=s)
plt.ylabel('relative CEP (rad)', size=s)
plt.tick_params(axis='both',labelsize=s)
target = 0
#plt.ylim([-np.pi,np.pi])
#plt.yticks([-np.pi, -np.pi/2,0,np.pi/2, np.pi], ['-$\pi$','-$\pi$/2', '0', '$\pi$/2','$\pi$' ], size=s)


#Histogram
histo = plt.subplot(gs[0,1])
plt.hist(phase, bins=round(ecart_type/20), orientation='horizontal', color='navy')  #bins =.... number of columns
plt.yticks([])
plt.axis('off')
plt.xlabel('occurrence', size=s)
plt.tick_params(axis='both',labelsize=s)
#plt.ylim([-np.pi,np.pi])
d,f=np.histogram(phase,bins=round(ecart_type/20))
plt.text(0.1*max(d), max(phase)-0.1*max(phase) ,'$\sigma_{rms}$ = ' + str(ecart_type) + ' mrad', size=s+1)



#Save figure
fig.suptitle('file : ' + str(files), size = s -4)
plt.savefig( str(output_dir) + '\\' + str(filename) + '_phase_histo.png', dpi=300,  bbox_inches='tight')











def index(l, p): return len([x for x in takewhile(lambda x: x[1] <= p, enumerate(l))])
    
def partial (start, end, save=0, zero=0):   #start and end are given in seconds   #if save =1, it will save it   #if zero=1, the origin of the plot is 0
    a = index(time, start)
    b = index(time, end)
    
    
    #Phase deviation rms in mrad
    mean_phase2 = sum(phase[a:b])/np.size(phase[a:b])
    for i in np.arange(0,np.size(phase)):  #il faut le refaire parceque les phases ont été centrée sur 0 !!
        squared_phase[i]=phase[i]*phase[i]         
    mean_squared_phase2 = sum(squared_phase[a:b])/np.size(squared_phase[a:b])
    ecart_type2 = int(round(np.sqrt(mean_squared_phase2 - mean_phase2*mean_phase2),3)*1000)
    
    
           
    #Figure parameters
    fig=plt.figure(figsize=(10,3))
    gs = gridspec.GridSpec(1, 2, wspace = 0,  width_ratios=[3, 1])
    s=12
    
    #Histogram
    plt.subplot(gs[0,1])
    plt.hist(phase[a:b]-np.mean(phase[a:b]), bins=round(ecart_type2/20), orientation='horizontal', color='navy')  #bins =.... number of columns
    plt.xlabel('occurrence', size=s)
    plt.ylim([-np.pi,np.pi])
    plt.tick_params(axis='both',labelsize=s) 
    plt.yticks([])
    plt.axis('off')
    d,f=np.histogram(phase[a:b]-np.mean(phase[a:b]), bins=round(ecart_type2/20)) 
    plt.text(0.1*max(d), 0.8*np.pi, '$\sigma_{rms}$ = ' + str(ecart_type2) + ' mrad', size=s+1)
    
    #CEP as a function of time
    plt.subplot(gs[0,0])
    if zero ==1:
        plt.plot(time[a:b]-time[a],phase[a:b]-np.mean(phase[a:b]), '.', markersize=1.2,  color='navy')
        plt.xlim([0, time[b]-time[a]])
    elif zero ==0:
        plt.plot(time[a:b],phase[a:b]-np.mean(phase[a:b]), '.', markersize=1.2,  color='navy')
        plt.xlim([time[a], time[b]])
    plt.ylim([-np.pi,np.pi])
    plt.xlabel('time (sec)', size=s) 
    plt.ylabel('relative CEP (rad)', size=s)
    plt.tick_params(axis='both',labelsize=s) 
    plt.yticks([-np.pi, -np.pi/2,0,np.pi/2, np.pi], ['-$\pi$','-$\pi$/2', '0', '$\pi$/2','$\pi$' ], size=s)
    
    #Save figure
    fig.suptitle('file : ' + str(files), size = s -4)
    
    if save == 1:
        plt.savefig( str(output_dir) + '\\' + str(filename) + '_phase_histo_interval-' + str(start) + '_' + str(end) +'.png', dpi=300,  bbox_inches='tight')
       
        
        
#partial(start=0, end=60, save=1, zero=0)