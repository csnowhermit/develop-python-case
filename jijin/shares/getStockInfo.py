# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import traceback
import re
import time
import sys
import logging
import traceback


'''
    从东方财富网获取股票链接，在百度股票中获取每只股票具体的数值
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


def getStockList(lst, stockURL):
    '''
    获取股票列表
    :param lst: 股票列表
    :param stockURL:
    :return:
    '''
    html = getHTMLText(stockURL)  # 获取一个页面
    soup = BeautifulSoup(html, 'html.parser')  # 使用BeautifulSoup解析
    a = soup.find_all('a')  # 找到所有的a标签
    for i in a:
        try:
            href = i.attrs['href']  # 找到a标签中的href属性
            lst.append(re.findall(r"[s][hz]\d{6}", href)[0])  # 在href中按照正则表达式查找，以列表的方式得到匹配上的子串
        except:
            continue  # 有些a标签没有href，所以直接跳过


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

            # 股票名称，编码
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
                logger.info("当前进度: {:.2f}%".format((writeCount + failCount) * 100 / len(lst)))
        except Exception as e:
            failCount = failCount + 1
            # print("except: " + str(count) + "\r当前进度: {:.2f}%".format(count * 100 / len(lst)), end="")
            logger.error("当前进度: {:.2f}%".format((writeCount + failCount) * 100 / len(lst)))
            logger.error(traceback.format_exc())
            continue
    logger.info("股票总数：%d, 成功爬取：%d, 失败：%d" % (len(lst), writeCount, failCount))


def main():
    stock_list_url = 'http://quote.eastmoney.com/stocklist.html'  # 东方财富网股票列表页面
    stock_info_url = 'https://gupiao.baidu.com/stock/'  # 百度股票
    output_file = 'D:/Downloads/FinancialData/shares/sharesData_' + time.strftime('%Y-%m-%d',
                                                                                  time.localtime(time.time())) + '.txt'
    # stockList = [ 'sh600705', 'sh600706', 'sh600707', 'sh600708', 'sh600709', 'sh600710', 'sh600711', 'sh600712', 'sh600713', 'sh600714', 'sh600715']
    stockList = []
    getStockList(stockList, stock_list_url)  # 获取股票列表
    print(stockList)
    getStockInfo(stockList, stock_info_url, output_file)


if __name__ == '__main__':
    main()
