# -*- coding:utf-8 -*-

import os
import time
from sklearn.externals import joblib
from NLP.textCategory.bayes.bayes_train import get_dataset, get_words, split_train_and_test_set, multinamialNB_save_path, bernousNB_save_path, isChat
from kafka import KafkaConsumer
from NLP.Logger import *

'''
    从文件读取模型并进行分类，从消息队列读取数据
'''

bootstrap_server = "192.168.117.101:9092,192.168.117.102:9092,192.168.117.103:9092"
topic = "daotai"

log = Logger('D:/data/bayes_mq.log', level='info')

consumer = KafkaConsumer(topic, auto_offset_reset='latest', bootstrap_servers=bootstrap_server)
# print(consumer)

# test_data = get_dataset()
# train_set_tmp, train_label_tmp, test_set, test_label = split_train_and_test_set(test_data, 0.0)

'''
    分离出来
'''
def divideTestSet(test_set):
    for tset in test_set:
        print(tset)
        # pass

'''
    获取最新的模型
'''
def get_newest_model(model_path):
    if os.path.exists(model_path):
        # 按文件最后修改时间排序，reverse=True表示降序排序
        filelist = sorted(os.listdir(model_path), key=lambda x: os.path.getctime(os.path.join(model_path, x)), reverse=True)
        return os.path.join(model_path, filelist[0])


'''
    测试多项式分类器
'''
def test_bayes(model_file):
    clf = joblib.load(model_file)
    while True:
        msg = consumer.poll(timeout_ms=1000, max_records=3)  # 每次拉取
        for s in msg.values():
            for k in s:
                # print(k.offset, k.value)
                # print(type(k.value), k.value.decode("utf-8"))
                word_list = []
                sentences = k.value.decode("utf-8")
                new_sentences = get_words(sentences)
                if isChat(new_sentences) is False:    # 如果不是闲聊
                    word_list.append(new_sentences)
                    predict = clf.predict(word_list)
                    for left in predict:
                        if left == "坐车":
                            left = "坐高铁"
                        print(left, "-->", word_list, "-->", sentences)
                        log.logger.info((left, "-->", word_list, "-->", sentences))
                else:
                    print("咨询类", "-->", sentences)    # 闲聊场景，将原话传给闲聊机器人
                    log.logger.info(("咨询类", "-->", sentences))
        time.sleep(0.5)    # 隔0.5s再次拉取


def main():
    # test_bayes(get_newest_model(multinamialNB_save_path))
    test_bayes(get_newest_model(bernousNB_save_path))
    # print(get_newest_model(multinamialNB_save_path))
    # print(get_newest_model(bernousNB_save_path))
    # divideTestSet(test_set)

if __name__ == '__main__':
    main()