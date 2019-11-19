# -*- coding:utf-8 -*-

import os
import time
import random
import jieba
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer, HashingVectorizer, CountVectorizer
from sklearn import metrics
from sklearn.naive_bayes import BernoulliNB
from sklearn.externals import joblib

'''
    贝叶斯：文本分类
'''

atomic_file = "../atomic.txt"                   # 不可切分词
origin_sentences_file = "../原始例句.txt"       # 原始例句
keywords_intention_file = "../keywords_intention.txt"      # 整理后的关键字-意图
stopwords_file = "../stopwords.txt"            # 停用词
zhuhai_station_file = "../zhuhai.txt"          # 珠海方向车站
others_station_file = "../others.txt"          # 其他方向车站

multinamialNB_save_path = "./model/multinamialNB/"    # 多项式分类器模型保存路径
bernousNB_save_path = "./model/bernousNB/"            # 伯努利分类器模型保存路径

jieba.load_userdict(atomic_file)    # 不可切分词


'''
    加载数据集：最原始文本集
'''
def get_dataset():
    data = []
    with open(origin_sentences_file, encoding="utf-8", errors="ignore") as fo:
        for line in fo.readlines():
            arr = line.strip().split("\t")
            data.append((get_words(arr[0]), arr[1]))
    random.shuffle(data)    # 随机打乱
    return data

'''
    加载数据集：分离出的关键字对应材料
'''
def load_dataset():
    data = []
    with open(keywords_intention_file, encoding="utf-8", errors="ignore") as fo:
        for line in fo.readlines():
            arr = line.strip().split("\t")
            data.append((arr[0].replace(",", " "), arr[1]))
    random.shuffle(data)    # 随机打乱
    return data


def getWordList(filepath):
    keySet = []
    with open(filepath, encoding="utf-8", errors="ignore") as fo:
        for line in fo.readlines():
            keySet.append(line.strip())
    return set(keySet)

zhuhai_c = getWordList(zhuhai_station_file)
others = getWordList(others_station_file)

'''
    获取“关键字-意图”文件中所有关键字
'''
def getAllKeywords(zhuhai_c, others):
    keywords = []
    with open(keywords_intention_file, encoding="utf-8") as fo:
        lines = fo.readlines()
        for line in lines:
            arr = line.strip().split("\t")
            for k in arr[0].strip().split(","):
                if k in zhuhai_c:
                    keywords.append("地名1")
                elif k in others:
                    keywords.append("地名2")
                else:
                    keywords.append(k)
    return set(keywords)

keywords = getAllKeywords(zhuhai_c, others)
stopwords = getWordList(stopwords_file)


'''
    获取文档中的关键词
'''
def get_words(line):
    s = ""
    arr = jieba.cut(line)
    for a in arr:
        if a in zhuhai_c:
            a = "地名1"
        elif a in others:
            a = "地名2"
        elif a in keywords:
            a = a
        else:
            a = ""
        if len(a) > 0:
            s = s + a + " "
    return s.strip(" ")


'''
    划分训练集和测试集
'''
def split_train_and_test_set(data, rate):
    filesize = int(rate * len(data))    # 训练集:测试集=7:3

    train_set = [each[0] for each in data[:filesize]]
    train_label = [each[1] for each in data[:filesize]]

    test_set = [each[0] for each in data[filesize:]]
    test_label = [each[1] for each in data[filesize:]]
    return train_set, train_label, test_set, test_label

'''
    多项式分类器
'''
def multinamialNB(train_set, train_label, test_set, test_label):
    nbc = Pipeline([
        ('vect', TfidfVectorizer(

        )),
        ('clf', MultinomialNB(alpha=1.0))
    ])

    nbc.fit(train_set, train_label)    # 训练多项式分类器
    predict = nbc.predict(test_set)    # 测试分类器分类效果
    count = 0
    for left, right, tset in zip(predict, test_label, test_set):
        print(left, "-->", right, "-->", tset)
        if left == right:
            count += 1
    print("多项式分类器准确率：", count/len(test_label))
    joblib.dump(nbc, multinamialNB_save_path + "multinamialNB_" + str(int(time.time())) + ".m")

'''
    伯努利分类器
'''
def bernousNB(train_set, train_label, test_set, test_label):
    nbc_1 = Pipeline([
        ('vect', TfidfVectorizer(

        )),
        ('clf', BernoulliNB(alpha=0.1))
    ])
    nbc_1.fit(train_set, train_label)
    predict = nbc_1.predict(test_set)  # 在测试集上预测结果
    count = 0  # 统计预测正确的结果个数
    for left, right, tset in zip(predict, test_label, test_set):
        print(left, "-->", right, "-->", tset)
        if left == right:
            count += 1
        else:
            # 预测错的，单独记录
            if str(tset).__contains__("这个"):    # 如果存在“这个”关键字时，需进一步判断
                pass
    print("伯努利分类器准确率：", count / len(test_label))
    joblib.dump(nbc_1, bernousNB_save_path + "bernousNB_" + str(int(time.time())) + ".m")




def main():
    if os.path.exists(multinamialNB_save_path) is False:
        os.mkdir(multinamialNB_save_path)
    if os.path.exists(bernousNB_save_path) is False:
        os.mkdir(bernousNB_save_path)

    # for i in range(100):    # 多轮训练
        # # data = get_dataset()    # 加载最原始的输入数据
        # data = load_dataset()  # 加载手动提取的关键词数据
        # train_set, train_label, test_set, test_label = split_train_and_test_set(data, 1.0)
        # # print(train_set)
        # # print(train_label)
        # # print(test_set)
        # # print(test_label)
        # print("第", i, "轮：")
        # test_set = train_set
        # test_label = train_label
        # multinamialNB(train_set, train_label, test_set, test_label)
        # bernousNB(train_set, train_label, test_set, test_label)

    ## 新想法：全部数据用来训练，新截取关键词用来测试（7:3划分训练集，由于数据集较小，部分情况训练不到）
    # 1.加载准备好的关键词及意图，作为训练数据集
    org_data = load_dataset()
    train_set, train_label, test_set_tmp, test_label_tmp = split_train_and_test_set(org_data, 1.0)

    # 2.加载原始数据，现场切词，作为测试数据集
    test_data = get_dataset()
    train_set_tmp, train_label_tmp, test_set, test_label = split_train_and_test_set(test_data, 0.0)

    # for left, right in zip(train_set, train_label):
    #     print(left, "-->", right)

    # for left, right in zip(test_set, test_label):
    #     print(left, "==>", right)

    # 3.训练模型并得出准确率
    multinamialNB(train_set, train_label, test_set, test_label)
    bernousNB(train_set, train_label, test_set, test_label)


if __name__ == '__main__':
    main()