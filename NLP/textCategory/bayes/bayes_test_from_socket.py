# -*- coding:utf-8 -*-

import os
import time
import random
import socket
import configparser
from sklearn.externals import joblib
import _thread as thread
from kafka import KafkaConsumer
from NLP.textCategory.bayes.bayes_train import get_dataset, get_words, split_train_and_test_set, multinamialNB_save_path, bernousNB_save_path, isChat
from NLP.Logger import *

'''
    从文件读取模型并进行分类，打开socket，接收消息
'''

log = Logger('D:/data/bayes_mq.log', level='info')

# test_data = get_dataset()
# train_set_tmp, train_label_tmp, test_set, test_label = split_train_and_test_set(test_data, 0.0)

# '''
#     分离出来
# '''
# def divideTestSet(test_set):
#     for tset in test_set:
#         print(tset)
#         # pass

AnswerDict = []
intentionList = []

def loadAnswers():
    with open("../kdata/intention_answer.txt", encoding="utf-8", errors="ignore") as fo:
        for line in fo.readlines():
            arr = line.strip().split("\t")
            AnswerDict[arr[0]] = arr[2]
            intentionList.append(arr[0])
    print("load answers finished")

def getAnswer(intention):
    result_list = AnswerDict[intention].split("|")
    return result_list[random.randint(0, len(result_list) - 1)]

'''
    获取最新的模型
'''
def get_newest_model(model_path):
    model_full_path = os.path.join(os.path.dirname(__file__), model_path)
    model_full_path = model_full_path.replace('\\', '').replace('.', '')

    if os.path.exists(model_full_path):
        # 按文件最后修改时间排序，reverse=True表示降序排序
        filelist = sorted(os.listdir(model_full_path), key=lambda x: os.path.getctime(os.path.join(model_full_path, x)), reverse=True)
        log.logger.info(("Use Model: %s" % (os.path.join(model_full_path, filelist[0]))))
        return os.path.join(model_full_path, filelist[0])
    else:
        log.logger("Model path is not exists")

'''
    读取配置文件，获取打开SocketServer的ip和端口
'''
def getConfig():
    cf = configparser.ConfigParser()
    cf.read("../kdata/config.conf")
    host = str(cf.get("sserver", "host"))
    port = int(cf.get("sserver", "port"))
    return host, port

'''
    测试多项式分类器
'''
def test_bayes(model_file):
    clf = joblib.load(model_file)
    # loadAnswers()    # 加载 意图-答案 表

    sev = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP连接
    HOST, PORT = getConfig()
    sev.bind((HOST, PORT))
    sev.listen()
    print("语义识别端已启动。。。")

    conn, addr = sev.accept()
    log.logger.info((conn, addr))

    while True:
        sentences = bytes.decode(conn.recv(4096), encoding='utf-8')

        word_list = []
        new_sentences = get_words(sentences)
        if isChat(new_sentences) is False:  # 如果不是闲聊
            word_list.append(new_sentences)
            predict = clf.predict(word_list)
            for left in predict:
                if left == "坐车":
                    left = "坐高铁"
                # answer = getAnswer(left)
                # thread.start_new_thread(send_msg, ())    # 新开一个线程，通知前端
                print(left, "-->", word_list, "-->", sentences)
                log.logger.info((left, "-->", word_list, "-->", sentences))
        else:
            print("咨询类", "-->", sentences)  # 闲聊场景，将原话传给闲聊机器人
            log.logger.info(("咨询类", "-->", sentences))


def main():
    # test_bayes(get_newest_model(multinamialNB_save_path))
    test_bayes(get_newest_model(bernousNB_save_path))
    # print(get_newest_model(multinamialNB_save_path))
    # print(get_newest_model(bernousNB_save_path))
    # divideTestSet(test_set)

    # model_file = "D:/workspace/Pycharm_Projects/develop-python-case/NLP/textCategory/bayes/model/bernousNB/bernousNB_1576579523_9512195121951219_0_0.m"
    # test_bayes(model_file)

if __name__ == '__main__':
    main()