# -*- coding:utf-8 -*-

import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread
import os
import wave
import pyaudio
from commonUtils.redisPSUtil.RedisHelper import RedisHelper

'''
    语音合成、播报回复
    数据来源：redis channel：channel_tts
    发音人：{'小燕': 'xioyan', '小宇': 'xioyu', '小峰': 'xiaofeng', '小梅': 'xiaomei', '小蓉': 'xiaorong', '凯瑟琳': 'catherine'}
            {'许久-亲切男声': 'xujiu', '小萍-知性女声': 'xiaoping', '许小宝-可爱童声': 'xuxiaobao', '小婧-亲切女声': 'xiaojing'}
    男声：xiaoyu（有点生硬）、xiaofeng（音色好点）
        Example：直行200米出门左转。
            xiaoyu：liang3 bai2 mi3
            xiaofeng：liang2 bai3 mi3
    女声：xiaoyan（普通话，太过生硬）、xiaomei（粤语）、xiaorong（四川话）、catherine（英文）
'''

STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识

class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, Text, vcn='xioyan'):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.Text = Text
        self.vcn = vcn     # 发音人

        # 公共参数(common)
        self.CommonArgs = {"app_id": self.APPID}
        # 业务参数(business)，更多个性化参数可在官网查看
        # "vcn": "xioyan"，发音人
        # 小燕（xioyan）、小宇（xioyu）、小峰（xiaofeng）、小梅（xiaomei，粤语）、小蓉（xiaorong）、凯瑟琳（catherine，英语）
        self.BusinessArgs = {"aue": "raw", "auf": "audio/L16;rate=16000", "tte": "utf8"}
        self.BusinessArgs["vcn"] = self.vcn
        self.Data = {"status": 2, "text": str(base64.b64encode(self.Text.encode('utf-8')), "UTF8")}

    # 生成url
    def create_url(self):
        url = 'wss://tts-api.xfyun.cn/v2/tts'
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/tts " + "HTTP/1.1"
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        # 拼接鉴权参数，生成url
        url = url + '?' + urlencode(v)
        # print("date: ",date)
        # print("v: ",v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        # print('websocket url :', url)
        return url

def on_message(ws, message):
    try:
        print(message)
        message =json.loads(message)
        code = message["code"]
        sid = message["sid"]
        audio = message["data"]["audio"]
        audio = base64.b64decode(audio)
        status = message["data"]["status"]
        if status == 2:
            print("ws is closed")
            ws.close()
        if code != 0:
            errMsg = message["message"]
            print("sid:%s call error:%s code is:%s" % (sid, errMsg, code))
        else:
            with open('./demo.pcm', 'ab') as f:
                f.write(audio)
    except Exception as e:
        print("receive msg,but parse exception:", e, message)


# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)


# 收到websocket关闭的处理
def on_close(ws):
    print("### closed ###")


# 收到websocket连接建立的处理
def on_open(ws):
    def run(*args):
        d = {"common": wsParam.CommonArgs,
             "business": wsParam.BusinessArgs,
             "data": wsParam.Data,
             }
        d = json.dumps(d)
        print("------>开始发送文本数据")
        ws.send(d)
        if os.path.exists('./demo.pcm'):
            os.remove('./demo.pcm')

    thread.start_new_thread(run, ())

def pcm2wav(pcm_path):
    print(pcm_path)
    wav_path = pcm_path[pcm_path.rindex("/")+1:].replace(".", "_") + '.wav'
    with open(pcm_path, 'rb') as pcmfile:
        pcmdata = pcmfile.read()
    with wave.open(wav_path, 'wb') as wavfile:
        wavfile.setparams((1, 2, 16000, 0, 'NONE', 'NONE'))
        wavfile.writeframes(pcmdata)
    return wav_path


def play(wav_path):
    chunk = 1024  # 2014kb
    wf = wave.open(wav_path, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), channels=wf.getnchannels(),
                    rate=wf.getframerate(), output=True)

    data = wf.readframes(chunk)  # 读取数据

    while True:
        data = wf.readframes(chunk)
        if len(data) == 0 or data == "":
            break
        stream.write(data)
    stream.stop_stream()  # 停止数据流
    stream.close()
    p.terminate()  # 关闭 PyAudio
    print('play函数结束！')



if __name__ == "__main__":
    rds = RedisHelper()  # 得到实例化对象
    while True:
        data = rds.subscribe("channel_tts").parse_response()
        if data:
            text = str(data[2], encoding="utf-8")
            print(text)

            vcnDict = {'小燕': 'xioyan', '小宇': 'xioyu', '小峰': 'xiaofeng', '小梅': 'xiaomei', '小蓉': 'xiaorong', '凯瑟琳': 'catherine'}

            # 测试时候在此处正确填写相关信息即可运行
            wsParam = Ws_Param(APPID='5d760a37',
                               APIKey='0881cf5a9cb3548c79e654b26f77b572',
                               APISecret='c340e2627a9c1697c117769dbdbb12d5',
                               Text=text,
                               vcn="xiaojing")
            websocket.enableTrace(False)
            wsUrl = wsParam.create_url()
            ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close)
            ws.on_open = on_open
            ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

            # pcm转wav
            wav_path = pcm2wav("./demo.pcm")
            print(wav_path)
            play(wav_path)





        time.sleep(0.5)


