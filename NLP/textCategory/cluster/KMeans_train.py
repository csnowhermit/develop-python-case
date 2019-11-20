# -*- coding:utf-8 -*-

from sklearn.cluster import KMeans
from sklearn.externals import joblib
from NLP.textCategory.decisionTree.decisionTree_train import *

'''
    采用聚类算法解决意图识别问题
'''

mat, labels = buildFeatureMat(load_dataset(), keywords)
test_mat, test_labels = buildFeatureMat(get_dataset(), keywords)

clf = KMeans(n_clusters=19)
s = clf.fit(mat)    # 训练
print(s)

keywords = list(keywords)
print(len(keywords))
print(len(set(test_labels)))
print(set(test_labels))
test_labels_num = []
for label in test_labels:
    for i in range(len(keywords)):
        if label == keywords[i]:
            test_labels_num.append(i)
            continue

print(test_labels_num)
predict_list = clf.predict(test_mat)    # 预测的list
print(predict_list)