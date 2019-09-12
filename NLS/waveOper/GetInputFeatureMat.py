import wave
import numpy as np

'''
    根据wav文件，做成输入特征矩阵
'''

# filename = "D:/workspace/IDEA_Projects/nls/ali/example-recognizer/target/classes/nls-sample-16k.wav"
filename = "./nls-sample-16k.wav"

wav = wave.open(filename, "rb")  # 打开一个wav格式的声音文件流
num_frame = wav.getnframes()  # 获取帧数
num_channel = wav.getnchannels()  # 获取声道数
framerate = wav.getframerate()  # 获取帧速率
num_sample_width = wav.getsampwidth()  # 获取实例的比特宽度，即每一帧的字节数
str_data = wav.readframes(num_frame)  # 读取全部的帧
wav.close()  # 关闭流

wave_data = np.fromstring(str_data, dtype=np.short)  # 将声音文件数据转换为数组矩阵形式
wave_data.shape = -1, num_channel  # 按照声道数将数组整形，单声道时候是一列数组，双声道时候是两列的矩阵
wave_data = wave_data.T  # 将矩阵转置

# wave_data, framerate
print("帧数：", num_frame)
print("声道数：", num_channel)
print("帧速率：", framerate)
print("WAV文件矩阵：", wave_data)

print(type(wave_data))
print(wave_data.shape)
# np.save('./wave.txt', wave_data)

print("=============之后根据wave_data和帧速率做输入特征=============")

