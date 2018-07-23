# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 10:32:06 2018

@author: matthew
"""

import os 
import glob
import matplotlib.pyplot as plt
import binascii
import numpy as np

path = r'/home/mjayk/Documents/RCS/UoHBoard/ReadFiles/RCS_ReadFiles'
os.chdir(path)
files = glob.glob('**.RCS')


fname  = files[1]
print(fname)
with open(fname,"rb") as binary_file:
    dataraw = binary_file.read()


header = dataraw[0:13].decode('utf-8')

#decode markerblock 
    
markerblock = dataraw[14:28]
markerblock_str = binascii.b2a_hex(markerblock).decode('utf-8')

year = markerblock_str[0:2]
month = markerblock_str[2:4]
day = markerblock_str[4:6]
hour  = markerblock_str[6:8]
minute = markerblock_str[8:10]
second = markerblock_str[10:12]
dts = year + '/' + month  + '/' + day  + '    ' + hour +':'+ minute +':'+ second
print(year + ' // '  + month + ' // '  + day + ' // '  + hour + ' // '  + minute + ' // '  + second)
#

p1 = []
p2 = [] 
p3 = []
tof = []
glitchcount = []

packetlength = 14

#for lmn in np.linspace(0,len(dataraw)-14*2+1,len(dataraw)-14*2):
lmn = 0
firstbit = 0
while firstbit < len(dataraw)-packetlength:
    lmn = int(lmn)
    firstbit = 27+(packetlength*lmn)+1
    lastbit = firstbit+packetlength
    data = dataraw[firstbit:lastbit]
    data_s = binascii.b2a_hex(data).decode('utf-8')


    if data[8] != 255:
        p1.append(float(data[1]*2**8) + float(data[0]))
        p2.append(float(data[3]*2**8) + float(data[2]))
        p3.append(float(data[5]*2**8) + float(data[4]))
        
       # glitchcount.append(float(str(data[6])))   
        
        toffactor = 1/12e6
        tof.append((float((data[7])*2**8 + (data[6])))/12)
    lmn = lmn+1
    

    #break 

p1 = np.array(p1)
p2 = np.array(p2)
p3 = np.array(p3)
tof = np.array(tof)


#Scatering ratio
ratio=[]
for prq in np.linspace(0,len(tof)-1,len(tof)):
    prq = int(prq)
    if p1[prq] > p2[prq]:
        if p2[prq] == 0:
            ratio.append(0)
        else:
            ratio.append(p1[prq]/p2[prq])
    if p2[prq] >p1[prq]:
        if p1[prq] == 0:
            ratio.append(0)
        else:
            ratio.append(p2[prq]/p1[prq])


if 1 == 1:
    plt.figure(2)
    plt.subplot(221)
    plt.cla()
    plt.title('Time of flight')
#    n, bins, patches = plt.hist(tof, bins=range(1,10))
    n, bins, patches = plt.hist(tof, bins=range(1,10))
    plt.plot(bins[0:-1] + 0.5, n)       
    
    
    plt.subplot(222)
    plt.cla()
    plt.title('Biref')
    n, bins, patches = plt.hist(p3) 
    plt.plot(bins[0:-1] + 0.5, n)
    
    plt.subplot(223)
    plt.cla()
    plt.title('Scat1')
    n,bins,patches = plt.hist(p1)
    plt.plot(bins[0:-1],n)
    
    plt.subplot(224)
    plt.cla()
    plt.title('Scat2')
    n, bins, patches = plt.hist(p2)
    plt.plot(bins[0:-1],n)
    