#!/usr/bin/python26
# encoding=utf-8

'''
    zookeeper校验仪
'''

import time
from kazoo.client import KazooClient
from kazoo.recipe.watchers import ChildrenWatch


class ValidatorDetectot:
    def __init__(self, path):
        self.zk = KazooClient(hosts='localhost:2181')  # 连接zk集群
        self.validator_children_watcher = ChildrenWatch(client=self.zk, path=path,
                                                        func=self.validator_watcher_fun)  #
        self.zk.start()

    def validator_watcher_fun(self, children):
        print("The children now are: " + str(children))

    def create_node(self):
        self.zk.create('mproxy/validators/validator', b'validatir_huabei_1', ephemeral=True, sequence=True,
                       makepath=True)

    def __del__(self):
        self.zk.close()


def main():
    path = '/mproxy/validators'
    detector = ValidatorDetectot(path=path)
    detector.create_node()
    time.sleep(1)


if __name__ == '__main__':
    main()
