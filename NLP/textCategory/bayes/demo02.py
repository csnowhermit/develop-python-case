# -*- coding:utf-8 -*-

from NLP.textCategory.bayes.bayes_train import *

print(len(keywords))
print(keywords)
print(len(set(keywords)))

atoList = []
with open("../atomic.txt", encoding="utf-8") as fo:
    for line in fo.readlines():
        atoList.append(line.strip())


print(len(atoList))
print(atoList)

for a in atoList:
    if a not in keywords:
        print(a)
print("==")

