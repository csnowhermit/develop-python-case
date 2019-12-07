# -*- coding:utf-8 -*-

import time
from kafka import KafkaProducer
from NLP.textCategory.bayes.bayes_train import origin_sentences_file

'''
    贝叶斯分类器批量识别测试：生产者，从“原始例句.txt”文件中读取，走kafka流程到bayes_test_mq
'''

broker_list = "192.168.117.101:9092,192.168.117.102:9092,192.168.117.103:9092"
topic = "daotai"

producer = KafkaProducer(bootstrap_servers=broker_list, compression_type='gzip')

'''
    读取原始例句
'''
def read_corpus():
    data = []
    with open(origin_sentences_file, encoding="utf-8", errors="ignore") as fo:
        for line in fo.readlines():
            data.append(line.strip().split("\t")[0])
            # print(line.strip().split("\t")[1], '-->', line.strip().split("\t")[0])
    return data

def send(data):
    for d in data:
        print(">", d)
        bmsg = bytes(str(d).encode('utf-8'))
        producer.send(topic=topic, value=bmsg)
        time.sleep(1)

def main():
    data = read_corpus()
    send(data)

if __name__ == '__main__':
    main()

