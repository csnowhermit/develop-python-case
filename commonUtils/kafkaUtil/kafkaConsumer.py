# -*- coding:utf-8 -*-

import time
from kafka import KafkaConsumer

'''
    python kafka包：python操作kafka，消费者
'''

bootstrap_server = "192.168.117.101:9092,192.168.117.102:9092,192.168.117.103:9092"
topic = "daotai"

# auto_offset_reset='earliest'，最少消费一次
consumer = KafkaConsumer(topic, auto_offset_reset='earliest', bootstrap_servers=bootstrap_server)
print(consumer)
# for msg in consumer:
#     print(str(msg).encode("UTF-8"))
while True:
    msg = consumer.poll(timeout_ms=1000, max_records=3)    # 每次拉取
    for s in msg.values():
        for k in s:
            # print(k.offset, k.value)
            print(type(k.value), k.value.decode("utf-8"))
    time.sleep(0.5)


