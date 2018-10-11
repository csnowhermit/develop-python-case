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
import getpass
import datetime
import threading
import traceback
import queue

# 扫描文件时间间隔
SCAN_FILE_INTERVAL = 2
# 扫描通知时间间隔
SCAN_NOTIFY_INTERVAL = 0.5
# 扫描目录修改时间限制（超过此事件则不进行扫描）
SCAN_DIR_MTIME_LIMIT = 0  # 1*60*60
# 新文件限制大小
NEWFILE_LIMIT_SIZE = 100 * 1024
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
    msg = "Usage: %s [user=afa/mid] [sysId]" % fileName.split(".")[0]
    log(msg)


def getLogPath(sysId, userName):
    """
    根据sysId和用户名获取日志目录路径
    :param sysId:
    :param userName:
    :return:
    """
    today = datetime.datetime.now().strftime("%Y%m%d")
    homePath = "/home/%s" % (userName,)
    logRootPath = os.path.join(homePath, "afap/log")
    logPath = os.path.join(logRootPath, today)
    if sysId == "platform":
        logPath = os.path.join(homePath, "log")
    elif sysId and (sysId != "afa"):
        logPath = os.path.join(logPath, sysId)

    if not os.path.exists(logPath):
        try:
            os.makedirs(logPath)
        except:
            msg = "创建目录失败，等待目录自动创建：%s" % logPath
            log(msg)
            while not os.path.exists(logPath):
                time.sleep(SCAN_FILE_INTERVAL)

    if not os.path.isdir(logPath):
        msg = "路径非目录：%s" % logPath
        raise ValueError(msg)

    return logPath


def monitoring(logPathList):
    """

    :param logPathList:
    :return:
    """
    for (i, logPath) in enumerate(logPathList):
        logId = "%02d" % (i + 1)
        log("> %s %s", logId, logPath)
        thread = threading.Thread(target=scanLogPath, args=(logId, logPath))
        thread.daemon = True
        thread.start()

    log("\n\n")
    counter = 0
    enterTime = datetime.datetime.now()
    while True:
        now = datetime.datetime.now()
        if enterTime.day != now.day:
            log("[main thread]date has changed.")
            break

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

    # 文件前缀
    fileHashCode = "%04d" % abs(hash(fullPath))
    fileHashCode = fileHashCode[-4:]
    fileHashPrefix = "[%s%s%04d]" % (logId, fileHashCode, counter)

    # 标准日志前缀
    now = datetime.datetime.now()
    stdLogPrefix = now.strftime("[%Y/%m/%d %H:")

    # 开始读文件
    with open(fullPath) as fp:
        fp.seek(pos)  # 定位文件指针到上一步更新点
        text = fp.read(appendSize)  # 读取日志文件新增内容
        if text:
            log("%s%s", fileHashPrefix, fullPath)  # 先打印日志文件名，再逐行打印日志信息
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
    enterTime = datetime.datetime.now()
    while True:
        now = datetime.datetime.now()
        if enterTime.day != now.day:
            log("[sub thread]date has changed.")
            break
        time.sleep(SCAN_FILE_INTERVAL)
        logNotifyInfoList = travelPath(logId, logPath, fileInfo, isFirstTime=True)
        if logNotifyInfoList:
            def cmpFunc(x, y):
                xPath = x[1]
                yPath = y[1]
                xCreateTime = os.path.getctime(xPath)
                yCreateTime = os.path.getctime(yPath)

                ret = __cmp__(xCreateTime, yCreateTime)
                if ret != 0:
                    return ret

                ret = __cmp__(len(xPath, yPath))
                if ret != 0:
                    return ret

                return __cmp__(xPath, yPath)

            logNotifyInfoList = sorted(logNotifyInfoList, cmp=cmpFunc)
            for logNotifyInfo in logNotifyInfoList:
                log("%s - %s - %s", os.path.getctime(logNotifyInfo[1]), os.stat(logNotifyInfo[1]), logNotifyInfo[1])
                logNotifyQueue.put(logNotifyInfoList)


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
    logNotifyInfoList = []
    fileList = os.listdir(path)
    for fileName in fileList:
        fullPath = os.path.join(path, fileName)  # 获取文件的全路径
        fileInfo.setdefault(fullPath, {})
        fi = fileInfo[fullPath]
        mtime = os.path.getmtime(fullPath)  # 修改时间
        size = os.path.getsize(fullPath)  # 文件大小

        if os.path.isdir(fullPath):  # 如果是目录
            forwardPath = True
            if not fi:
                pass
            else:
                elapsed = int(time.time()) - int(mtime)
                if SCAN_DIR_MTIME_LIMIT and (mtime == fi["mtime"]) and (elapsed > SCAN_DIR_MTIME_LIMIT):
                    forwardPath = False
            if forwardPath:
                logNotifyInfoList += travelPath(logId, fullPath, fileInfo, isFirstTime)
        elif os.path.isfile(fullPath):  # 如果是文件
            if not isFirstTime:
                if not fi:  # 如果是新文件
                    pos = 0
                    appendSize = size
                else:  # 如果是旧文件
                    pos = fi["size"]
                    appendSize = size - pos  # 总大小-上次读到的位置= 文件新增的大小

                if appendSize > NEWFILE_LIMIT_SIZE:  # 如果文件过大
                    pos = size - NEWFILE_LIMIT_SIZE
                    appendSize = NEWFILE_LIMIT_SIZE
                elif appendSize > 0:  # 如果有增长，则加入到日志提醒列表中
                    logNotifyInfo = (logId, fullPath, pos, appendSize)
                    logNotifyInfoList.append(logNotifyInfo)
                elif appendSize == 0:  # 如果没增长，直接pass掉
                    pass
                else:  # 否则（如果增长为负），说明文件被truncate掉
                    pass
                    log("file was truncated: %s", fullPath)
        else:  # 如果既非目录也非文件
            log("skip %s", fullPath)

        # 更新文件信息
        fi["mtime"] = mtime  # 更新文件修改时间
        fi["size"] = size  # 更新文件大小
    return logNotifyInfoList


def readSysIdList():
    """

    :return:
    """
    fileName = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sysid.list")
    if not os.path.exists(fileName):
        return {}

    sysIdMap = {}
    with open(fileName) as fp:
        for line in fp:
            line = line.strip()
            if not line:
                continue
            items = line.split(None, 2)
            if len(items) == 1:
                continue
            (sysName, sysId) = items
            sysIdMap[sysName] = sysId.split("_")
    return sysIdMap


def getSysIdList(sysIdList):
    """

    :param sysIdList:
    :return:
    """
    sysIdMap = readSysIdList()

    def getStsIdListFromName(name):
        """

        :param name:
        :return:
        """
        if "/" in name:
            (name, path) = name.split("/", 1)
        else:
            path = ""
        sysIdList = sysIdMap.get(name, [name])
        if path:
            sysIdList = [("%s/%s" % (sysId, path)) for sysId in sysIdList]
        return sysIdList

    sysIdList2 = []
    for sysId in set(sysIdList):
        _sysIdList = getStsIdListFromName(sysId)
        sysIdList += _sysIdList

    return sysIdList2


def main():
    argv = sys.argv[1:]
    if not argv:
        showUsage()
        return
    userName = getpass.getuser()  # 得到当前用户的用户名
    argsDict = {}
    sysIdList = []
    for item in argv:
        if "=" in item:
            (name, value) = item.split("=", 1)
            argsDict[name] = value
        else:
            sysIdList.append(item)
    if not sysIdList:
        showUsage()
        return

    if "user" in argsDict:
        userName = argsDict.pop("user")

    if argsDict:
        raise ValueError(argsDict)

    try:
        sysIdList = getSysIdList(sysIdList)
        logPathList = [getLogPath(sysId, userName) for sysId in sysIdList]
        monitoring(logPathList)  # 开始监控
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
