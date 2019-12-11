# -*- coding:utf-8 -*-

from NLP.textCategory.bayes.bayes_train import *

yuyi = []
with open(keywords_intention_file, encoding="utf-8") as fo:
    for line in fo.readlines():
        arr = line.strip().split("\t")
        yuyi.append(arr[1])

print(len(yuyi))
print(len(set(yuyi)))
print(set(yuyi))