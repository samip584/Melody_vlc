import json

import librosa
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#%matplotlib inline
import os
from PIL import Image
import pathlib
import csv

from math import sqrt
import warnings
warnings.filterwarnings('ignore')



def classify(song_loc):
    cmap = plt.get_cmap('inferno')
    header = 'filename chroma_stft rmse spectral_centroid spectral_bandwidth rolloff zero_crossing_rate'
    for i in range(1, 21):
        header += ' mfcc'+str(i)
    header += ' label'
    header = header.split()
    a = "asd"

    file = open('/home/samip/Code/Melody_vlc/song_data.csv', 'w')
    with file:
        writer = csv.writer(file)
        writer.writerow(header)

    for i in range(len(song_loc)):
        if song_loc[i] == '/':
            num = i
    num+=1
     
    filename = song_loc[num:]
    filename = filename.replace(" ", "")
    print(filename)
    y, sr = librosa.load(song_loc, mono=True, duration = 30)
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    rmse = librosa.feature.rms(y=y)
    spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    zcr = librosa.feature.zero_crossing_rate(y)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    to_append = '{} {} {} {} {} {} {}'.format(filename,np.mean(chroma_stft),np.mean(rmse),np.mean(spec_cent), np.mean(spec_bw), np.mean(rolloff), np.mean(zcr))    
    for e in mfcc:
        to_append += ' {}'.format(np.mean(e))
    to_append += ' Song'
    file = open('/home/samip/Code/Melody_vlc/song_data.csv', 'a')
    with file:
        writer = csv.writer(file)
        writer.writerow(to_append.split())

    data = pd.read_csv('/home/samip/Code/Melody_vlc/song_data.csv')
    data = data.drop(['filename'],axis=1)
    #print(data)

    song_data = data.values
    song_data = song_data[0]


    data = pd.read_csv('/home/samip/Code/Melody_vlc/data.csv')
    data = data.drop(['filename'],axis=1)

    genre_list = data.iloc[:, -1]
    chroma_shifts =data['chroma_stft']
    spectral_centroid = data['spectral_centroid']
    spectral_bandwidth = data['spectral_bandwidth']
    rolloff =data['rolloff']
    zero_crossing_rate =data['zero_crossing_rate']
    mfcc1 = data['mfcc1']
    mfcc2 = data['mfcc2']
    mfcc3 = data['mfcc3']
    mfcc4 = data['mfcc4']
    mfcc5 = data['mfcc5']
    mfcc6 = data['mfcc6']
    mfcc7 = data['mfcc7']
    mfcc8 = data['mfcc8']
    mfcc9 = data['mfcc9']
    mfcc10 = data['mfcc10']
    mfcc11 = data['mfcc11']
    mfcc12 = data['mfcc12']
    mfcc13 = data['mfcc13']
    mfcc14 = data['mfcc14']
    mfcc15 = data['mfcc15']
    mfcc16 = data['mfcc16']
    mfcc17 = data['mfcc17']
    mfcc18 = data['mfcc18']
    mfcc19 = data['mfcc19']
    mfcc20 = data['mfcc20']


    Euclidean_dist_list ={}
    count = 0
    for i in range (1000):
        Euclidean_dist_list[i] =  sqrt( (chroma_shifts[i]-song_data[0])**2 
                                        + (spectral_centroid[i]-song_data[2])**2 
                                        + (spectral_bandwidth[i]-song_data[3])**2 
                                        + (rolloff[i]-song_data[4])**2 
                                        + (zero_crossing_rate[i]-song_data[5])**2 
                                        + (mfcc1[i]-song_data[6])**2 
                                        + (mfcc2[i]-song_data[7])**2 
                                        + (mfcc3[i]-song_data[8])**2 
                                        + (mfcc4[i]-song_data[9])**2 
                                        + (mfcc5[i]-song_data[10])**2  
                                        + (mfcc6[i]-song_data[11])**2 
                                        + (mfcc7[i]-song_data[12])**2 
                                        + (mfcc8[i]-song_data[13])**2 
                                        + (mfcc9[i]-song_data[14])**2 
                                        + (mfcc10[i]-song_data[15])**2
                                        + (mfcc11[i]-song_data[16])**2
                                        + (mfcc12[i]-song_data[17])**2 
                                        + (mfcc13[i]-song_data[18])**2
                                        + (mfcc14[i]-song_data[19])**2
                                        + (mfcc16[i]-song_data[20])**2
                                        + (mfcc17[i]-song_data[21])**2
                                        + (mfcc18[i]-song_data[22])**2 
                                        + (mfcc19[i]-song_data[23])**2
                                        + (mfcc20[i]-song_data[24])**2
                                        )

    minimum = min(Euclidean_dist_list.items(), key=lambda x: x[1])
    return(int(minimum[0]/100))











