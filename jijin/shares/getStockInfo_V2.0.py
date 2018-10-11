# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import time
import sys
import logging
import traceback
import threading

'''
    从东方财富网获取股票链接，在百度股票中获取每只股票具体的数值
    @version: 2.0
    @Note: 
    1、改进日志机制，每条记录的成功失败情况都有据可查
    2、沪指和深指分开爬取及存储，多线程爬取
'''

# 获取logger实例，如果参数为空则返回root logger
logger = logging.getLogger("Logger")

# 指定logger输出格式
formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')

# 文件日志
file_handler = logging.FileHandler(
    "log/getStockInfo_" + time.strftime('%Y-%m-%d', time.localtime(time.time())) + ".log")
file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式

# 控制台日志
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter  # 也可以直接给formatter赋值

# 为logger添加的日志处理器
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 指定日志的最低输出级别，默认为WARN级别
logger.setLevel(logging.INFO)


def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


def getStockList(stockURL):
    '''
    获取股票列表
    :param lst: 股票列表
    :param stockURL:
    :return:
    '''
    html = getHTMLText(stockURL)  # 获取一个页面
    soup = BeautifulSoup(html, 'html.parser')  # 使用BeautifulSoup解析
    a = soup.find_all('a')  # 找到所有的a标签
    shList = []
    szList = []
    for i in a:
        try:
            href = i.attrs['href']  # 找到a标签中的href属性
            # lst.append(re.findall(r"[s][hz]\d{6}", href)[0])  # 在href中按照正则表达式查找，以列表的方式得到匹配上的子串
            stockName = re.findall(r"[s][hz]\d{6}", href)[0]
            if stockName.startswith("sh"):
                shList.append(stockName)
            elif stockName.startswith("sz"):
                szList.append(stockName)
            else:
                continue

                # if re.findall(r"[s][h]\d{6}", href)[0]:
                #     shList.append(re.findall(r"[s][h]\d{6}", href)[0])
                # elif re.findall(r"[s][z]\d{6}", href)[0]:
                #     szList.append(re.findall(r"[s][z]\d{6}", href)[0])
                # else:
                #     continue

        except:
            continue  # 有些a标签没有href，所以直接跳过
    return (shList, szList)


def splitList(lst, n):
    '''
    将list均等拆分n等份
    :param lst: 待拆分数组
    :param n: n等份
    :return: 以Dict的方式返回拆分后结果
    '''
    retDict = {}
    for i in range(0, n):
        retDict.update({i: []})

    for j in range(len(lst)):
        retLst = retDict[j % n];
        retLst.append(lst[j])

        retDict.update({j % n: retLst})
    return retDict


def getStockInfo(lst, stockURL, fpath):
    failCount = 0
    writeCount = 0
    for stock in lst:
        url = stockURL + stock + ".html"
        html = getHTMLText(url)
        try:
            if html == "":
                continue
            infoDict = {}  # 每只股票的信息列表
            soup = BeautifulSoup(html, 'html.parser')
            stockInfo = soup.find('div', attrs={'class': 'stock-bets'})

            # 股票名称，代码
            stockName = stockInfo.find_all(attrs={'class': 'bets-name'})[0]
            infoDict.update({'股票名称': stockName.text.split()[0]})
            infoDict.update({'股票代码': stockName.text.split()[1]})

            # 当天时间
            currDate = stockInfo.find_all(attrs={'class': 'state f-up'})[0]
            infoDict.update({'时间': currDate.text.split()[1:]})

            # 收盘价，涨跌额，涨跌幅等基本信息
            stockBasicInfo = stockInfo.find_all(attrs={'class': 'price s-up '})[0]
            infoDict.update({'收盘价': stockBasicInfo.text.split()[0]})
            infoDict.update({'涨跌额': stockBasicInfo.text.split()[1]})
            infoDict.update({'涨跌幅': stockBasicInfo.text.split()[2]})
            # logger.info(infoDict)

            # 得到详细信息
            keyList = stockInfo.find_all('dt')  # 得到详细信息的键
            valueList = stockInfo.find_all('dd')  # 得到详细信息的值
            if ((len(keyList) == 0) or (len(valueList) == 0)):  # 如果详细信息为空，则跳过
                continue

            for i in range(len(keyList)):
                key = keyList[i].text
                val = valueList[i].text
                infoDict[key] = val

            with open(fpath, 'a', encoding='utf-8') as f:
                f.write(str(infoDict) + '\n')
                writeCount = writeCount + 1
                # print("\r当前进度: {:.2f}%".format(count * 100 / len(lst)), end="")
                logger.info(
                    "当前爬取：" + infoDict["股票代码"] + " 进度: {:.2f}%".format((writeCount + failCount) * 100 / len(lst)))
        except Exception as e:
            failCount = failCount + 1
            # print("except: " + str(count) + "\r当前进度: {:.2f}%".format(count * 100 / len(lst)), end="")
            try:
                sharesCode = infoDict["股票代码"]
            except:
                sharesCode = ""
            logger.error("当前爬取：" + sharesCode + " 进度: {:.2f}%".format((writeCount + failCount) * 100 / len(lst)))
            logger.error(traceback.format_exc())
            continue
    logger.info("股票总数：%d, 成功爬取：%d, 失败：%d" % (len(lst), writeCount, failCount))


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


        # getStockInfo(stockList, stock_info_url, output_file)


if __name__ == '__main__':
    main()
