# -*- coding:utf-8 -*-

import os
import json
import requests

'''
    向交互模块提交指令
'''

# 方向：中文-字母代号对应关系
positionDict = {}
positionDict["指东"] = "EAST"
positionDict["指西"] = "WEST"
positionDict["指南"] = "SOUTH"
positionDict["指北"] = "NORTH"
positionDict["上"] = "UP"
positionDict["下"] = "DOWN"
positionDict["左"] = "LEFT"
positionDict["右"] = "RIGHT"
positionDict["左右"] = "LeftRight"
positionDict["直"] = "StraightLine"    # 直行，straight line
positionDict["回答"] = "AnswersNotFound"


def submit_msg(forward, actions, play_filepath):
    # 伪装成浏览器
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
    base_url = "http://localhost:80/"

    # # GET请求
    # get_url = base_url + "?forward=" + str(positionDict[forward]) + "&actions="
    # for a in actions:
    #     get_url = get_url + positionDict[a] + "_"
    #
    # get_url = get_url[0:-1]
    # print(get_url)
    # # response = requests.request("GET", get_url)
    # response = requests.get(get_url)    # GET请求下，两种提交方式都可以

    # POST请求
    actionArr = ""
    data = {}
    for a in actions:
        actionArr = actionArr + positionDict[a] + "_"
    actionArr = actionArr[0: -1]

    data["forward"] = positionDict[forward]
    data["actions"] = actionArr
    data['play_filename'] = play_filepath
    response = requests.post(base_url, json.dumps(data))
    return response

def main():
    forward = "指东"
    actions = ['直', '左右', '上']
    play_filepath = "/test.wav"
    response = submit_msg(forward, actions, play_filepath)
    print(response)

if __name__ == '__main__':
    main()