# -*- coding:utf-8 -*-

import os
import time
import random
import jieba
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer, HashingVectorizer, CountVectorizer
from sklearn.naive_bayes import BernoulliNB
from sklearn.externals import joblib
from sklearn.naive_bayes import GaussianNB        # 高斯贝叶斯分类器
from sklearn.naive_bayes import BaseDiscreteNB    # BaseDiscreteNB为抽象类，不能直接进行实例化，应该用基于该抽象类的MultinomialNB和BernoulliNB

'''
    贝叶斯：文本分类
    模型文件命名规范：
    多项式分类器：multinamialNB_时间戳_准确率_alpha参数值.m。
        例：multinamialNB_1574499534_82.3256%_0.03.m，1574499534时间，alpha=0.03时，准确率为82.3256%。
    伯努利分类器：bernousNB_时间戳_准确率_alpha参数值_binarize参数值.m。
        例：bernousNB_1574499534_82.3256%_0.02_None.m，1574499534时间，alpha=0.02，binarize=None时，准确率为82.3256%。
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
            new_sentences = get_words(arr[0])
            if isChat(new_sentences) is False:    # 如果不是闲聊
                data.append((new_sentences, arr[1]))
            else:    # 如果过滤掉主干成分之后句子为空，说明是在闲聊，进闲聊处理逻辑
                pass
                # chatFunction(line)    # 进闲聊function
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

'''
    是否闲聊：是，返回True；否，返回False
    定义闲聊：分词列表中，出现len(word)>1的情况，说明不是闲聊；否则定义为闲聊
'''
def isChat(sentences):
    tag = True    # 默认是闲聊
    if len(str(sentences).strip()) == 0:    # 如果分词列表无内容，则认为是闲聊
        return tag

    arr = str(sentences).split(" ")
    for a in arr:
        if len(a)>1:
            tag = False    # 标记该问话不是闲聊
            return tag


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
        if a in zhuhai_c:    # Entity实体（地名）的泛化
            # a = "地名1"
            a = "地名"
        elif a in others:    # Entity实体（地名）的泛化
            # a = "地名2"
            a = "地名"
        elif a in keywords:    # 其他关键字原样识别
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
    高斯贝叶斯分类器
    不能用：高斯分布需满足数值型，而该场景为标称型
'''
def gaussianNB(train_set, train_label, test_set, test_label):
    nbc = Pipeline([
        ('vect', TfidfVectorizer(

        )),
        ('clf', GaussianNB())
    ])

    nbc.fit(train_set, train_label)  # 训练多项式分类器
    predict = nbc.predict(test_set)  # 测试分类器分类效果
    count = 0
    for left, right, tset in zip(predict, test_label, test_set):
        print(left, "-->", right, "-->", tset)
        if left == right:
            count += 1
    print("高斯贝叶斯分类器准确率：", count / len(test_label))
    # joblib.dump(nbc, multinamialNB_save_path + "multinamialNB_" + str(int(time.time())) + ".m")

'''
    多项式分类器
    :param alpha：平滑系数，为0表示不平滑
    :param fit_prior：是否考虑先验概率，True，是；False，否
    :param class_prior：一个数组，指定每个类别的先验概率P(Y=C_1)、P(Y=C_2)...P(Y=C_k)。默认为None
    note：当fit_prior=False时候，class_prior填不填没有意义；这时所有类别具有相同先验概率：P(Y=C_k)=1/k，k为类别个数；
    当fit_prior=True and class_prior=None时，最终先验概率：P(Y=C_k)=m_k/m
    当fit_prior=True and class_prior<>None时，最终先验概率：P(Y=C_k)=class_prior
'''
def multinamialNB(train_set, train_label, test_set, test_label, alpha, fit_prior, class_prior):
    nbc = Pipeline([
        ('vect', TfidfVectorizer(

        )),
        ('clf', MultinomialNB(alpha=alpha,
                              fit_prior=fit_prior,
                              class_prior=class_prior))
    ])

    nbc.fit(train_set, train_label)    # 训练多项式分类器
    predict = nbc.predict(test_set)    # 测试分类器分类效果
    count = 0
    for left, right, tset in zip(predict, test_label, test_set):
        # print(left, "-->", right, "-->", tset)
        if left == right:
            count += 1
    print("多项式分类器准确率：", count/len(test_label))
    joblib.dump(nbc, multinamialNB_save_path + "multinamialNB_" + str(int(time.time())) + ".m")

'''
    伯努利分类器
    :param alpha：平滑系数，为0表示不平滑
    :param binarize：一个浮点是，特征值大于它，为1；小于它，为0。或者为None，表示已经是二元化了
    :param fit_prior：是否考虑先验概率，True，是；False，否
    :param class_prior：一个数组，指定每个类别的先验概率P(Y=C_1)、P(Y=C_2)...P(Y=C_k)。默认为None
'''
def bernousNB(train_set, train_label, test_set, test_label, alpha, binarize, fit_prior, class_prior):
    nbc_1 = Pipeline([
        ('vect', TfidfVectorizer(

        )),
        ('clf', BernoulliNB(alpha=alpha,
                            binarize=binarize,
                            fit_prior=fit_prior,
                            class_prior=class_prior))
    ])
    nbc_1.fit(train_set, train_label)
    predict = nbc_1.predict(test_set)  # 在测试集上预测结果
    count = 0  # 统计预测正确的结果个数
    for left, right, tset in zip(predict, test_label, test_set):
        # print(left, "-->", right, "-->", tset)
        if left == right:
            count += 1
        else:
            # 预测错的，单独记录
            if str(tset).__contains__("这个"):    # 如果存在“这个”关键字时，需进一步判断
                pass
    print("伯努利分类器准确率：", count / len(test_label))
    joblib.dump(nbc_1, bernousNB_save_path + "bernousNB_" + str(int(time.time())) + ".m")

'''
    多轮训练模型，找最优的参数组合
'''
def trainModel():
    # 1.加载准备好的关键词及意图，作为训练数据集
    org_data = load_dataset()
    train_set, train_label, test_set_tmp, test_label_tmp = split_train_and_test_set(org_data, 1.0)

    # 2.加载原始数据，现场切词，作为测试数据集
    test_data = get_dataset()
    train_set_tmp, train_label_tmp, test_set, test_label = split_train_and_test_set(test_data, 0.0)

    # # 训练多项式分类器
    # alpha = 0.0
    # fit_prior = True    # 考虑先验概率
    # class_prior = None    # 不手动指定每个类别的先验概率
    # for i in range(100):
    #     print(alpha, end=',')
    #     multinamialNB(train_set, train_label, test_set, test_label, alpha, fit_prior, class_prior)
    #     alpha = alpha + 0.01

    # # 训练伯努利分类器
    alpha = 0.0  # 平滑度
    # binarize=0.0   # 特征1/0的分界线
    fit_prior = True  # 考虑先验概率
    class_prior = None  # 不手动指定每个类别的先验概率
    # for i in range(100):
    #     for j in range(100):
    #         print(alpha, binarize, end=',')
    #         bernousNB(train_set, train_label, test_set, test_label, alpha, binarize, fit_prior, class_prior)
    #         binarize = binarize + 0.01
    #     alpha = alpha + 0.01
    #     binarize = 0.0    # 每一轮alpha算完之后，都将binarize归位

    # 伯努利分类器binarize为None的情况
    binarize = None
    for i in range(100):
        print(alpha, end=',')
        bernousNB(train_set, train_label, test_set, test_label, alpha, binarize, fit_prior, class_prior)
        alpha = alpha + 0.01



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
    # gaussianNB(train_set, train_label, test_set, test_label)
    # 经训练，多项式分类器取一下参数值时，准确率最高
    multi_alpha = 0.03
    fit_prior = True
    class_prior = None
    multinamialNB(train_set, train_label, test_set, test_label, alpha=multi_alpha, fit_prior=fit_prior, class_prior=class_prior)

    # 经训练，伯努利分类器取以下参数值时，准确率最高
    ber_alpha = 0.02
    binarize = None
    bernousNB(train_set, train_label, test_set, test_label, alpha=ber_alpha, binarize=binarize, fit_prior=fit_prior, class_prior=class_prior)

    # # 多轮训练，找最优的参数组合
    # trainModel()



if __name__ == '__main__':
    main()