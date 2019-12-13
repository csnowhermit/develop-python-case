# -*- coding:utf-8 -*-

import os
from collections import Counter
from NLP.Logger import *
from NLP.textCategory.utils.SubmitActionUtil import submit_msg

'''
    后消费者：将回答切分，传给前端
'''

log = Logger('D:/data/PostConsumer.log', level='info')

directions1 = ['东', '西', '南', '北']
directions2 = ['直行', '上', '下', '左', '右', '左右']

'''
    分析回答并通知前端
    Note：新增参数param，两套日志系统，便于通过uid排错
'''
def notice(uid, message):
    forward = message[0:2]    # 指向
    msg = message[3:]         # 要合成的语音
    locateArr = []    # 指向后的序列
    actions = []      # 指令序列
    for d in directions2:
        if msg.find(d) > -1:
            locateArr.append(msg.find(d))

    locateArr = sorted(locateArr)
    prev = -2    # 不设-1，避免在0处误识别为now == prev + 1，即“左右、右”的情况
    for a in locateArr:
        now = a
        if now == prev:    # 出现 左、左右 的情况
            # actions.remove(len(actions) - 1)    # 1.先将 左 删掉
            actions.pop()    # 1.弹出最后一个元素：左
            actions.append(directions2[len(directions2) - 1])    # 2.原处添加 左右
        elif now == prev + 1:    # 出现 左右、右 的情况
            continue      # 该情况下，紧跟后续的 右 无需截取出来
        else:
            actions.append(msg[now])
        prev = now

    # 分析完成之后通知前端
    response = submit_msg(forward, actions)
    # print(response, forward, msg, locateArr, actions)
    log.logger.info((uid, response, forward, msg, locateArr, actions))
    return (uid, response, forward, msg, locateArr, actions)

'''
    合成语音播放
'''
def tts():
    pass

def main():
    message = "指西，直行200米不出门，左侧电梯上3楼。"
    notice(message)

if __name__ == '__main__':
    main()