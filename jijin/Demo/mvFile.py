#!/usr/bin/python26
#encoding=utf-8

import os
import time

def mvFileData():
    while (True):
        cmd = "mv /root/afa.log /root/flumeSpool/afa-" + str(time.time()) + ".log"
        os.system(cmd)
        time.sleep(5)
        print(cmd)

if __name__ == '__main__':
    mvFileData()