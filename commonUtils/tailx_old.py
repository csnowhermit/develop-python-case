#!/usr/bin/python26
# encoding=utf-8

"""
    个人工具.afa3.tailx
    检测指定目录（包括子目录）中的新增文件，并输出新增的文件信息；
    不能输出已有文件的新增内容；
"""

import os
import sys
import time
import datetime
import threading
import traceback
import queue

# 扫描文件时间间隔
SCAN_FILE_INTERVAL = 1
# 扫描通知时间间隔
SCAN_NOTIFY_INTERVAL = 0.5
# 扫描目录修改时间限制（超过此时间则不进行扫描）
SCAN_DIR_MTIME_LIMIT = 1 * 60 * 60
# 新文件限制大小
NEWFILE_LIMIT_SIZE = 100 * 1024
# 日志根目录
LOG_ROOT_PATH = "/home/afa/afap/log"
# 日志通知队列
logNotifyQueue = queue.Queue()


def log(msg, *args):
    """

    :param msg:
    :param args:
    :return:
    """
    if args:
        msg %= args
    print(msg)


def showUsage():
    """

    :return:
    """
    fileName = os.path.basename(__file__)
    msg = "Usage: %s [sysId] " % fileName.split(".")[0]
    log(msg)


def getLogPath(sysId):
    """
    根据sysId得到日志目录
    :param sysId:
    :return:
    """
    today = datetime.datetime.now().strftime("%Y%m%d")
    logPath = os.path.join(LOG_ROOT_PATH, today)
    if sysId and (sysId != "afa"):
        logPath = os.path.join(logPath, sysId)
    if not os.path.exists(logPath):
        msg = "目录不存在：%s" % logPath
    if not os.path.isdir(logPath):
        msg = "路径非目录：%s" % logPath
        raise ValueError(msg)

    return logPath


def monitoring(logPathList):
    """
    监控目录
    :param logPathList:
    :return:
    """
    # thread：多线程处理，每个线程监控一个文件
    for (i, logPath) in enumerate(logPathList):
        logId = "%02d" % (i + 1)
        log("> %s %s", logId, logPath)
        thread = threading.Thread(target=scanLogPath, args=(logId, logPath))
        thread.daemon = True
        thread.start()

    log("\n\n")
    # read notify
    counter = 0
    while True:
        if logNotifyQueue.qsize() == 0:
            time.sleep(SCAN_NOTIFY_INTERVAL)
            continue
        logNotifyInfo = logNotifyQueue.get()
        try:
            counter += 1
            handleLogNotify(logNotifyInfo, counter)
        except Exception:
            msg = "处理中断：\n%s" % (traceback.format_exc())
            log(msg)


def handleLogNotify(logNotifyInfo, counter):
    """

    :param logNotifyInfo:
    :param counter:
    :return:
    """
    (logId, fullPath, pos, appendSize) = logNotifyInfo
    fileHashCode = "%04d" % abs(hash(fullPath))
    fileHashCode = fileHashCode[-4:]
    fileHashPrefix = "[%s%s%04d]" % (logId, fileHashCode, counter)
    # 标准日志文件的前缀
    now = datetime.datetime.now()
    stdLogPrefix = now.strftime("[%Y%m%d %H:")
    # 读文件
    with open(fullPath) as fp:
        fp.seek(pos)
        text = fp.read(appendSize)
        if text:
            log("%s%s", fileHashPrefix, fullPath)
            for line in text.splitlines():
                prefix = fileHashPrefix if line.startswith(stdLogPrefix) else ""
                log("%s%s", prefix, line)


def scanLogPath(logId, logPath):
    """

    :param logId:
    :param logPath:
    :return:
    """
    fileInfo = {}
    travelPath(logId, logPath, fileInfo, isFirstTime=True)
    while True:
        time.sleep(SCAN_FILE_INTERVAL)
        travelPath(logId, logPath, fileInfo, isFirstTime=True)


def travelPath(logId, path, fileInfo, isFirstTime):
    """

    :param logId:
    :param path:
    :param fileInfo:
    :param isFirstTime:
    :return:
    """
    if not os.path.exists(path):
        log("路径不存在：%s", path)
        return
    fileList = os.listdir(path)
    for fileName in fileList:
        fullPath = os.path.join(path, fileName)  # 文件的全路径
        fileInfo.setdefault(fullPath, {})  # 文件信息
        fi = fileInfo[fullPath]
        mtime = os.path.getmtime(fullPath)  # 修改时间
        size = os.path.getsize(fullPath)  # 文件大小

        # 如果是目录
        if os.path.isdir(fullPath):
            forwardPath = True
            if not fi:
                pass
            else:
                elapsed = int(time.time()) - int(mtime)
                if (mtime == fi["mtime"]) and (slice > SCAN_DIR_MTIME_LIMIT):
                    forwardPath = False

            if forwardPath:
                travelPath(logId, fullPath, fileInfo, isFirstTime)
        elif os.path.isfile(fullPath):  # 如果是文件
            if not isFirstTime:
                if not fi:
                    pos = 0
                    appendSize = size
                else:
                    pos = fi["size"]
                    appendSize = size - pos

                # 如果文件过大
                if appendSize > NEWFILE_LIMIT_SIZE:
                    pos = size - NEWFILE_LIMIT_SIZE
                    appendSize = NEWFILE_LIMIT_SIZE

                # 将文件放入队列
                if appendSize > 0:
                    logNotifyInfo = (logId, fullPath, pos, appendSize)
                    logNotifyQueue.put(logNotifyInfo)
                elif appendSize == 0:
                    pass
                else:
                    pass
                    # log("file was truncated: %s", fullPath)
        else:  # 其他情况
            log("skip: %s", fullPath)

        # 更新文件信息
        fi["mtime"] = mtime
        fi["size"] = size


def main():
    """

    :return:
    """
    if len(sys.argv) == 1:
        showUsage()
        return
    sysIdList = set(sys.argv[1:])
    logPathList = [getLogPath(sysId) for sysId in sysIdList]

    # 开始监控
    try:
        monitoring(logPathList)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()


"""
添加环境变量如下：
alias tailx='python tailx.py $*'
alias pygrep='find /home/afa/afap/application/afa /home/afa/afap/application/app -type f name "*.py" | xargs grep $@'

# The following three lines have been added by UDB DB2
if [ -f /home/afa/sqllib/db2profile ]; then
    . /home/afa/sqllib/db2profile
fi

"""