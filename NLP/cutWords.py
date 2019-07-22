import os
import sys
import time
import traceback
import jieba
from jieba import analyse
from collections import Counter

'''
    舆情数据：中文分词
'''

jieba.load_userdict("./data/hmm.txt")  # 过滤掉不拆分的词
contents = []
with open("./data/2018.6-2019.5舆情数据.txt", encoding='UTF-8') as f:
    line = f.readline()
    while line:
        contents.append(line)
        line = f.readline()

stop_words = []  # 停用词
with open("./data/stop_words.txt", encoding="UTF-8") as fo:
    for line in fo.readlines():
        stop_words.append(line.strip('\n'))


def cut():
    count_freq = {}
    for line in contents:
        words = jieba.cut(str(line), cut_all=True)    # 全模式切分
        words = list(words)
        print("/ ".join(words))

    # for i in range(len(words)):
    #     try:
    #         int(words[i])
    #         float(words[i])
    #         bool(words[i])
    #     except ValueError:
    #         if words[i] in stationEntryDict:    # 如果第i个词是站名，则匹配第i+1个词
    #             entrys = getEntryByStation(words[i])
    #             if i == len(words):
    #                 continue
    #             for j in range(len(words)):  # 匹配全词
    #                 if words[j] is not None and words[j] in entrys:
    #                     # print(words[i], words[j])
    #                     count_freq[str(words[i]) + "," + str(words[j])] = count_freq.get(str(words[i]) + "," + str(words[j]), 0) + 1
    return count_freq



def main():
    count_freq = cut()
    for c in count_freq:
        print(c, count_freq[c])

if __name__ == '__main__':
    main()
