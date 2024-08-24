# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 10:49:45 2024

@author: GAVIN.LIU
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from matplotlib.tri import Triangulation
from scipy.interpolate import griddata
from mpl_toolkits.mplot3d import Axes3D
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

def moving_max(data, window, step):
    # 檢查参數是否合理
    if window <= 0 or step <= 0:
        raise ValueError("Window size and step size must be positive integers.")
    if window > len(data):
        raise ValueError("Window size must be less than or equal to the length of the data.")
    
    max_values = []
    for i in range(0, len(data) - window + 1, step):
        window_data = data[i:i + window]
        max_value = max(window_data)
        max_values.append(max_value)
    
    return max_values

def find_local_maxima_indices(data, threshold=5):
    local_maxima_indices = []
    
    n = len(data)
    if n < 3:  # 如果數據少於3個元素，無法有局部最大值
        return local_maxima_indices
    
    for i in range(1, n - 1):
        # 首先檢查當前元素是否超過閾值
        if data[i] > threshold:
            # 判斷當前元素是否為局部最大值
            if data[i] > data[i - 1] and data[i] > data[i + 1]:
                local_maxima_indices.append(i)
            # 處理平坦區域，即連續相同的元素
            elif data[i] == data[i + 1]:
                j = i
                while j < n - 1 and data[j] == data[j + 1]:
                    j += 1
                # 如果當前元素比平坦區域的兩端都大，則它是局部最大值
                if j < n - 1 and data[i] > data[j + 1] and data[i] > data[i - 1]:
                    local_maxima_indices.append(i)
                # 跳過到平坦區域的最後一個元素
                i = j
    
    return local_maxima_indices


def group_and_median(arr, valid_range):
    if len(arr) == 0:
        return []

    # 初始化
    result = []
    group = [arr[0]]

    for i in range(1, len(arr)):
        if abs(arr[i] - arr[i-1]) < valid_range:
            # 若差異小於 valid_range，加入群組
            group.append(arr[i])
        else:
            # 若差異不小於 valid_range，則處理當前群組
            if len(group) % 2 == 0:
                # 偶數個元素，取中間前一個值
                median_value = sorted(group)[len(group)//2 - 1]
            else:
                # 奇數個元素，取中間值
                median_value = sorted(group)[len(group)//2]
            result.append(median_value)
            group = [arr[i]]  # 開始新的群組

    # 處理最後一個群組
    if len(group) % 2 == 0:
        median_value = sorted(group)[len(group)//2 - 1]
    else:
        median_value = sorted(group)[len(group)//2]
    result.append(median_value)

    return result


def map_y2_index_to_y1_indices(y2_index, window, step):
    start_index = y2_index * step
    end_index = start_index + window - 1
    return start_index, end_index

#%% 路徑設定
folder = r'D:\DeltaBox\OneDrive - Delta Electronics, Inc\ProjectCode_git\WJ_CNC\data\20240814\Tool_B'
filename_list = os.listdir(folder)

#%% 參數設定
samplingrate = 12800 # Hz
interval = 3 #sec
group_point = [0,80,160]

#%% 讀檔取數據

# 取固定區段，避免OOM (之後須改成用演算法找區段，如進刀、退刀、精銑等)
data_all = []
start_alignment_threshold = 5

for filename in filename_list:
    file_path = os.path.join(folder, filename)
    df = pd.read_csv(file_path)
    start_alignment = np.argmax(np.array(df['ai0']) > start_alignment_threshold)
    # start_alignment = list(np.array(df[channel])>threshold).index(True)
    data = np.array(df)[start_alignment:]
    plt.figure()
    plt.title(f'{filename}-ai2')
    
    
    ### 取開頭點
    # 濾波
    filtered_data = filter(data[:,2], [260,270], samplingrate, 'bandpass')
    plt.plot(filtered_data)
    # 取moving_rms
    filter_smooth = moving_rms(filtered_data, 500, 250)
    filter_smooth = np.abs(hilbert(filtered_data))
    
    
    # 取得最大值
    # filter_moving_rms_moving_max__data = moving_max(filter_moving_rms_data, 10,5)
    # 找local maximum，並篩選>threshold的值
    local_maxima_indices = find_local_maxima_indices(filter_smooth, 0.06)
    # 將鄰近點組成群組
    local_maxima_indices_group = group_and_median(local_maxima_indices,30000)
    # 映射回原數列index
    # original_index = map_y2_index_to_y1_indices(local_maxima_indices_group[3], 500, 250)[0]
    # original_index = local_maxima_indices_group
    # # 取該段數據
    # target_data = data[original_index+10000:original_index+10000+interval*samplingrate]
    # plt.plot(range(original_index+10000,original_index+10000+interval*samplingrate), filtered_data[original_index+10000:original_index+10000+interval*samplingrate])
    # plt.ylim(-0.2,0.2)
    
    # # if filename == '20240814132730_20240814133030_normal_007_B-9.csv':
    # #     break
    # # else:
    # #     continue
    # plt.savefig(fr'D:\DeltaBox\OneDrive - Delta Electronics, Inc\ProjectCode_git\WJ_CNC\data\data_exploration\{filename}.png')
    # plt.close()
    # data_all.append(target_data)
    original_index_list = local_maxima_indices_group
    
    for i in range(2,6):
        # original_index = map_y2_index_to_y1_indices(local_maxima_indices_group[3], 500, 250)[0]
        original_index = original_index_list[i]
        
        # 取該段數據
        target_data = data[original_index+10000:original_index+10000+interval*samplingrate]
        data_all.append(target_data)
        plt.plot(range(original_index+10000,original_index+10000+interval*samplingrate), filtered_data[original_index+10000:original_index+10000+interval*samplingrate])
        plt.ylim(-0.2,0.2)
    plt.savefig(fr'D:\DeltaBox\OneDrive - Delta Electronics, Inc\ProjectCode_git\WJ_CNC\data\data_exploration\{filename}.png')
    plt.close()
    
data_all = np.array(data_all)
#%%

plt.figure()
y = data[:,2]
plt.plot(y)
y2 = filter(y, [250,300], samplingrate, 'bandpass')
plt.twinx()
plt.plot(np.linspace(0,len(y),len(y2)), y2, color='orange')
y3 = moving_rms(y2, 500, 250)
plt.plot(np.linspace(0,len(y),len(y3)), y3, color='green')



#%%
data_all2 = data_all.copy()
# np.save(r'D:\DeltaBox\OneDrive - Delta Electronics, Inc\ProjectCode_git\WJ_CNC\20240821_day1_65_4regiongood_data_all.npy',data_all2)
# data_all = np.load(r'D:\DeltaBox\OneDrive - Delta Electronics, Inc\ProjectCode_git\WJ_CNC\20240821_day1_65_4regiongood_data_all.npy')


#%% moving_rms看趨勢
window = 200
step = 100

moving_rms_all = []
for each_data in data_all:
    each_moving_rms_temp = []
    for i in range(0,3):
        y = moving_rms(each_data[:,i], window, step)
        each_moving_rms_temp.append(y)
    moving_rms_all.append(np.array(each_moving_rms_temp).T)
moving_rms_all = np.array(moving_rms_all)

channel = 'ai1'
ch = ['ai0', 'ai1', 'ai2'].index(channel)

plt.figure()
plt.plot(moving_rms_all[group_point[0]:group_point[1],:,ch].T,color='blue')
plt.plot(moving_rms_all[group_point[1]:group_point[2],:,ch].T,color='orange')
plt.plot(moving_rms_all[group_point[2]:,:,ch].T,color='green')


#%% 時域RMS趨勢
def RMS(datalist):
    # a = np.array(datalist)
    rms = np.sqrt(np.mean(np.square(datalist)))
    return rms

rms_all = []
for each_data in data_all:
    each_rms_temp = []
    for i in range(0,3):
        rms_value = RMS(each_data[:,i])
        each_rms_temp.append(rms_value)
    rms_all.append(np.array(each_rms_temp))
rms_all = np.array(rms_all)

plt.figure()
plt.plot(rms_all)


#%% FFT圖
fft_all = []
for each_data in data_all:
    each_fft_temp = []
    for i in range(0,3):
        fft_x,fft_y = myfft(each_data[:,i], samplingrate)
        each_fft_temp.append(fft_y)
    fft_all.append(np.array(each_fft_temp).T)
fft_all = np.array(fft_all)

channel = 'ai0'
ch = ['ai0', 'ai1', 'ai2'].index(channel)

# 純FFT
plt.figure()
plt.plot(fft_x, fft_all[group_point[0]:group_point[1],:,ch].T,color='blue')
plt.plot(fft_x, fft_all[group_point[1]:group_point[2],:,ch].T,color='orange')
plt.plot(fft_x, fft_all[group_point[2]:,:,ch].T,color='green')



# FFT group average
plt.figure()
plt.plot(fft_x, np.average(fft_all[group_point[0]:group_point[1],:,ch].T, axis=1), color='blue')
plt.plot(fft_x, np.average(fft_all[group_point[1]:group_point[2],:,ch].T, axis=1),color='orange')
plt.plot(fft_x, np.average(fft_all[group_point[2]:,:,ch].T, axis=1),color='green')



#%% fft的moving_rms
window = 20
step = 10
channel = 'ai1'
ch = ['ai0', 'ai1', 'ai2'].index(channel)



moving_rms_fft_all = []
for each_data in fft_all:
    each_moving_rms_fft_temp = []
    for i in range(0,3):
        y = moving_rms(each_data[:,i], window, step)
        each_moving_rms_fft_temp.append(y)
    moving_rms_fft_all.append(np.array(each_moving_rms_fft_temp).T)
moving_rms_fft_all = np.array(moving_rms_fft_all)



plt.figure()
plt.plot(np.linspace(0,6400, moving_rms_fft_all.shape[1]), moving_rms_fft_all[group_point[0]:group_point[1],:,ch].T,color='blue')
plt.plot(np.linspace(0,6400, moving_rms_fft_all.shape[1]),moving_rms_fft_all[group_point[1]:group_point[2],:,ch].T,color='orange')
plt.plot(np.linspace(0,6400, moving_rms_fft_all.shape[1]), moving_rms_fft_all[group_point[2]:,:,ch].T,color='green')
#%% moving_rms_fft 特定頻率範圍趨勢
frequency_range = [520,540]
channel = 'ai0'

original_moving_rms_fft_point = moving_rms_fft_all.shape[1]
ch = ['ai0', 'ai1', 'ai2'].index(channel)

target_data = moving_rms_fft_all[:,:,ch][:, frequency_range[0]*original_moving_rms_fft_point//(samplingrate//2):frequency_range[1]*original_moving_rms_fft_point//(samplingrate//2)]
fig, axes = plt.subplots(2)
plt.suptitle(f'moving_rms_fft freq. range {frequency_range}')
axes[0].set_title('max')
axes[0].plot(np.max(target_data,axis=1))
axes[1].set_title('mean')
axes[1].plot(np.mean(target_data,axis=1))
plt.tight_layout()





#%% 3D waterfall plot

frequency_range = [850,900]
channel = 'ai1'

original_moving_rms_fft_point = moving_rms_fft_all.shape[1]


ch = ['ai0', 'ai1', 'ai2'].index(channel)
axi = ['z', 'x', 'y'][ch]

z = moving_rms_fft_all[:,:,ch][:, frequency_range[0]*original_moving_rms_fft_point//(samplingrate//2):frequency_range[1]*original_moving_rms_fft_point//(samplingrate//2)]
x = np.linspace(frequency_range[0], frequency_range[1], z.shape[1])
y = np.linspace(0,65,z.shape[0])
X,Y = np.meshgrid(x, y)
x = X.flatten()
y = Y.flatten()
z = z.flatten()


# 三角面
tri = Triangulation(x, y)

# 畫圖
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_title(f'{channel} ({axi}) - {frequency_range} Hz')
# 畫表面
ax.plot_trisurf(x, y, z, triangles=tri.triangles, cmap='viridis')
# label
ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('Times')
ax.set_zlabel('Amplitude')

