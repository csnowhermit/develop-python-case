#!/usr/bin/python26

'''
    tailF命令：解决tail -F /path/to/***.yyyyMMdd.log 场景下的日志实时获取问题
    已解决：循环过程中tail命令启动过多的情况
'''

import os
import time
import threading

oldThread = None
newThread = None
pidPath = "./pid.log"

class MyThread(threading.Thread):
    def __init__(self, threadID, fullPath):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.fullPath = fullPath

    def run(self):
        cmd = "tail -F " + str(self.fullPath)
        os.system(cmd)

    def __del__(self):
        self.fullPath = None

'''
    获取n秒后的时间，n为负数则为获取n秒前的时间
'''
def getSpecifyTime(n, fmt):
    now = time.time()
    before = now + n

    return time.strftime(fmt, time.localtime(before))


'''
    读取记录的当前时间段的PID
'''
def readPid(pidPath):
    pid = 0
    with open(pidPath) as f:
        pid = f.readline()

    f.close()
    return pid

def main():
    currTime = getSpecifyTime(-86400, "%Y%m%d_%H%M%S")

    fullPath = "/root/afa"+ str(currTime) +".log & echo $! > " + str(pidPath)
    try:
        oldThread = MyThread(threadID=str(fullPath).__hash__(),
                             fullPath=fullPath)
        oldThread.start()
    except:
        pass


if __name__ == '__main__':
    while True:
        main()
        time.sleep(86400)
        pid = readPid(pidPath)
        killCmd = "kill -9 " + str(pid)
        os.system(killCmd)
