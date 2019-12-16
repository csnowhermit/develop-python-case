# -*- coding:utf-8 -*-

import os
import time
import redis

'''
    Redis 发布订阅机制
'''

r = redis.Redis(host="192.168.117.134", port=6379, password="123456")
for i in range(10):
    r.publish(channel="channel.1", message="hello_" + str(i))

while True:
    ps = r.pubsub()
    s = ps.subscribe("channel.1")

    print(type(s), s)
    time.sleep(1)
