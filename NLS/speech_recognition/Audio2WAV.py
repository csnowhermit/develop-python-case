# -*- coding：utf-8 -*-

import pyaudio
import wave

'''
    Python调用麦克风生成WAV文件
'''

input_filename = "input.wav"                           # 麦克风采集的语音输入
input_filepath = "D:/data/iat_tingxie/"              # 输入文件的path
in_path = input_filepath + input_filename

def get_audio(filepath):
    aa = str(input("是否开始录音？   （y/N）"))
    if aa == str("y") :
        CHUNK = 256
        FORMAT = pyaudio.paInt16
        CHANNELS = 1                # 声道数
        RATE = 16000                # 采样率
        RECORD_SECONDS = 30
        WAVE_OUTPUT_FILENAME = filepath
        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("*"*10, "开始录音：请在", RECORD_SECONDS, "秒内输入语音")
        frames = []
        batches = int(RATE / CHUNK)
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            if i % batches == 0:
                print("\r[{0}]".format(int(RECORD_SECONDS - i / batches)), end='', flush=True)
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
    elif aa == str("N"):
        exit()
    else:
        print("无效输入，请重新选择")
        get_audio(in_path)

# if __name__ == '__main__':
#     get_audio(in_path)
