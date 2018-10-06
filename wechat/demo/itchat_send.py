# -*- coding: utf-8 -*-
# https://itchat.readthedocs.io/zh/latest/tutorial/tutorial0/
# 微信测试：主动发送消息

import time
import itchat

itchat.auto_login(hotReload=True)
# itchat.auto_login()
# itchat.run()

receiver = itchat.search_friends(name='小号')
print(receiver)

username = receiver[0]['UserName']
print(username)

# 第一个参数为要发送的内容，第二个参数为接收者的UserName（我的小号）
res1 = itchat.send_msg(u'Hello World - ' + str(time.time()), toUserName=username)
print(res1)

# 给文件传输助手发消息
res2 = itchat.send('Hello, filehelper', toUserName='filehelper')  # 这条是成功的

print(res2)

