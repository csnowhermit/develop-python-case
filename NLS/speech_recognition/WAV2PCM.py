# -*- coding：utf-8 -*-

# wav2pcm.py 文件内容
import os

def wav_to_pcm(wav_file):
    # 假设 wav_file = "音频文件.wav"
    # wav_file.split(".") 得到["音频文件","wav"] 拿出第一个结果"音频文件"  与 ".pcm" 拼接 等到结果 "音频文件.pcm"
    pcm_file = "%s.pcm" %(wav_file.split(".")[0])

    # 就是此前我们在cmd窗口中输入命令,这里面就是在让Python帮我们在cmd中执行命令
    print("ffmpeg.exe -y  -i %s  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 %s"%(wav_file,pcm_file))
    os.system("ffmpeg.exe -y  -i %s  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 %s"%(wav_file,pcm_file))

    return pcm_file

if __name__ == '__main__':
    wav_file = "D:/workspace/openSourceModel/ASRT_SpeechRecognition/dataset/data_thchs30/data/A11_152.wav"
    wav_to_pcm(wav_file)