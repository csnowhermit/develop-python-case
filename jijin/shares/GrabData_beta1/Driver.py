#!/usr/bin/python26
# encoding=utf-8

import threading
from shares.GrabData_beta1.GrabStockInfo import *

'''
    从东方财富网获取股票链接，在百度股票中获取每只股票具体的数值
    @version: 3.0
    @Note: 
    1、功能拆分，形成专门的Logger和爬取功能
    2、
'''


class MyThread(threading.Thread):
    '''
        继承父类threading.Thread
    '''

    def __init__(self, threadID, name, key, stockList, stock_info_url, fpath):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.key = key
        self.stockList = stockList
        self.stock_info_url = stock_info_url
        self.fpath = fpath

    def run(self):
        '''
            把要执行的代码写到run函数里面 线程在start()后会直接运行run函数
        :return:
        '''
        getStockInfo(self.stockList, self.stock_info_url, self.fpath)

    def __del__(self):
        '''
        线程销毁，所有变量清空
        :return:
        '''
        logger.info("线程 " + str(self.name) + "(ID" + str(self.threadID) + ") 已被销毁")
        self.threadID = None
        self.name = None
        self.key = None
        self.stockList = None
        self.stock_info_url = None
        self.fpath = None


def main():
    stock_list_url = 'http://quote.eastmoney.com/stocklist.html'  # 东方财富网股票列表页面
    stock_info_url = 'https://gupiao.baidu.com/stock/'  # 百度股票
    # output_file = 'D:/Downloads/FinancialData/shares/sharesData_' + time.strftime('%Y-%m-%d',
    #                                                                               time.localtime(time.time())) + '.txt'

    (shList, szList) = getStockList(stock_list_url)  # 获取股票列表

    # shList = ['sh600705', 'sh600706', 'sh600707', 'sh600708', 'sh600709', 'sh600710', 'sh600711', 'sh600712',
    #           'sh600713', 'sh600714', 'sh600715']

    logger.info("本次爬取列表：")
    logger.info("沪指：" + str(shList))
    logger.info("深指：" + str(szList))

    n = 3  # 分三等份，爬取
    shSplitDict = splitList(shList, n)
    szSplitDict = splitList(szList, n)

    logger.info("本次沪指分 " + str(n) + " 等份爬取，详情：" + str(shSplitDict))
    logger.info("本次深指分 " + str(n) + " 等份爬取，详情：" + str(szSplitDict))

    # 启动沪指数据爬取
    for key in shSplitDict.keys():
        output_file = 'D:/Downloads/FinancialData/shares/sh/shSharesData_' + time.strftime('%Y-%m-%d', time.localtime(
            time.time())) + "_" + str(key) + '.txt'
        print(output_file)
        MyThread(threadID=str(key).__hash__(),
                 name="sh_" + str(key),
                 key=key,
                 stockList=shSplitDict[key],
                 stock_info_url=stock_info_url,
                 fpath=output_file).start()  # 启动线程

    # 启动深指数据爬取
    for key in szSplitDict.keys():
        output_file = 'D:/Downloads/FinancialData/shares/sz/szSharesData_' + time.strftime('%Y-%m-%d', time.localtime(
            time.time())) + "_" + str(key) + '.txt'
        print(output_file)
        MyThread(threadID=str(key).__hash__(),
                 name="sz_" + str(key),
                 key=key,
                 stockList=szSplitDict[key],
                 stock_info_url=stock_info_url,
                 fpath=output_file).start()  # 启动线程


if __name__ == '__main__':
    main()
