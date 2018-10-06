# -*- coding: utf-8 -*-
# https://itchat.readthedocs.io/zh/latest/tutorial/tutorial0/
# 微信测试：接收消息

import itchat

@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
    # print(msg['Text'])
    # print(str(msg))
    print(msg['FromUserName'] + " ==> " + msg['Text'])
    fromUserName = msg['FromUserName']    # 发信人
    text = msg['Text']    # 发信内容

itchat.auto_login(hotReload=True)
itchat.run()

