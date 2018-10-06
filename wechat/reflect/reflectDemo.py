# -*- coding: utf-8 -*-
# 反射

import threading

def sayHello():
    print("Hello")

def sayHi():
    print("Hi")

class MyThread(threading.Thread):
    def __init__(self, threadID):
        super(MyThread, self).__init__()
        self.threadID = threadID

    def run(self, funcName):
        pass

    def __del__(self):
        self.threadID = None

if __name__ == '__main__':
    pass