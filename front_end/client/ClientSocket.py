#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
    通过socket发送xml报文
    数据路由：SocketClient(12333) -> rinetd -> 前置应用(12333, 12345) -> SocketServer(12345)
'''

import socket               # 导入 socket 模块
from front_end.util import SocketAdaptor

def main():
    # client = socket.socket()  # 创建 socket 对象
    # host = socket.gethostname()  # 获取本地主机名
    # # host = "192.168.117.128"
    # port = 12333  # 设置端口号
    # print(host)
    client = SocketAdaptor.getOutSocketAdaptor(socket.gethostname(), 12333)
    # client.connect((host, port))

    xml = "<xml><appid><![CDATA[wx1f87d44db95cba7a]]></appid><charset><![CDATA[UTF-8]]></charset><mch_id><![CDATA[7551000001]]></mch_id><nonce_str><![CDATA[c0aa8e4423a146d48caca9ae0a95c570]]></nonce_str><out_refund_id_0><![CDATA[50000306132018032603956710803]]></out_refund_id_0><out_refund_no_0><![CDATA[wechat20180326112302fHEGKLdk98]]></out_refund_no_0><out_trade_no><![CDATA[wechat20180326112302fHEGKLdk98]]></out_trade_no><out_transaction_id><![CDATA[4200000066201803265831178939]]></out_transaction_id><refund_channel_0><![CDATA[ORIGINAL]]></refund_channel_0><refund_count><![CDATA[1]]></refund_count><refund_fee_0><![CDATA[1]]></refund_fee_0><refund_id_0><![CDATA[7551000001201803261153251711]]></refund_id_0><refund_status_0><![CDATA[PROCESSING]]></refund_status_0><refund_time_0><![CDATA[20180326112243]]></refund_time_0><result_code><![CDATA[0]]></result_code><sign><![CDATA[5pGD84UsIgcTlm8YCsUqbV9/W3Cew67FMRxil2zGorq63AGB+R0b1VllrE/Z8ZwIurTIVaNZR1P8W+gPZAEnNA==]]></sign><sign_type><![CDATA[SM3WITHSM2]]></sign_type><status><![CDATA[0]]></status><trade_type><![CDATA[pay.weixin.native]]></trade_type><transaction_id><![CDATA[7551000001201803266215107977]]></transaction_id><version><![CDATA[2.0]]></version></xml>"
    client.send(bytes(xml, encoding="utf-8"))
    recvFromFront = client.recv(1024)
    recvStr = str(recvFromFront, encoding="utf-8")
    if recvStr == "True":
        print("收到Server->Front的返回：验签成功")
    elif recvStr == "False":
        print("收到Server->Front的返回：验签失败")
    else:
        print(recvStr)

    client.close()

if __name__ == '__main__':
    main()