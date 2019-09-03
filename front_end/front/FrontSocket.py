#!/usr/bin/python26
#encoding=utf-8

'''
    前置应用
'''
import socket
from front_end.util import XmlUtil
from front_end.util import Sign

def sign(recvXml, feature):
    dataDict = XmlUtil.unpackXml(xml=recvXml, feature=feature)  # 拆包完成后
    # print(dataDict)

    signStr = XmlUtil.getSignStr(dataDict=dataDict)  # 拼接加签字符串
    # print(signStr)

    sign = Sign.getMD5Sign(signStr=signStr)  # md5加签
    # print(sign)

    signKeyAndValue = "sign=" + sign
    newDataDict = XmlUtil.updateDict(dataDict=dataDict, signKeyAndValue=signKeyAndValue)  # 加签后新拼装的Dict
    # print(newDataDict)

    newXml = XmlUtil.pack2Xml(newDataDict)  # 拼包成新的xml报文
    return newXml

def main():
    # 前置机SocketServer：接收来自rinetd或客户端的报文
    frontServer = socket.socket()  # 创建 socket 对象
    host = socket.gethostname()  # 获取本地主机名
    port = 12333  # 设置端口
    frontServer.bind((host, port))  # 绑定端口

    frontServer.listen(5)  # 等待客户端连接
    while True:
        c, addr = frontServer.accept()  # 建立客户端连接。
        print('连接地址：', addr)
        recvXml = c.recv(4096)  # 接收到来自客户端的xml报文
        print("客户端的xml报文：" + str(recvXml, encoding="utf-8"))

        # 前置机SocketClient：将加签过的报文发送至服务端
        front2Server = socket.socket()  # 创建 socket 对象
        host = socket.gethostname()  # 获取本地主机名
        port = 12345  # 设置端口号

        front2Server.connect((host, port))
        newXml = sign(recvXml=recvXml, feature="xml")
        front2Server.send(bytes(newXml, encoding="utf-8"))

        recvFromServer = front2Server.recv(4096)  # 得到服务端的验签结果
        recvFromServer = str(recvFromServer, encoding="utf-8")
        print("服务端的验签结果为：" + recvFromServer)
        front2Server.close()  # 将连接到服务端的连接关闭

        c.send(bytes(str(recvFromServer), "utf-8"))  # 将服务端的眼前结果返回给客户端
        # print(c.recv(4096))
        c.close()  # 关闭连接

if __name__ == '__main__':
    main()


