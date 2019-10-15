import speech

'''
    调用win10自带语音识别
'''

while True:
    say = speech.input()  # 接收语音
    speech.say("you said:" + say)  # 说话
    print(type(say), say)

    if say == "你好":
        speech.say("How are you?")
    elif say == "天气":
        speech.say("今天天气晴!")
    else:
        speech.say("听不懂！")
