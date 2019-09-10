# _*_ coding:utf-8 _*_

from win32com.client import constants
import os
import win32com.client
import pythoncom

'''
    利用pythoncom包实现语音识别：Windows语音输入识别
'''

speaker = win32com.client.Dispatch("SAPI.SPVOICE")

class SpeechRecognition:
    def __init__(self, wordsToAdd):
        self.speaker = win32com.client.Dispatch("SAPI.SpVoice")
        self.listener = win32com.client.Dispatch("SAPI.SpSharedRecognizer")
        self.context = self.listener.CreateRecoContext()
        self.grammar = self.context.CreateGrammar()
        self.grammar.DictationSetState(0)
        self.wordsRule = self.grammar.Rules.Add("wordsRule", constants.SRATopLevel + constants.SRADynamic, 0)
        self.wordsRule.Clear()# [self.wordsRule.InitialState.AddWordTransition(None, word) for word in wordsToAdd]
        self.grammar.Rules.Commit()
        self.grammar.CmdSetRuleState("wordsRule", 1)
        self.grammar.Rules.Commit()
        self.eventHandler = ContextEvents(self.context)
        self.say("Started successfully")
    def say(self, phrase):
        self.speaker.Speak(phrase)
class ContextEvents(win32com.client.getevents("SAPI.SpSharedRecoContext")):
    def OnRecognition(self, StreamNumber, StreamPosition, RecognitionType, Result):
        newResult = win32com.client.Dispatch(Result)
        print("你在说 ", newResult.PhraseInfo.GetText())
        speechstr=newResult.PhraseInfo.GetText()
        # 下面即为语音识别信息对应
        if  speechstr=="张三":
            speaker.Speak("lisi")
        elif  speechstr=="你好":
            speaker.Speak("hello world")
        elif  speechstr=="国庆快乐":
            speaker.Speak("Happy   nationalday")
        elif  speechstr=="新年快乐":
            speaker.Speak("happy  New Year")
        elif  speechstr=="李四":
            speaker.Speak("a  beauty baby")
        elif  speechstr=="王五":
            speaker.Speak("a  little boy")
        elif  speechstr=="赵六":
            speaker.Speak("a  boy  can  coding")
        else:
            pass

if __name__ == '__main__':

    speaker.Speak("语音识别开启")
    wordsToAdd = ["张三",
                  "你好",
                  "国庆快乐",
                  "新年快乐",
                  "李四",
                  "王五",
                  "赵六",]
    speechReco = SpeechRecognition(wordsToAdd)
    while True:
        pythoncom.PumpWaitingMessages()