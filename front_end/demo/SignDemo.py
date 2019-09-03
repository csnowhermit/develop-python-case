#!/usr/bin/python26
#encoding=utf-8


from front_end.util.XmlUtil import *
from front_end.util import Sign

xml = "<xml><appid><![CDATA[wx1f87d44db95cba7a]]></appid><charset><![CDATA[UTF-8]]></charset><mch_id><![CDATA[7551000001]]></mch_id><nonce_str><![CDATA[c0aa8e4423a146d48caca9ae0a95c570]]></nonce_str><out_refund_id_0><![CDATA[50000306132018032603956710803]]></out_refund_id_0><out_refund_no_0><![CDATA[wechat20180326112302fHEGKLdk98]]></out_refund_no_0><out_trade_no><![CDATA[wechat20180326112302fHEGKLdk98]]></out_trade_no><out_transaction_id><![CDATA[4200000066201803265831178939]]></out_transaction_id><refund_channel_0><![CDATA[ORIGINAL]]></refund_channel_0><refund_count><![CDATA[1]]></refund_count><refund_fee_0><![CDATA[1]]></refund_fee_0><refund_id_0><![CDATA[7551000001201803261153251711]]></refund_id_0><refund_status_0><![CDATA[PROCESSING]]></refund_status_0><refund_time_0><![CDATA[20180326112243]]></refund_time_0><result_code><![CDATA[0]]></result_code><sign><![CDATA[5pGD84UsIgcTlm8YCsUqbV9/W3Cew67FMRxil2zGorq63AGB+R0b1VllrE/Z8ZwIurTIVaNZR1P8W+gPZAEnNA==]]></sign><sign_type><![CDATA[SM3WITHSM2]]></sign_type><status><![CDATA[0]]></status><trade_type><![CDATA[pay.weixin.native]]></trade_type><transaction_id><![CDATA[7551000001201803266215107977]]></transaction_id><version><![CDATA[2.0]]></version></xml>"

str = "sign=123456789"
dataDict = unpackXml(xml=xml, feature="xml")    # 拆包完成后
print(dataDict)

signStr = getSignStr(dataDict=dataDict)     # 拼接加签字符串
print(signStr)

sign = Sign.getMD5Sign(signStr=signStr)    # md5加签
print(sign)

signKeyAndValue="sign="+sign
newDataDict = updateDict(dataDict=dataDict, signKeyAndValue=signKeyAndValue)    # 加签后新拼装的Dict
print(newDataDict)

print("=====加签成功，准备发往第三方=====")
newXml = pack2Xml(newDataDict)
print("新的xml报文：" + newXml)

newDataDict1 = unpackXml(newXml, feature="xml")


signResult = Sign.checkMD5Sign(dataDict=newDataDict1)
if signResult==True:
    print("验签成功")
elif signResult == False:
    print("验签失败")
else:
    print(signResult)