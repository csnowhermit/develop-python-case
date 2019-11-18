# -*- coding:utf-8 -*-

'''
    朴素贝叶斯
'''

# 多项式分类器：词频型，以单词为粒度
# from sklearn import datasets
# iris = datasets.load_iris()
#
# from sklearn.naive_bayes import MultinomialNB
# clf = MultinomialNB()
# clf = clf.fit(iris.data, iris.target)
# y_pred=clf.predict(iris.data)
# print("多项分布朴素贝叶斯，样本总数： %d 错误样本数 : %d" % (iris.data.shape[0],(iris.target != y_pred).sum()))

# 伯努利分类器：文档型，以文档为粒度
from sklearn import datasets
iris = datasets.load_iris()

from sklearn.naive_bayes import BernoulliNB
clf = BernoulliNB()
clf = clf.fit(iris.data, iris.target)
y_pred=clf.predict(iris.data)
print("伯努利朴素贝叶斯，样本总数： %d 错误样本数 : %d" % (iris.data.shape[0],(iris.target != y_pred).sum()))


