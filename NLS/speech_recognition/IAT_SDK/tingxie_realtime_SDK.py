# -*- coding：utf-8 -*-


from ctypes import *
import time
import pyaudio
import win32com.client

'''
    IAT语音听写：输入为麦克风
'''

# FRAME_LEN = 640  # Byte
MSP_SUCCESS = 0
# 返回结果状态
MSP_AUDIO_SAMPLE_FIRST = 1
MSP_AUDIO_SAMPLE_CONTINUE = 2
MSP_AUDIO_SAMPLE_LAST = 4
MSP_REC_STATUS_COMPLETE = 5

# 调用动态链接库
dll = cdll.LoadLibrary("./windows_sdk/iat_sdk_x64.dll")
# 登录参数，apppid一定要和你的下载SDK对应
login_params = b"appid = 5d760a37, work_dir = ."

# 实时录音
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


class Msp:
    def __init__(self):
        pass

    def login(self):
        ret = dll.MSPLogin(None, None, login_params)
        # print('MSPLogin =>', ret)

    def logout(self):
        ret = dll.MSPLogout()
        # print('MSPLogout =>', ret)

    def isr(self, session_begin_params):
        ret = c_int()
        sessionID = c_voidp()
        dll.QISRSessionBegin.restype = c_char_p
        sessionID = dll.QISRSessionBegin(None, session_begin_params, byref(ret))
        #print('QISRSessionBegin => sessionID:', sessionID, '\nret:', ret.value)

        # 每秒【1000ms】  16000 次 * 16 bit 【20B】 ，每毫秒：1.6 * 16bit 【1.6*2B】 = 32Byte
        # 1帧音频20ms【640B】 每次写入 10帧=200ms 【6400B】

        # piceLne = FRAME_LEN * 20
        piceLne = 1638 * 2
        epStatus = c_int(0)
        recogStatus = c_int(0)
        cnt = 0
        frameSize = 8000  # 每一帧的音频大小
        while True:
            cnt = cnt + 1
            print(">", cnt)
            wavData = stream.read(int(frameSize/2))

            ret = dll.QISRAudioWrite(sessionID, wavData, len(wavData), MSP_AUDIO_SAMPLE_FIRST, byref(epStatus), byref(recogStatus))
            # print('len(wavData):', len(wavData), '\nQISRAudioWrite ret:', ret,'\nepStatus:', epStatus.value, '\nrecogStatus:', recogStatus.value)

            time.sleep(0.1)
            if len(wavData) == 0:    # 如果没采集到语音，跳过继续采集
                continue
            ret = dll.QISRAudioWrite(sessionID, wavData, len(wavData), MSP_AUDIO_SAMPLE_CONTINUE, byref(epStatus), byref(recogStatus))
            # print('len(wavData):', len(wavData), 'QISRAudioWrite ret:', ret, 'epStatus:', epStatus.value, 'recogStatus:', recogStatus.value)

            # 添加语音结束标识
            ret = dll.QISRAudioWrite(sessionID, None, 0, MSP_AUDIO_SAMPLE_LAST, byref(epStatus), byref(recogStatus))
            # print('len(wavData):', len(wavData), 'QISRAudioWrite ret:', ret, 'epStatus:', epStatus.value, 'recogStatus:', recogStatus.value)

            # print("\n所有待识别音频已全部发送完毕\n获取的识别结果:")

            # 获取音频
            laststr = ''
            counter = 0
            ret = c_int()
            dll.QISRGetResult.restype = c_char_p
            retstr = dll.QISRGetResult(sessionID, byref(recogStatus), 0, byref(ret))
            if retstr is not None:
                laststr += retstr.decode()
                # print('###', laststr)

            # while recogStatus.value != MSP_REC_STATUS_COMPLETE:    # 由于识别是语音片段分片识别的，需要循环直到识别完成
            #     ret = c_int()
            #     dll.QISRGetResult.restype = c_char_p
            #     retstr = dll.QISRGetResult(sessionID, byref(recogStatus), 0, byref(ret))
            #     if retstr is not None:
            #         laststr += retstr.decode()
            #         print('###',laststr)
            #     # print('ret:', ret.value, 'recogStatus:', recogStatus.value)
            #     counter += 1
            #     time.sleep(0.2)
            #     counter += 1
            #     # if counter == 50:
            #     #     laststr += '讯飞语音识别失败'
            #     #     break
            print(laststr)

        # 不知道为什么注解了？
        #ret = dll.QISRSessionEnd(sessionID, '\0')


        # print('end ret: ', ret)
        # return laststr


def XF_test(audio_rate):
    msp = Msp()
    #print("登录科大讯飞")
    msp.login()
    #print("科大讯飞登录成功")
    session_begin_params = b"sub = iat, ptt = 0, result_encoding = utf8, result_type = plain, domain = iat"
    if 16000 == audio_rate:
        session_begin_params = b"sub = iat, domain = iat, language = zh_cn, accent = mandarin, sample_rate = 16000, result_type = plain, result_encoding = utf8"
    msp.isr(session_begin_params)    # 该方法中循环采集语音，进行识别


def main():
    # 如果代码作为外置包被其他程序调用，请注释掉下两行；单独使用时保留
    XF_test(16000)

if __name__ == '__main__':
    main()