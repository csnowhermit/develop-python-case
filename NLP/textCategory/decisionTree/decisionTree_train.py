# -*- coding:utf-8 -*-

import os
import time
import numpy as np
import pandas as pd
import graphviz
from sklearn import tree
from sklearn.datasets import load_wine    # 测试数据集
from sklearn.model_selection import train_test_split    # 训练集与测试机切分包
from sklearn.externals import joblib
from NLP.textCategory.bayes.bayes_train import *

'''
    基于决策树的文本分类
    分类树：使用信息增益或信息增益比或基尼系数来划分节点，每个节点样本的类别情况投票决定测试样本的类别。
    回归树：使用最大均方差来划分节点，每个节点样本的均值作为测试样本的回归预测值。
        回归树要求训练和测试label为float类型，因为需要计算均分方差。（文本分类场景不适合回归树）
    分类树中观察值为离散变量，回归树中观察值为连续变量。
    决策树调参过程：https://www.cnblogs.com/lyxML/p/9575820.html
'''

decisionTreeClassifier_model_path = "./model/"

'''
    构建特征向量：基于“关键字-意图”文件构建特征向量
'''
def buildFeatureMat(data, keywords):
    keywords = list(keywords)
    # print("keywords: ", keywords)
    mat = np.zeros((len(data), len(keywords)))    # 每行为各特征向量
    labels = []    # 意图类别，一一对应矩阵中各行

    for i in range(len(data)):
        arr = data[i][0].split(" ")    # 每行的关键字列表
        for a in arr:
            for j in range(len(keywords)):
                if a==keywords[j]:
                    mat[i, j] = 1
        labels.append(data[i][1])
    return mat, labels



'''
    构建决策树
'''
def buildDecisionTree(train_set, train_label, test_set, test_label):
    clf = tree.DecisionTreeClassifier(criterion="gini",
                                      splitter="best",
                                      max_features=4,    # 最大考虑几个特征
                                      max_depth=4        # 最大深度，避免过拟合
                                      )  # 初始化树模型，entropy，基于信息熵；gini，基尼系数
    # 回归树采用最大均方差来划分节点，每个节点样本的均值作为测试样本的回归预测值。该场景下不能用回归树，会报错：ValueError: could not convert string to float: '人工窗口'
    # clf = tree.DecisionTreeRegressor(criterion="mse")
    clf = clf.fit(train_set, train_label)      # 训练模型
    score = clf.score(test_set, test_label)    # 在测试数据上测试效果
    print("模型准确率：", score)

    # 持久化模型
    # joblib.dump(clf, decisionTreeClassifier_model_path + "decisionTreeClassifier_" + str(int(time.time())) + ".m")

    # 图像显示决策树
    dot_data = tree.export_graphviz(clf,
                                    out_file=None,
                                    feature_names=list(keywords),
                                    class_names=list(set(train_label)),
                                    filled=True,
                                    rounded=True)
    graph = graphviz.Source(dot_data)

    # 评估决策时：特征重要性
    # print([*zip(list(keywords), clf.feature_importances_)])


def main():
    if os.path.exists(decisionTreeClassifier_model_path) is False:
        os.mkdir(decisionTreeClassifier_model_path)

    for i in range(5):
        time.sleep(random.randint(2, 5))
        data = load_dataset()  # 从文件加载数据
        test_data = get_dataset()  # 加载原始文本，新切词为测试数据
        mat, labels = buildFeatureMat(data, keywords)  # 构建特征矩阵及label
        test_mat, test_labels = buildFeatureMat(test_data, keywords)  # 构建测试矩阵及label

        # train_set, test_set_tmp, train_label, test_label_tmp = train_test_split(mat, labels, test_size=0.0)
        # train_set_tmp, test_set, train_label_tmp, test_label = train_test_split(test_mat, test_labels, test_size=0.99)

        train_set, test_set, train_label, test_label = train_test_split(mat, labels, test_size=0.3)
        buildDecisionTree(train_set, train_label, test_set, test_label)

    # df = pd.concat([pd.DataFrame(mat), pd.DataFrame(labels)], axis=1)    # 特征矩阵+labels，做成DataFrame
    # print(df[177])


if __name__ == '__main__':
    main()