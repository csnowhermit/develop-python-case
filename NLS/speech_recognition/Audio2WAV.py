# -*- coding：utf-8 -*-

import pyaudio
import wave

'''
    Python调用麦克风生成WAV文件
'''

input_filename = "input.wav"               # 麦克风采集的语音输入
input_filepath = "音频存储位置"              # 输入文件的path
in_path = input_filepath + input_filename

def get_audio(filepath):
    aa = str(input("是否开始录音？   （是/否）"))
    if aa == str("是") :
        CHUNK = 256
        FORMAT = pyaudio.paInt16
        CHANNELS = 1                # 声道数
        RATE = 16000                # 样率采
        RECORD_SECONDS = 10
        WAVE_OUTPUT_FILENAME = filepath
        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("*"*10, "开始录音：请在", RECORD_SECONDS, "秒内输入语音")
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print("*"*10, "录音结束\n")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
    elif aa == str("否"):
        exit()
    else:
        print("无效输入，请重新选择")
        get_audio(in_path)

# if __name__ == '__main__':
#     get_audio(in_path)
