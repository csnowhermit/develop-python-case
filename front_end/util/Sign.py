#!/usr/bin/python26
#encoding=utf-8

'''
    加签工具类
'''

import hashlib
from front_end.util import XmlUtil

def getMD5Sign(signStr):
    '''
        计算MD5加签值
    :param signStr: 待加签的字符串
    :return: 返回加签结果
    '''
    md5 = hashlib.md5()
    md5.update(bytes(signStr, encoding="utf-8"))

    return md5.hexdigest()

def checkMD5Sign(dataDict):
    '''
        对xml的拆包结果进行验签
    :param dataDict: xml拆包后形成的Dict
    :return: 返回验签结果，成功返回True，失败返回False，抛出异常返回 sign error
    '''
    try:
        signValue = dataDict["sign"]  # 获取到加签的值
        signStr = XmlUtil.getSignStr(dataDict=dataDict)  # 获取到用于加验签的字符串
        if signValue ==getMD5Sign(signStr=signStr):
            return True
        else:
            return False
    except Exception:
        return "sign error"



if __name__ == '__main__':
    print(getMD5Sign("Helo"))