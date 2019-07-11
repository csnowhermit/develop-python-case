#!/usr/bin/python26
# encoding=utf-8

import requests
from bs4 import BeautifulSoup
import re
import traceback
from jijin.shares.GrabData_beta1.Logger import *

'''
    爬取股票信息工具类
'''

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
    '''
        爬取股票的具体信息
    :param lst: 股票列表
    :param stockURL: 股票信息的url
    :param fpath: 内容写入文件
    :return: 无返回值
    '''
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
