# coding:utf-8

"""
本地语音文件识别测试
"""
import speech_recognition as sr
import sys

say = '你看看'
r = sr.Recognizer()

# 本地语音测试
harvard = sr.AudioFile('../changeVoice/原始录音.wav')
with harvard as source:
    # 去噪
    r.adjust_for_ambient_noise(source, duration=0.2)
    audio = r.record(source)

# 语音识别
# test = r.recognize_google(audio, language="cmn-Hans-CN", show_all=True)    # 报错：连不上google云服务
# print(test)

test = r.recognize_sphinx(audio, show_all=True)
print(type(test))
print(test)
print(str(test))

test.save_dict("./test.dict", "")

# for t in test.:
#     print(t)

# # 分析语音
# flag = False
# for t in test['alternative']:
#     print(t)
#     if say in t['transcript']:
#         flag = True
#         break
# if flag:
#     print('Bingo')