#!/usr/bin/python26
#encoding=utf-8

import socket

'''
    Socket接入接出适配器
'''


def getOutSocketAdaptor(host, port):
    '''
        获取一个socket接出适配器
    :param host: 主机名或ip地址
    :param port: 端口号
    :return: 返回socket接出适配器
    '''
    client = socket.socket()  # 创建 socket 对象
    # host = socket.gethostname()  # 获取本地主机名
    client.connect((host, port))

    return client