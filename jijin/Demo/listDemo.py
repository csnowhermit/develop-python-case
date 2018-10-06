#!/usr/bin/python26
# encoding=utf-8

import threading
from pandas.core.frame import DataFrame
from Utils.Logger import logger, logPath

# shList = list(range(1, 100, 2))
# print(shList)
# df = DataFrame(shList)
# print(type(df))
# # print(df)
#
# df["line1"] = df[0].map(lambda x: x%2 == 0)
# df["line2"] = df[0].map(lambda x: x%2 == 1)
# print(df)

shList = ['sh600705', 'sh600706', 'sh600707', 'sh600708', 'sh600709',
          'sh600710', 'sh600711', 'sh600712', 'sh600713', 'sh600714',
          'sh600715']
szList = ['sz600705', 'sz600706', 'sz600707', 'sz600708', 'sz600709',
          'sz600710', 'sz600711', 'sz600712', 'sz600713', 'sz600714']

def splitList(lst, n):
    retDict = {}
    for i in range(0, n):
        retDict.update({i: []})

    for j in range(len(lst)):
        retLst = retDict[j%n];

        retLst.append(lst[j])

        retDict.update({j%n: retLst})
    return retDict


# lst = list(range(1, 32))
# print(lst)
# print(splitList(lst, 4))

shDict = splitList(shList, 4)
szDict = splitList(szList, 4)

print(shDict)
print(szDict)

print(shDict.keys())
print(szDict.keys())

logPath="./Demo.log"


# 输出不同级别的log
logger.debug('this is debug info')
logger.info('this is information')
logger.warn('this is warning message')
logger.error('this is error message')
logger.fatal('this is fatal message, it is same as logger.critical')
logger.critical('this is critical message')






