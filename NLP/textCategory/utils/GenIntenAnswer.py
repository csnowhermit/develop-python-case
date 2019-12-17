# -*- coding:utf-8 -*-

import os
import random
import redis

'''
    加载“语义-回答”
    数据结构：采用hash存储
    hash：
        hset IntenAnswer 坐公交 指西，直行200米出门左转。
        hset IntenAnswer 坐地铁 指东，直行50米下楼。
        hset IntenAnswer 坐车 指西，直行200米不出门，左右两侧电梯上3楼。|指东，直行200米不出门，左右两侧电梯上3楼。
'''

r = redis.Redis(host="192.168.117.134", port=6379, password="123456")
cache_key = "IntenAnswer"
yuyiList = []
default_result = "不好意思，我不理解您说的呢"

'''
    缓存“语义-回答”
'''
def cache():
    if r.exists(cache_key) is True:    # 确保每次都是全新加载的
        r.delete(cache_key)

    with open("../kdata/intention_answer.txt", encoding="utf-8", errors="ignore") as fo:
        for line in fo.readlines():
            arr = line.strip().split("\t")
            r.hset(cache_key, arr[0], arr[2])
            yuyiList.append(arr[0])
    print("cached finished")
    return set(yuyiList)

def getAnswerSet():
    answers = []
    with open("../kdata/intention_answer.txt", encoding="utf-8", errors="ignore") as fo:
        for line in fo.readlines():
            arr = line.strip().split("\t")
            answer_arr = arr[2].split("|")
            for a in answer_arr:
                answers.append(a)
    print("Get all answers successed")
    return set(answers)


'''
    通过语义获取回答，出现多个回答时随机返回一个
'''
def getAssignAnswer(field):
    try:
        result = r.hget(cache_key, field).decode("utf-8")
        result_List = result.split("|")
        return result.split("|")[random.randint(0, len(result_List) - 1)]
    except:
        return default_result


def main():
    cache()

if __name__ == '__main__':
    main()

