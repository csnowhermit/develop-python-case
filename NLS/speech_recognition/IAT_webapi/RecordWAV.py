# -*- coding：utf-8 -*-

import pyaudio
import wave
import time
import numpy as np

'''
    录音，并转pcm文件
'''

data = None

'''
    循环录音到同一个文件
'''
def loop_recording(filepath):
    CHUNK = 256
    FORMAT = pyaudio.paInt16
    CHANNELS = 1  # 声道数
    RATE = 16000  # 采样率
    RECORD_SECONDS = 60    # 录制时间：60s
    WAVE_OUTPUT_FILENAME = filepath
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)

    print("*" * 10, "开始录音：请在", RECORD_SECONDS, "秒内输入语音")
    frames = []
    batches = int(RATE / CHUNK)
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        if i % batches == 0:
            print("\r[{0}]".format(int(RECORD_SECONDS - i / batches)), end='', flush=True)
        data = stream.read(CHUNK)
        frames.append(data)    # 原本为一个文件写一次，现在改为动一下写一次
        # print(type(frames), frames)
        # print(type(data), data)
        wf.writeframes(b''.join(frames))
        frames = []    # 写完一批清空后再写下一批
    print("*" * 10, "录音结束\n")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf.close()


def wav2pcm(wav_file, to_pcm):
    f = open(wav_file, 'rb')
    f.seek(0)
    f.read(44)
    data = np.fromfile(f, dtype=np.int16)
    data.tofile(to_pcm)


if __name__ == '__main__':
    dir_paths = ['D:/data/iat/']
    to_pcm = "D:/data/loop_recording.pcm"

    while True:
        inputfile = dir_paths[0] + str(time.time()).replace('.', '') + ".wav"
        print(inputfile)
        loop_recording(inputfile)    # 录音
        # wav2pcm(inputfile, to_pcm)       # 转pcm文件
