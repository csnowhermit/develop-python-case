
import speech_recognition as sr

'''
    python离线语音识别：speechRecognition包+pocketsphinx包
    参考自：https://blog.csdn.net/linmy3303/article/details/104625770
    A11_0.wav：绿是阳春烟景，大块文章的底色，四月的林峦更是绿得鲜活、秀魅、诗意盎然。
'''

# obtain audio from the microphone
recognizer = sr.Recognizer()
harvard = sr.AudioFile(r"./A11_0.wav")
with harvard as source:
    audio = recognizer.record(source)
# recognize speech using Sphinx
# r.recognize_sphinx()可与CMU Sphinx 引擎脱机工作，其他六个识别器都需要连接互联网
try:
    result = recognizer.recognize_sphinx(audio, language='zh-CN')
    print("Sphinx thinks you said: " + result)    # 指定中文识别
except sr.UnknownValueError:
    print("Sphinx could not understand audio")
except sr.RequestError as e:
    print("Sphinx error: {0}".format(e))
