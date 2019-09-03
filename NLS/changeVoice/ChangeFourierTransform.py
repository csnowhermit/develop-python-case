import librosa
import matplotlib.pyplot as plt
import numpy as np

'''
    傅里叶变换变声
'''

y,sr = librosa.load("原始录音.wav")

# stft 短时傅立叶变换
a = librosa.stft(y)
length = len(a)

# 改变或去除某些值，可以改变声音
r_a = a[10:length-10]

# istft 逆短时傅立叶变换，变回去
b = librosa.istft(r_a)

librosa.output.write_wav("傅里叶变换变声.wav",b,sr)

# 以下是显示频谱图
fig = plt.figure()
s1 = fig.add_subplot(3,1,1)
s2 = fig.add_subplot(3,1,2)
s3 = fig.add_subplot(3,1,3)

s1.plot(y)
s2.plot(a)
s3.plot(b)

plt.show()