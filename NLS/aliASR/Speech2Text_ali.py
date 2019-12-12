# -*- coding: utf-8 -*-

import os
import time
import pyttsx3
import threading
import ali_speech
from ali_speech.callbacks import SpeechRecognizerCallback
from ali_speech.constant import ASRFormat
from ali_speech.constant import ASRSampleRate

'''
    语音转文字：调阿里API
'''

class MyCallback(SpeechRecognizerCallback):


    """
    构造函数的参数没有要求，可根据需要设置添加
    示例中的name参数可作为待识别的音频文件名，用于在多线程中进行区分
    """
    def __init__(self, name='default'):
        self._name = name

    def on_started(self, message):
        print('MyCallback.OnRecognitionStarted: %s' % message)

    def on_result_changed(self, message):
        print('MyCallback.OnRecognitionResultChanged: file: %s, task_id: %s, result: %s' % (
            self._name, message['header']['task_id'], message['payload']['result']))

    def on_completed(self, message):
        print('MyCallback.OnRecognitionCompleted: file: %s, task_id:%s, result:%s' % (
            self._name, message['header']['task_id'], message['payload']['result']))
        with open("./ali_result.txt", 'w', encoding='utf-8') as f:
            f.write(str(message['payload']['result']))
            f.flush()

    def on_task_failed(self, message):
        print('MyCallback.OnRecognitionTaskFailed: %s' % message)

    def on_channel_closed(self):
        print('MyCallback.OnRecognitionChannelClosed')

def process(client, appkey, token):
    audio_name = '../waveFeature/nls-sample-16k.wav'
    callback = MyCallback(audio_name)
    recognizer = client.create_recognizer(callback)
    recognizer.set_appkey(appkey)
    recognizer.set_token(token)
    recognizer.set_format(ASRFormat.PCM)
    recognizer.set_sample_rate(ASRSampleRate.SAMPLE_RATE_16K)
    recognizer.set_enable_intermediate_result(False)
    recognizer.set_enable_punctuation_prediction(True)
    recognizer.set_enable_inverse_text_normalization(True)

    try:
        ret = recognizer.start()
        if ret < 0:
            return ret
        print('sending audio...')
        with open(audio_name, 'rb') as f:
            audio = f.read(3200)
            while audio:
                ret = recognizer.send(audio)
                if ret < 0:
                    break
                time.sleep(0.1)
                audio = f.read(3200)
        recognizer.stop()
    except Exception as e:
        print(e)
    finally:
        recognizer.close()

    with open("./ali_result.txt", encoding='utf-8') as f:
        result = f.read()

        engine = pyttsx3.init()
        print(result)
        engine.say("提问：%s" % result)

        answer = "北京天气：晴，20~33摄氏度，西北风3-4级"
        print(answer)
        engine.say("回答：%s" % answer)
        engine.runAndWait()


def process_multithread(client, appkey, token, number):
    thread_list = []
    for i in range(0, number):
        thread = threading.Thread(target=process, args=(client, appkey, token))
        thread_list.append(thread)
        thread.start()
    for thread in thread_list:
        thread.join()

if __name__ == "__main__":
    client = ali_speech.NlsClient()
    # 设置输出日志信息的级别：DEBUG、INFO、WARNING、ERROR
    client.set_log_level('INFO')
    # appkey = '您的appkey'
    # token = '您的Token'

    appkey = "P4XS02DsBCVhQBn2"
    token = "53c1bd0aef3d4684b2edc053aa0a3896"
    process(client, appkey, token)
    # 多线程示例
    # process_multithread(client, appkey, token, 2)


