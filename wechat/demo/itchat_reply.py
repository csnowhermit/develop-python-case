# -*- coding: utf-8 -*-
# https://itchat.readthedocs.io/zh/latest/tutorial/tutorial0/
# 微信测试：自动回复原消息
# 收到的消息样例如下：
# {'MsgId': '7098218771104089956', 'FromUserName': '@ad94276eb5e2848ed945acc7f6be02c51b03b7eb4b5cbed3911d838917691a69', 'ToUserName': '@54c7010e2a17ec0a0cc18a14789c5e43783b014a2bbb769ef3c171bd18ae387a', 'MsgType': 1, 'Content': 'hello', 'Status': 3, 'ImgStatus': 1, 'CreateTime': 1537320904, 'VoiceLength': 0, 'PlayLength': 0, 'FileName': '', 'FileSize': '', 'MediaId': '', 'Url': '', 'AppMsgType': 0, 'StatusNotifyCode': 0, 'StatusNotifyUserName': '', 'RecommendInfo': {'UserName': '', 'NickName': '', 'QQNum': 0, 'Province': '', 'City': '', 'Content': '', 'Signature': '', 'Alias': '', 'Scene': 0, 'VerifyFlag': 0, 'AttrStatus': 0, 'Sex': 0, 'Ticket': '', 'OpCode': 0}, 'ForwardFlag': 0, 'AppInfo': {'AppID': '', 'Type': 0}, 'HasProductId': 0, 'Ticket': '', 'ImgHeight': 0, 'ImgWidth': 0, 'SubMsgType': 0, 'NewMsgId': 7098218771104089956, 'OriContent': '', 'EncryFileName': '', 'User': <User: {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@ad94276eb5e2848ed945acc7f6be02c51b03b7eb4b5cbed3911d838917691a69', 'NickName': 'alias', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=679784990&username=@ad94276eb5e2848ed945acc7f6be02c51b03b7eb4b5cbed3911d838917691a69&skey=@crypt_4d7745_70fe54348be9ed8d975b0c1d6ade3a08', 'ContactFlag': 1, 'MemberCount': 0, 'RemarkName': '小号', 'HideInputBarFlag': 0, 'Sex': 0, 'Signature': '', 'VerifyFlag': 0, 'OwnerUin': 0, 'PYInitial': 'ALIAS', 'PYQuanPin': 'alias', 'RemarkPYInitial': 'XH', 'RemarkPYQuanPin': 'xiaohao', 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'AttrStatus': 135205, 'Province': '广东', 'City': '广州', 'Alias': '', 'SnsFlag': 0, 'UniFriend': 0, 'DisplayName': '', 'ChatRoomId': 0, 'KeyWord': '', 'EncryChatRoomId': '', 'IsOwner': 0}>, 'Type': 'Text', 'Text': 'hello'}

import itchat
import threading

@itchat.msg_register(itchat.content.TEXT)
def print_Text(msg):
    user = msg['User']
    nickName = user['NickName']
    retStr = nickName + " 说：" + msg['Text']
    print(retStr)
    return retStr

@itchat.msg_register(itchat.content.PICTURE)
def print_Picture(msg):
    return u"不好意思，我智商不够，暂时解析不了图片"

@itchat.msg_register(itchat.content.RECORDING)
def print_Recording(msg):
    return u"不好意思，我智商不够，暂时解析不了语音"

@itchat.msg_register(itchat.content.CARD)
def print_Card(msg):
    return u"不好意思，我智商不够，暂时解析不了名片"

class TextThread(threading.Thread):
    '''
        继承父类threading.Thread
    '''
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self, msg):
        '''
            把要执行的代码写到run函数里面 线程在start()后会直接运行run函数
        :return:
        '''
        while True:
            print_Text(msg)

    def __del__(self):
        '''
        线程销毁，所有变量清空
        :return:
        '''
        self.threadID = None

class PictureThread(threading.Thread):
    '''
        继承父类threading.Thread
    '''
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self, msg):
        '''
            把要执行的代码写到run函数里面 线程在start()后会直接运行run函数
        :return:
        '''
        while True:
            print_Picture(msg)

    def __del__(self):
        '''
        线程销毁，所有变量清空
        :return:
        '''
        self.threadID = None

class RecordingThread(threading.Thread):
    '''
        继承父类threading.Thread
    '''
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self, msg):
        '''
            把要执行的代码写到run函数里面 线程在start()后会直接运行run函数
        :return:
        '''
        while True:
            print_Recording(msg)

    def __del__(self):
        '''
        线程销毁，所有变量清空
        :return:
        '''
        self.threadID = None

class CardThread(threading.Thread):
    '''
        继承父类threading.Thread
    '''
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self, msg):
        '''
            把要执行的代码写到run函数里面 线程在start()后会直接运行run函数
        :return:
        '''
        while True:
            print_Card(msg)

    def __del__(self):
        '''
        线程销毁，所有变量清空
        :return:
        '''
        self.threadID = None


itchat.auto_login()
itchat.run()

if __name__ == '__main__':
    TextThread(threadID=str("TextThread").__hash__()).start()
    PictureThread(threadID=str("PictureThread").__hash__()).start()
    RecordingThread(threadID=str("RecordingThread").__hash__()).start()
    CardThread(threadID=str("CardThread").__hash__()).start()