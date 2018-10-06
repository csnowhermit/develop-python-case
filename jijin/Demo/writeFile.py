#!/usr/bin/python26
#encoding=utf-8

import time

def writeData():
    count = 0
    age = 20

    while (True):
        s = str(count) + ", zhangsan-" + str(count) + ", " + str(age)
        print(s)
        f = open("d:/afa.log", 'a', encoding='utf-8')
        f.write(str(s) + '\n')
        count += 1
        age += 1
        time.sleep(1)

if __name__ == '__main__':
    writeData()