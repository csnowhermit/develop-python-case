# -*- coding:utf-8 -*-

import pyaudio
from kafka import KafkaProducer

'''
    采集音频文件，写入kafka
'''

broker_list = "192.168.117.101:9092,192.168.117.102:9092,192.168.117.103:9092"
topic = "daotai_wav"

producer = KafkaProducer(bootstrap_servers=broker_list)

CHUNK = 256
FORMAT = pyaudio.paInt16
CHANNELS = 1  # 声道数
RATE = 16000  # 采样率
RECORD_SECONDS = 60

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
frameSize = 8000

index = 0    # 0表示是第一次，要截取掉wav格式的前44个字符

while True:
    buf = stream.read(int(frameSize / 4))
    if index == 0:
        print(type(buf), len(buf[44:]))
        producer.send(topic=topic, value=buf[44:])
        index = 1
    else:
        print(type(buf), len(buf))
        producer.send(topic=topic, value=buf)

