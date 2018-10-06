#!/usr/bin/python26

import time

def writeData():
    count = 0
    age = 20

    while (True):
        s = str(count) + ", zhangsan-" + str(count) + ", " + str(age)
        print(s)
#        f = open("/root/afa.log", 'a', encoding='utf-8')
        f = open("/root/afa"+ time.strftime("%Y%m%d_%H%M%S", time.localtime()) +".log", 'a')
        f.write(str(s) + '\n')
        count += 1
        age += 1
        time.sleep(1)

if __name__ == '__main__':
    writeData()
