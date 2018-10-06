#!/usr/bin/python26
# encoding=utf-8
from bs4 import BeautifulSoup

'''
    工具类：解析xml，得到加验签字符串
    要点：
    1、xml中值为空或空字符串或若干空白字符串的去掉
    2、所有键按ASCII码升序排序，键=值之间按照&链接
    3、对拼装成的字符串进行加签操作
'''

# xml = "<xml><appid><![CDATA[wx1f87d44db95cba7a]]></appid><charset><![CDATA[UTF-8]]></charset><mch_id><![CDATA[7551000001]]></mch_id><nonce_str><![CDATA[c0aa8e4423a146d48caca9ae0a95c570]]></nonce_str><out_refund_id_0><![CDATA[50000306132018032603956710803]]></out_refund_id_0><out_refund_no_0><![CDATA[wechat20180326112302fHEGKLdk98]]></out_refund_no_0><out_trade_no><![CDATA[wechat20180326112302fHEGKLdk98]]></out_trade_no><out_transaction_id><![CDATA[4200000066201803265831178939]]></out_transaction_id><refund_channel_0><![CDATA[ORIGINAL]]></refund_channel_0><refund_count><![CDATA[1]]></refund_count><refund_fee_0><![CDATA[1]]></refund_fee_0><refund_id_0><![CDATA[7551000001201803261153251711]]></refund_id_0><refund_status_0><![CDATA[PROCESSING]]></refund_status_0><refund_time_0><![CDATA[20180326112243]]></refund_time_0><result_code><![CDATA[0]]></result_code><sign><![CDATA[5pGD84UsIgcTlm8YCsUqbV9/W3Cew67FMRxil2zGorq63AGB+R0b1VllrE/Z8ZwIurTIVaNZR1P8W+gPZAEnNA==]]></sign><sign_type><![CDATA[SM3WITHSM2]]></sign_type><status><![CDATA[0]]></status><trade_type><![CDATA[pay.weixin.native]]></trade_type><transaction_id><![CDATA[7551000001201803266215107977]]></transaction_id><version><![CDATA[2.0]]></version></xml>"
# xml = "<xml><a><![CDATA[1]]></a><d><![CDATA[4]]></d><c><![CDATA[2]]></c><b><![CDATA[3]]></b><e><![CDATA[           ]]></e></xml>"

def unpackXml(xml, feature):
    '''
        拆包xml报文
    :param xml: 要拆包的xml报文
    :return: 返回拆包后生成的Dict
    '''
    soup = BeautifulSoup(xml, features=feature)
    xml = soup.find('xml')
    # print(xml)

    dataDict = dict([(item.name, item.text) for item in xml.find_all()])
    # print(dataDict)
    return dataDict


def updateDict(dataDict, signKeyAndValue):
    '''
        将新 键=值 对拼包至xml报文中
    :param data: 原xml报文
    :param s: 要拼进原xml报文的键值对
    :return: 返回拼之后的xml报文
    '''
    sArr = signKeyAndValue.split("=")
    # print(sArr)
    if len(sArr)==2:
        # dataDict.update(sArr[0], sArr[1])
        dataDict[sArr[0]]=sArr[1]

    return dataDict

def pack2Xml(dataDict):
    '''
        将Dict转换成XML格式的数据
    :param dataDict: dict对象
    :return: 返回xml格式的数据
    '''
    xml = []
    for k in sorted(dataDict.keys()):
        v  = dataDict.get(k)
        if not v.startswith('<![CDATA['):
            v =  '<![CDATA[{}]]>'.format(v)

        xml.append('<{key}>{value}</{key}>'.format(key=k, value=v))

    return '<xml>{}</xml>'.format(''.join(xml))


def getSignStr(dataDict):
    '''
        获取到用于加验签的字符串
    要点：
    1、xml中值为空或空字符串或若干空白字符串的去掉
    2、所有键按ASCII码升序排序，键=值之间按照&链接
    3、对拼装成的字符串进行加签操作
    :param dataDict: xml拆包后得到的Dict
    :return: 返回用于加验签的字符串
    '''
    # print(type(dataDict))

    keys = dataDict.keys()
    ls = list(keys)

    ls.sort()
    # print("ls: " + str(ls))

    str = ""
    for i in ls:
        # print(i + " ==> " + data.get(i))
        if i == "sign":
            continue
        elif dataDict.get(i) is None:
            continue
        elif dataDict.get(i).isspace():
            continue
        else:
            str = str + i + "=" + dataDict.get(i) + "&"

    # print(str[0:len(str) - 1])
    return str[0:len(str)-1]



