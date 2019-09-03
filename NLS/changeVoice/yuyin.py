import subprocess
import sys

# reload(sys)
# sys.setdefaultencoding('utf-8')

enText = "Hello world"
zhText = u"你好世界"
# txtFile = "d:/test.txt"  #文件内为中文
# wavFile = "d:/test.wav"

# 在线发音(-v是设置voice，en是英文，m3男声，zh是中文，f3是女声)
subprocess.call(["D:/Program Files (x86)/eSpeak/TTSApp.exe", "-ven+m3", enText])
subprocess.call(["D:/Program Files (x86)/eSpeak/TTSApp.exe", "-vzh+f3", zhText])

# # 保存为wav文件（第一种方法仅能保存英文wav，如果想保存其他语言wav需要使用第二种方法）
# subprocess.call(["D:/Program Files (x86)/eSpeak/TTSApp.exeD:/Program Files (x86)/eSpeak/TTSApp.exe","-w"+wavFile, enText])
# subprocess.call(["D:/Program Files (x86)/eSpeak/TTSApp.exe","-vzh+f3", "-f"+txtFile, "-w"+wavFile])