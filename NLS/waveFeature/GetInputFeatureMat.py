import wave
import numpy as np
from scipy.fftpack import fft   # fft，快速傅立叶变换

'''
    根据wav文件，做成输入特征矩阵
    1.获取帧速率和全部的帧；
    2.wave_data转置；
    3.切分成m个汉明窗；
    4.定义汉明窗：用周期函数；对每份数据加窗：数据array×汉明窗数据；
    5.每个窗进行快速傅立叶变换；
    6.每个窗取前一半的数据即可（因为是对称的）；
    7.data_input.reshape(data_input.shape[0],data_input.shape[1],1)，得到特征向量；
'''

# filename = "D:/workspace/IDEA_Projects/nls/ali/example-recognizer/target/classes/nls-sample-16k.wav"
# filename = "./nls-sample-16k.wav"
filename = "D:/workspace/openSourceModel/ASRT_SpeechRecognition/dataset/data_thchs30/data/A11_0.wav"
filename = "D:/workspace/openSourceModel/ASRT_SpeechRecognition/dataset/data_thchs30/data/A11_1.wav"

wav = wave.open(filename, "rb")  # 打开一个wav格式的声音文件流
num_frame = wav.getnframes()  # 获取帧数
num_channel = wav.getnchannels()  # 获取声道数
framerate = wav.getframerate()  # 获取帧速率
num_sample_width = wav.getsampwidth()  # 获取实例的比特宽度，即每一帧的字节数
str_data = wav.readframes(num_frame)  # 读取全部的帧
wav.close()  # 关闭流

wave_data = np.fromstring(str_data, dtype=np.short)  # 将声音文件数据转换为数组矩阵形式
print("wave_date转置前：", wave_data.shape)

wave_data.shape = -1, num_channel  # 按照声道数将数组整形，单声道时候是一列数组，双声道时候是两列的矩阵
wave_data = wave_data.T  # 将矩阵转置

# wave_data, framerate
print("帧数：", num_frame)
print("声道数：", num_channel)
print("帧速率：", framerate)
print("WAV文件矩阵(转置后)：", wave_data)

print(type(wave_data))
print("WAV文件矩阵(转置后)：", wave_data.shape)
# np.save('./wave.txt', wave_data)

print("=============之后根据 wave_data 和 帧速率 做输入特征=============")

if (16000 != framerate):
    raise ValueError('[Error] ASRT currently only supports wav audio files with a sampling rate of 16000 Hz, but this audio is ' + str(framerate) + ' Hz. ')

# wav波形 加时间窗以及时移10ms
time_window = 25  # 单位ms
window_length = framerate / 1000 * time_window  # 计算窗长度的公式，目前全部为400固定值

wav_arr = np.array(wave_data)
# wav_length = len(wavsignal[0])
wav_length = wav_arr.shape[1]    # wav文件的长度，为47308

range0_end = int(len(wave_data[0]) / framerate * 1000 - time_window) // 10  # 计算循环终止的位置，也就是最终生成的窗数（窗数对应特征矩阵的行数）
data_input = np.zeros((range0_end, 200), dtype=np.float)  # 用于存放最终的频率特征数据
data_line = np.zeros((1, 400), dtype=np.float)

x=np.linspace(0, 400 - 1, 400, dtype = np.int64)    # 生成从0到399的等差数列，共400个数
w = 0.54 - 0.46 * np.cos(2 * np.pi * (x) / (400 - 1) ) # 汉明窗

for i in range(0, range0_end):
    p_start = i * 160
    p_end = p_start + 400

    data_line = wav_arr[0, p_start:p_end]
    data_line = data_line * w  # 加窗，一个窗内数据正好为一个周期

    data_line = np.abs(fft(data_line)) / wav_length    # fft：快速傅里叶变换

    data_input[i] = data_line[0:200]  # 设置为400除以2的值（即200）是取一半数据，因为是对称的

# print(data_input.shape)
data_input = np.log(data_input + 1)

print(type(data_input), data_input.shape)
# print("输入特征矩阵：", data_input)
# np.save('./data_input.txt', data_input)

data_input = data_input.reshape(data_input.shape[0],data_input.shape[1],1)    # data_input为神经网络需要的输入特征向量
print(type(data_input), data_input.shape)
