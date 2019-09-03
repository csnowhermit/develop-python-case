import librosa

'''
    简单变声Demo：通过改变采样率来改变音速，相当于播放速度X2
'''

# y,sr = librosa.load("D:/workspace/IDEA_Projects/nls-sdk-java-demo/nls-sample-16k.wav", sr=None)
y, sr = librosa.load("原始录音.wav", sr=None)

# 通过改变采样率来改变音速，相当于播放速度X2
librosa.output.write_wav("改变语速.wav",y,sr*2)