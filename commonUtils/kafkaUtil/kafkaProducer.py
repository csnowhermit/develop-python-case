# -*- coding:utf-8 -*-

from kafka import KafkaProducer

'''
    python kafka包：python操作kafka，生产者
'''

broker_list = "192.168.117.101:9092,192.168.117.102:9092,192.168.117.103:9092"
topic = "daotai"

producer = KafkaProducer(bootstrap_servers=broker_list, compression_type='gzip')

while True:
    print(">", end="")
    msg = input()

    bmsg = bytes(str(msg).encode('utf-8'))
    producer.send(topic=topic, value=bmsg)
