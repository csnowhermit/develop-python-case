# -*- coding:utf-8 -*-

import os
import redis
import hashlib
import traceback
from NLP.Logger import *
from NLP.textCategory.utils.SubmitActionUtil import submit_msg
from NLS.tts.tts_webapi import tts_key, base_dir, play

'''
    后消费者：将回答切分，传给前端
'''

log = Logger('D:/data/PostConsumer.log', level='info')

directions1 = ['东', '西', '南', '北']
directions2 = ['直行', '上', '下', '左', '右', '左右']

r = redis.Redis(host="192.168.117.134", port=6379, password="123456")

'''
    分析回答并通知前端
    Note：新增参数param，两套日志系统，便于通过uid排错
'''
def notice(uid, message):
    def call_remote(*args):    # 用于thread.start_new_thread()调用
        submit_msg(forward, actions, play_filepath)

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

    # # 1.开启新线程通知前端
    # thread.start_new_thread(call_remote, ())

    # # 将要合成的字符串写入channel
    # r.publish(channel="channel_tts", message=msg)
    try:
        key = hashlib.md5(str(msg).strip().encode("utf-8")).hexdigest()
        play_filepath = r.hget(tts_key, str(key).strip()).decode("utf-8")

        response = submit_msg(forward, actions, play_filepath)  # 手势动作发送到前端
        play(os.path.join(base_dir, play_filepath))  # 播放回答文件
        # print(response, forward, msg, locateArr, actions)
        log.logger.info((uid, forward, msg, locateArr, actions))
    except:
        log.logger.error((uid, forward, msg, locateArr, actions))
        log.logger.error(traceback.format_exc())
    return (uid, forward, msg, locateArr, actions)

'''
    合成语音播放
'''
def tts(msg):
    pass

def main():
    message = "指西，直行200米不出门，左侧电梯上3楼。"
    uid = "123.1@2"
    notice(uid, message)

if __name__ == '__main__':
    main()