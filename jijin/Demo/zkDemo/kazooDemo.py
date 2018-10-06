#!/usr/bin/python26
#encoding=utf-8

from kazoo.client import KazooClient

zk = KazooClient(hosts='localhost:2181')  # 连接zk集群
zk.start()

# zk.create('/zookeeper/testDir', bytes('test', encoding='utf-8'))

print(zk.get('/zookeeper'))
print(zk.get('/zookeeper/testDir'))