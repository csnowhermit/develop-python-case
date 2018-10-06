#!/usr/bin/python26
# encoding=utf-8

'''
    发邮件通知
'''

import smtplib
from email.mime.text import MIMEText
import traceback


class smtpNotify():
    def __init__(self, to_list, server_host, username, password):
        '''
        初始化发邮件相关参数
        :param to_list: 收件人列表
        :param server_host: 邮件服务器host
        :param username: 发件人用户名
        :param password: 发件人密码
        '''
        self.to_list = to_list
        self.server_host = server_host
        self.username = username
        self.password = password

    def send(self, subject, content):
        '''
        发送邮件
        :param to_list: 收件人列表
        :param subject: 主题
        :param content: 内容
        :return:
        '''
        me = "manager" + "<" + self.username + ">"
        # _subtype 可以设为html，默认是plain
        msg = MIMEText(content, _subtype='plain')
        msg['Subject'] = subject
        msg['From'] = me
        msg['To'] = ';'.join(self.to_list)
        try:
            server = smtplib.SMTP()
            server.connect(self.server_host)
            server.login(self.username, self.password)
            server.sendmail(me, to_list, msg.as_string())
            server.getreply()  # 获取返回信息
            server.close()
        except:
            traceback.print_exc()


if __name__ == '__main__':
    to_list = ['920164255@qq.com', '492259023@qq.com']
    server_host = 'smtp.agree.com.cn'
    username = '********@agree.com.cn'
    password = ''

    sn = smtpNotify(to_list=to_list, server_host=server_host, username=username, password=password)

    subject = "TestSubject"
    content = "this is a test mail"

    sn.send(subject=subject, content=content)
    print("邮件发送成功")
