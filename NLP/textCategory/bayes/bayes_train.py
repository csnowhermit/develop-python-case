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
        伯努利分类器：bernousNB_时间戳_准确率_alpha参数值_binarize参数值.m。
'''

atomic_file = "../atomic.txt"                   # 不可切分词
origin_sentences_file = "../原始例句.txt"       # 原始例句
keywords_intention_file = "../keywords_intention_all.txt"      # 整理后的关键字-意图
stopwords_file = "../stopwords.txt"            # 停用词
zhuhai_station_file = "../zhuhai.txt"          # 珠海方向车站
others_station_file = "../others.txt"          # 其他方向车站
destBus_station_file = "../destBus.txt"        # 坐大巴能到的目的地

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
            if isChat(new_sentences) is False:    # 如果不是闲聊，训练的时候过滤掉闲聊内容
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
# destBus = getWordList(destBus_station_file)
destBus = []

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
                    keywords.append("地名1")    # 一层候车的为“地名1”
                elif k in others:
                    keywords.append("地名")    # 三层候车的为“地名”
                elif k in destBus:
                    keywords.append("地名4")    # 坐大巴到的目的地，only
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
        if a in zhuhai_c:    # Entity实体（地名）的泛化，坐城轨
            a = "地名1"
        elif a in others:    # Entity实体（地名）的泛化，坐车（坐高铁）
            a = "地名"
        elif a in destBus:   # Entity实体（地名）的泛化，坐大巴
            a = "地名4"
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
    :return count/len(test_label)：返回在当前训练集上的准确率
    note：当fit_prior=False时候，class_prior填不填没有意义；这时所有类别具有相同先验概率：P(Y=C_k)=1/k，k为类别个数；
    当fit_prior=True and class_prior=None时，最终先验概率：P(Y=C_k)=m_k/m
    当fit_prior=True and class_prior<>None时，最终先验概率：P(Y=C_k)=class_prior
'''
def multinamialNB(train_set, train_label, test_set, test_label, alpha, fit_prior, class_prior, persist):
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
    right_rate = count/len(test_label)
    print("multinamialNB:", right_rate)

    # 如果需要持久化，则将模型导出
    if persist is True:
        joblib.dump(nbc, multinamialNB_save_path + "multinamialNB_" +
                    str(int(time.time())) + "_" +
                    str(right_rate)[str(right_rate).index(".") + 1: ] + "_" +
                    str(alpha)[str(alpha).index(".") + 1: ] + ".m")
    return right_rate

'''
    伯努利分类器
    :param alpha：平滑系数，为0表示不平滑
    :param binarize：一个浮点是，特征值大于它，为1；小于它，为0。或者为None，表示已经是二元化了
    :param fit_prior：是否考虑先验概率，True，是；False，否
    :param class_prior：一个数组，指定每个类别的先验概率P(Y=C_1)、P(Y=C_2)...P(Y=C_k)。默认为None
    :return count / len(test_label)：返回在当前训练集上的准确率
'''
def bernousNB(train_set, train_label, test_set, test_label, alpha, binarize, fit_prior, class_prior, persist):
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
    right_rate = count / len(test_label)
    print("bernousNB:", count / len(test_label))

    if persist is True:
        if binarize is None:
            joblib.dump(nbc_1, bernousNB_save_path + "bernousNB_" +
                        str(int(time.time())) + "_" +
                        str(right_rate)[str(right_rate).index(".") + 1:] + "_" +
                        str(alpha)[str(alpha).index(".") + 1:] + "_" +
                        str(binarize) + ".m")
        else:
            joblib.dump(nbc_1, bernousNB_save_path + "bernousNB_" +
                        str(int(time.time())) + "_" +
                        str(right_rate)[str(right_rate).index(".") + 1:] + "_" +
                        str(alpha)[str(alpha).index(".") + 1:] + "_" +
                        str(binarize)[str(binarize).index(".") + 1:] + ".m")
    return right_rate

'''
    多轮训练模型，训练多项式分类器，找最优的参数组合，并保存至模型文件
    :param num：训练轮数，从多少轮中找最优
'''
def trainMultinamialNB(num):
    # 1.加载准备好的关键词及意图，作为训练数据集
    org_data = load_dataset()
    train_set, train_label, test_set, test_label = split_train_and_test_set(org_data, 0.7)

    # # 2.加载原始数据，现场切词，作为测试数据集
    # test_data = get_dataset()
    # train_set_tmp, train_label_tmp, test_set, test_label = split_train_and_test_set(test_data, 0.0)

    result = []    # 保存每轮训练的参数及准确率
    alpha_increase_rate = float(1 / num)

    # 3.训练多项式分类器
    alpha = 0.0
    fit_prior = True    # 考虑先验概率
    class_prior = None    # 不手动指定每个类别的先验概率
    for i in range(num):
        print(alpha, end=',')
        right_rate = multinamialNB(train_set, train_label, test_set, test_label, alpha, fit_prior, class_prior, persist=False)
        result.append((alpha, right_rate))
        alpha = alpha + alpha_increase_rate

    # 4.处理，找出最优的参数组合并导出模型
    scores = max([i[1] for i in result])  # 最大准确率
    alpha = [i[0] for i in result if i[1] == scores][0]  # 对应的参数值，多参数值可用的情况下只取第一个
    multinamialNB(train_set, train_label, test_set, test_label, alpha, fit_prior, class_prior, persist=True)



'''
    多轮训练模型：训练伯努利分类器，找最优的参数组合，并保存至模型文件
    :param num：训练轮数，从多少轮中找最优
'''
def trainBinarize(num_alpha, num_binarize):
    # 1.加载准备好的关键词及意图，作为训练数据集
    org_data = load_dataset()
    train_set, train_label, test_set, test_label = split_train_and_test_set(org_data, 0.7)

    # # 2.加载原始数据，现场切词，作为测试数据集
    # test_data = get_dataset()
    # train_set_tmp, train_label_tmp, test_set, test_label = split_train_and_test_set(test_data, 0.0)

    result = []  # 保存每轮训练的参数及准确率
    alpha_increase_rate = float(1 / num_alpha)
    binarize_increase_rate = float(1 / num_binarize)

    # 3.伯努利分类器，不考虑特征1/0的分界线
    alpha = 0.0  # 平滑度
    binarize = None
    fit_prior = True  # 考虑先验概率
    class_prior = None  # 不手动指定每个类别的先验概率
    for i in range(num_alpha):
        print(alpha, end=',')
        right_rate = bernousNB(train_set, train_label, test_set, test_label, alpha, binarize, fit_prior, class_prior, persist=False)
        result.append((alpha, binarize, right_rate))
        alpha = alpha + alpha_increase_rate

    # 4.伯努利分类器，指定值作为特征1/0的分界线
    alpha = 0.0  # 平滑度归零，继续训练
    binarize=0.0   # 特征1/0的分界线
    fit_prior = True  # 考虑先验概率
    class_prior = None  # 不手动指定每个类别的先验概率
    for i in range(num_alpha):
        for j in range(num_binarize):
            print(alpha, binarize, end=',')
            right_rate = bernousNB(train_set, train_label, test_set, test_label, alpha, binarize, fit_prior, class_prior, persist=False)
            result.append((alpha, binarize, right_rate))
            binarize = binarize + binarize_increase_rate
        alpha = alpha + alpha_increase_rate
        binarize = 0.0    # 每一轮alpha算完之后，都将binarize归位

    # 5.处理，找出最优的参数组合并导出模型
    scores = max([i[2] for i in result])  # 最大准确率
    alpha = [i[0] for i in result if i[2] == scores][0]  # 一个准确率对应多个参数时，取第一个
    binarize = [i[1] for i in result if i[2] == scores and i[1] == alpha]  # 对应的参数值
    if len(binarize) == 0:
        binarize = None
    else:
        binarize = binarize[0]
    bernousNB(train_set, train_label, test_set, test_label, alpha, binarize, fit_prior, class_prior, persist=True)



def main():
    if os.path.exists(multinamialNB_save_path) is False:
        os.mkdir(multinamialNB_save_path)
    if os.path.exists(bernousNB_save_path) is False:
        os.mkdir(bernousNB_save_path)

    # ## 新想法：全部数据用来训练，新截取关键词用来测试（7:3划分训练集，由于数据集较小，部分情况训练不到）
    # # 1.加载准备好的关键词及意图，作为训练数据集
    # org_data = load_dataset()
    # train_set, train_label, test_set_tmp, test_label_tmp = split_train_and_test_set(org_data, 1.0)
    #
    # # 2.加载原始数据，现场切词，作为测试数据集
    # test_data = get_dataset()
    # train_set_tmp, train_label_tmp, test_set, test_label = split_train_and_test_set(test_data, 0.0)

    # 3.多轮训练多项式分类器
    trainMultinamialNB(100)

    # 4.多轮训练伯努利分类器
    trainBinarize(100, 10)


if __name__ == '__main__':
    main()