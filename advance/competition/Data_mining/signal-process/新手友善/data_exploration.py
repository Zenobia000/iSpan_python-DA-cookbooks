# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 08:41:59 2024

@author: GAVIN.LIU
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from PdM_System.frequencyprocessing.frequencyprocessing import mystft
from scipy.signal import hilbert
#%% function

# FFT
def myfft(data,samplingrate):
    """
    data:
        np.array轉fft
        (L,C)
        L:sample數(等長)
        C:column數
    samplingrate: int
    
    return:
        np.array
        (x,y)
        x:frequency
        y:fft
        
    """
    data = np.array(data)
    data_fft = np.fft.fft(data,axis=0)
    data_fft = np.abs(data_fft)[0:len(data_fft)//2]
    data_fft /= len(data_fft)
    return np.linspace(0,samplingrate//2,len(data_fft),endpoint=False), data_fft

# 濾波器
def filter(data,filtered_frequency,sampling_rate,filter_type):
    if type(filtered_frequency) == list:
        low = (filtered_frequency[0] * 2) / sampling_rate
        high = (filtered_frequency[1] * 2) / sampling_rate
    else:
        filtered_frequency_converted = (filtered_frequency * 2) / sampling_rate
    a = data.copy()
    if filter_type == 'lowpass' or filter_type == 'low':
        bb, aa = signal.butter(3, filtered_frequency_converted, filter_type)
    elif filter_type == 'highpass' or filter_type == 'high':
        bb, aa = signal.butter(3, filtered_frequency_converted, filter_type)
    elif filter_type == 'bandpass' or filter_type == 'bandstop':
        bb, aa = signal.butter(3, [low,high], filter_type)
    b = signal.filtfilt(bb, aa, a)

    return b

# 移動rms
def moving_rms(x, N,s=1): # 再次優化 2022/05/03 -->2022/12/14新增s
    x_array = np.array(x)
    
    xc = np.cumsum(abs(x_array)**2)
    z = np.sqrt((xc[N-1:] - np.concatenate([np.zeros(1),xc[:-N]])) / N)
    z = np.concatenate([np.ones(N-1)*z[0],z])
    if s !=1:
        z = z[0:len(z):s] # 不等長
    return z
#%%

filename = '20240814172840_20240814173130_normal_029_B-2_L060.csv'

df = pd.read_csv(fr'D:\DeltaBox\OneDrive - Delta Electronics, Inc\ProjectCode_git\WJ_CNC\data\20240814\Tool_B\{filename}')
#%% 參數設定
samplingrate = 12800 # Hz
interval = 3 #sec

#%%

result_dict = {}



#%%
plt.figure()
plt.title('rawdata')
plt.plot(df['ai0'])
plt.plot(df['ai1'])
plt.plot(df['ai2'])

#%% moving_rms看趨勢
window = 500 # point
step = 250 # point
result_dict['moving_rms'] = {}
result_dict['moving_rms']['window'] = window
result_dict['moving_rms']['step'] = step



plt.figure()
plt.title(f'moving_rms (window: {window}, step: {step})')
for i in range(0,3):
    result_dict['moving_rms'][f'ai{i}'] = moving_rms(df[f'ai{i}'], window, step)
    plt.plot(result_dict['moving_rms'][f'ai{i}'])
    
#%% filter

filter_range = [260,270]
filter_type = 'bandpass'
result_dict['filter'] = {}
result_dict['filter']['filter_range'] = filter_range
result_dict['filter']['filter_type'] = filter_type




plt.figure()
plt.title(f'filter (type: {filter_type}, freq.: {filter_range})')
for i in range(0,3):
    
    result_dict['filter'][f'ai{i}'] = filter(df[f'ai{i}'], filter_range, samplingrate, filter_type)
    plt.plot(result_dict['filter'][f'ai{i}'])

#%% filter_moving_rms

window = 500 # point
step = 250 # point
result_dict['filter_moving_rms'] = {}
result_dict['filter_moving_rms']['window'] = window
result_dict['filter_moving_rms']['step'] = step

plt.figure()
plt.title(f'filter moving_rms (window: {window}, step: {step})')
for i in range(0,3):
    result_dict['filter_moving_rms'][f'ai{i}'] = moving_rms(result_dict['filter'][f'ai{i}'], window, step)

    plt.plot(result_dict['filter_moving_rms'][f'ai{i}'])







#%% envelop HHT

result_dict['filter_HHT'] = {}

plt.figure()
plt.title(f'filter HHT')
for i in range(0,3):
    result_dict['filter_HHT'][f'ai{i}'] = np.abs(hilbert(result_dict['filter'][f'ai{i}']))

    plt.plot(result_dict['filter_HHT'][f'ai{i}'])


#%%
plt.figure()
plt.plot(result_dict['filter'][f'ai{i}'])
plt.plot(result_dict['filter_HHT'][f'ai{i}'])
#%%
plt.figure()
plt.plot(result_dict['filter_HHT'][f'ai{i}'])
plt.twinx()
plt.plot(np.diff(result_dict['filter_HHT'][f'ai{i}']), color='orange')

filter_moving_rms_data = result_dict['filter_HHT'][f'ai{i}']
local_maxima_indices = find_local_maxima_indices(filter_moving_rms_data, 0.04)
# 將鄰近點組成群組
local_maxima_indices_group = group_and_median(local_maxima_indices,10000)
# 映射回原數列index
# original_index = map_y2_index_to_y1_indices(local_maxima_indices_group[3], 500, 250)[0]
original_index_list = local_maxima_indices_group


# 取該段數據
for original_index in original_index_list:
    target_data = np.array(df['ai2'])[original_index+10000:original_index+10000+interval*samplingrate]
    
    
    plt.plot(range(original_index+10000,original_index+10000+interval*samplingrate), df['ai2'][original_index+10000:original_index+10000+interval*samplingrate])
    plt.ylim(-0.2,0.2)

#%%
plt.figure()
plt.hist(np.diff(result_dict['filter_HHT'][f'ai{i}'][0:1340000]), bins=100, color='blue', edgecolor='black')
#%%
filter_condition = result_dict['filter_HHT'][f'ai{i}'][0:1340000]
data = np.array(result_dict['filter_HHT'][f'ai{i}'])[0:1340000]
plt.plot(np.linspace(0,100,len(data)), data)
plt.plot(np.where(data < 0.02, data, np.nan), color='red', label='data < 0.02')
plt.plot(np.where((data >= 0.02) & (data <= 0.04), data, np.nan), color='green', label='0.02 <= data <= 0.04')
plt.plot(np.where(data > 0.04, data, np.nan), color='blue', label='data > 0.04')
#%%
plt.figure()
plt.plot(result_dict['filter_HHT'][f'ai{i}'][0:1340000])
plt.twinx()
plt.plot(np.diff(result_dict['filter_HHT'][f'ai{i}'][0:1340000])**2, color='orange')


#%% STFT

f,t,Zxx = mystft(df['ai2'], samplingrate, nperseg=1280)



plt.figure()
plt.pcolormesh(t,f,np.log(np.abs(Zxx)))

