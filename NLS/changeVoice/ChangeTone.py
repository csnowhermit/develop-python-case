import librosa

'''
    简单变声Demo：通过移动音调变声 ，14是上移14个半步， 如果是 -14 下移14个半步
'''

y,sr = librosa.load("原始录音.wav")

# 通过移动音调变声 ，14是上移14个半步， 如果是 -14 下移14个半步
b = librosa.effects.pitch_shift(y, sr, n_steps=14)
librosa.output.write_wav("改变音调.wav",b,sr)