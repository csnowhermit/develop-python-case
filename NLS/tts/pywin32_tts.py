import win32com.client

'''
    python调用win10 tts
'''

speaker = win32com.client.Dispatch('SAPI.SpVoice')

str = '''
    静夜思 李白
    床前明月光，疑是地上霜。
    举头望明月，低头思故乡。
'''

speaker.Speak(str)