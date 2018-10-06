#!/usr/bin/python
# -*- coding: UTF-8 -*-

import socket               # 导入 socket 模块
from front_end.CommonUtils import ParseXml
from front_end.CommonUtils import Sign

def main():
    server = socket.socket()  # 创建 socket 对象
    host = socket.gethostname()  # 获取本地主机名
    port = 12345  # 设置端口
    server.bind((host, port))  # 绑定端口

    server.listen(5)  # 等待客户端连接
    while True:
        c, addr = server.accept()  # 建立客户端连接。
        print('连接地址：', addr)
        recvXml = c.recv(4096)  # 获取到前置应用转发过来的xml报文
        print("前置机的xml报文：" + str(recvXml, encoding="utf-8"))

        newDataDict = ParseXml.unpackXml(recvXml, feature="xml")  # 拆包

        signResult = Sign.checkMD5Sign(dataDict=newDataDict)  # 进行验签
        if signResult == True:
            print("验签成功")
        elif signResult == False:
            print("验签失败")
        else:
            print(signResult)

        signResult = str(signResult)
        # print(signResult)
        c.send(bytes(signResult, "utf-8"))  # 将验签结果返回给前置机
        # print(c.recv(1024))
        c.close()  # 关闭连接

if __name__ == '__main__':
    main()