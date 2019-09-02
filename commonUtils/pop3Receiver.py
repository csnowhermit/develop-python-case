#!/usr/bin/python26
# encoding=utf-8

'''
    pop3收邮件
'''

import poplib

try:
    emailServer = poplib.POP3('192.168.100.101', 2525)
    emailServer.user('admin')
    emailServer.pass_('123456')  # 遇到认证失败的话这一行可去掉试试
except Exception as e:
    print(str(e))

# 设置为1，可查看向pop3服务器提交了什么命令
emailServer.set_debuglevel(1)

# 获取欢迎信息
serverWelcome = emailServer.getwelcome()
print(serverWelcome)

# 获取一些统计信息
emailMsgNum, emailSize = emailServer.stat()
print('email number is %d and size is %d' % (emailMsgNum, emailSize))

# 遍历邮件，并打印出每封邮件的标题
for i in range(emailMsgNum):
    for piece in emailServer.retr(i + 1)[1]:
        if piece.startswith('Subject'):
            print('\t' + piece)
            break

emailServer.quit()
