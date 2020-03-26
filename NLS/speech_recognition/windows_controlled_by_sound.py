# -*- coding: utf-8 -*-

# 导入模块
from datetime import datetime          # datetime模块提供用于处理日期和时间的类
import subprocess                      # 子流程模块允许您生成新流程
import speech_recognition as sr        # speech_recognition库，用于执行语音识别并支持Google语音识别等。

'''
    声音控制windows
'''

# speech_recognition库，用于执行语音识别并支持Google语音识别等。
r = sr.Recognizer()
with sr.Microphone() as source:
    print("请说话：")
    audio = r.listen(source)    # 录音

print("===")
# 使用Google语音识别功能识别语音
# Query = r.recognize_google(audio)    # 调用google api会出错，连不上网络
Query = r.recognize_sphinx(audio, language='zh-CN')
print("Query:", Query)


# 使用语音命令功能运行应用程序
def get_app(Q):
    if Q == "time":
        print(datetime.now())
    elif Q == "notepad":
        subprocess.call(['Notepad.exe'])
    elif Q == "calculator":
        subprocess.call(['calc.exe'])
    elif Q == "stikynot":
        subprocess.call(['StikyNot.exe'])
    elif Q == "shell":
        subprocess.call(['powershell.exe'])
    elif Q == "paint":
        subprocess.call(['mspaint.exe'])
    elif Q == "cmd":
        subprocess.call(['cmd.exe'])
    elif Q == "browser":
        subprocess.call(['C:\Program Files\Internet Explorer\iexplore.exe'])
    else:
        print("Sorry ! Try Again")
    return

# 调用get_app（Query）Func。
get_app(Query)