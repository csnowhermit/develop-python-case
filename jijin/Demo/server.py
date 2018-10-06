#!/usr/bin/python26

import socket               # 导入 socket 模块

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
        print("recv：" + str(recvXml, encoding="utf-8"))

if __name__ == '__main__':
    main()