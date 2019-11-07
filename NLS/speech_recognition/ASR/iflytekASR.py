#-*- encoding:utf-8 -*-

import sys
import hashlib
from hashlib import sha1
import hmac
import base64
from socket import *
import json, time, threading
from websocket import create_connection
import websocket
from urllib.parse import quote
import logging
import pyaudio

'''
    读取pcm文件进行实时语音转写
'''

logging.basicConfig()

base_url = "wss://rtasr.xfyun.cn/v1/ws"
app_id = "5d760a37"
api_key = "e5aba0511eea04e2ab986cdf1e4b6972"
# file_path = "../iflytek/静夜思_李白.pcm"
# file_path = "D:/data/iat_tingxie/157242600644468.wav"

end_tag = "{\"end\": true}"

CHUNK = 256
FORMAT = pyaudio.paInt16
CHANNELS = 1  # 声道数
RATE = 16000  # 采样率
# RECORD_SECONDS = 60

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

class Client():
    def __init__(self):
        # 生成鉴权参数，公式：HmacSHA1(MD5(appid + ts), api_key)
        ts = str(int (time.time()))
        tmp = app_id + ts
        hl = hashlib.md5()    # h1.hexdigest()，返回16进制
        hl.update(tmp.encode(encoding='utf-8'))    # MD5(appid + ts)
        # my_sign = hmac.new(api_key, hl.hexdigest(), sha1).digest()
        my_sign = hmac.new(bytes(api_key, 'utf-8'), bytes(hl.hexdigest(), 'utf-8'), digestmod='sha1').digest()
        signa = base64.b64encode(my_sign)

        self.ws = create_connection(base_url + "?appid=" + app_id + "&ts=" + ts + "&signa=" + quote(signa))
        self.trecv = threading.Thread(target=self.recv)
        self.trecv.start()

    def send(self):
        # file_object = open(file_path, 'rb')
        try:
            index = 1
            while True:
                # chunk = file_object.read(1280)    # 实施转写问题，可以实时往pcm中写入
                chunk = stream.read(1280)
                print(type(chunk), len(chunk), index)
                if not chunk:      # 如果当前没读到，说明暂时没人问，continue
                    continue
                # self.ws.send(chunk)      # 分批发送识别

                index += 1
                time.sleep(0.04)
        finally:
            # print str(index) + ", read len:" + str(len(chunk)) + ", file tell:" + str(file_object.tell())
            # file_object.close()
            pass

        # self.ws.send(bytes(end_tag, encoding='utf-8'))
        print("send end tag success")

    def recv(self):
        try:
            while self.ws.connected:
                result = str(self.ws.recv())
                if len(result) == 0:
                    print("receive result end")
                    break
                result_dict = json.loads(result)

                # 解析结果
                if result_dict["action"] == "started":
                    print("handshake success, result: " + result)

                if result_dict["action"] == "result":
                    print("rtasr result: " + result)

                if result_dict["action"] == "error":
                    print("rtasr error: " + result)
                    self.ws.close()
                    return
        except websocket.WebSocketConnectionClosedException:
            print("receive result end")

    def close(self):
        self.ws.close()
        print("connection closed")




if __name__ == '__main__':
    client = Client()
    client.send()