#!/usr/bin/python26
# encoding=utf-8

'''
    多线程Demo
'''

import threading
import time


class MyThread(threading.Thread):
    '''
        继承父类threading.Thread
    '''

    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("start thread %s" % self.name)
        print_time(self.name, self.counter, 5)
        print("exit thread %s" % self.name)


def print_time(threadName, delay, counter):
    while counter:
        time.sleep(delay)
        print("%s: %s" % (threadName, counter))
        counter -= 1


def main():
    mt1 = MyThread("001", "thread_A", 5)
    mt2 = MyThread("002", "thread_B", 6)

    mt1.start()
    mt2.start()


if __name__ == '__main__':
    main()
