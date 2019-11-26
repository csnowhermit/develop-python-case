# -*- coding:utf-8 -*-

import pyaudio
import threading, time, queue
from NLS.speech_recognition.IAT_SDK.tingxie_realtime_SDK import Msp

'''
    生产者消费者模式
'''

q = queue.Queue()

# 实时录音
CHUNK = 256
FORMAT = pyaudio.paInt16
CHANNELS = 1  # 声道数
RATE = 16000  # 采样率
RECORD_SECONDS = 60
frameSize = 8000  # 每一帧的音频大小
intervel = 0.04  # 发送音频间隔(单位:s)

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

def Produce(name):
    # while True:
    #     wavData = stream.read(int(frameSize / 2))
    #     q.put(wavData)
    #     time.sleep(intervel)
    wavFile = open("./A11_152.wav", 'rb')
    piceLne = 1638 * 2
    wavData = wavFile.read(piceLne)
    print(type(wavData), len(wavData))
    time.sleep(0.1)
    while wavData:
        wavData = wavFile.read(piceLne)
        # print(type(wavData), wavData)
        if len(wavData) == 0:
            break
        q.put(wavData)
        time.sleep(0.1)
    wavFile.close()


def Consumer(name):
    while True:
        time.sleep(0.2)
        if not q.empty():
            wavData = q.get()
            # print(type(wavData), len(wavData))
            # msp.isr(wavData, session_begin_params)
        else:
            # print("录音中，请稍后。。。")
            pass

if __name__ == '__main__':
    # audio_rate = 16000
    #
    # msp = Msp()
    # print("登录科大讯飞")
    # msp.login()
    # print("科大讯飞登录成功")
    # session_begin_params = b"sub = iat, ptt = 0, result_encoding = utf8, result_type = plain, domain = iat"
    # if 16000 == audio_rate:
    #     session_begin_params = b"sub = iat, domain = iat, language = zh_cn, accent = mandarin, sample_rate = 16000, result_type = plain, result_encoding = utf8"

    # p1 = threading.Thread(target=Produce, args=('乘客',))
    # c1 = threading.Thread(target=Consumer, args=('导台',))
    # p1.start()
    # c1.start()

    wavFile = open("./A11_152.wav", 'rb')
    piceLne = 1638 * 2
    wavData = wavFile.read(piceLne)
    # print(type(wavData), len(wavData))
    time.sleep(0.1)
    while wavData:
        wavData = wavFile.read(piceLne)
        # print(type(wavData), wavData)
        if len(wavData) == 0:
            break
        q.put(wavData)
        time.sleep(0.1)
    wavFile.close()

    print(q.qsize())

    f = open("./A11_152.wav", 'rb')
    data = f.read(piceLne)
    # print(data == q.get())
    print(data)
    # while data:
    #     data = f.read(piceLne)
    #     # print(data == q.get())
    #     print(data)
    #     if len(data) == 0:
    #         break

    while True:
        data = q.get()
        print(data)