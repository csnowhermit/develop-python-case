# -*- coding:utf-8 -*-

import os
import jieba
import jieba.posseg as pesg
from NLP.textCategory.bayes.bayes_train import keywords, keywords_intention_file

# jieba.load_userdict("../atomic.txt")
# with open("../原始例句.txt", encoding="utf-8") as fo:
#     for line in fo.readlines():
#         words = pesg.cut(line.split("\t")[0])
#         for w in words:
#             # print(w.flag, w.word, end="/ ")
#             print(w.flag, end=" ")
#         print()

# print(keywords_intention_file)
# print(keywords)

# dirname = "D:/data/南站现场/广南一层中间12306录wav20191030/"
# for file in os.listdir(dirname):
#     if file.endswith(".old"):
#         os.rename(dirname + file, dirname + file[0: -4])


for i in range(1, 15):
    print("南", i, "桥柱\t找南" ,i, "桥柱")
    print("南", i, "桥\t找南" ,i, "桥柱")
    print("南", i, "柱\t找南" ,i, "桥柱")
    print("南", i, "桥墩\t找南" ,i, "桥柱")
    print("南", i, "桥洞\t找南" ,i, "桥柱")
    print("南", i, "洞口\t找南" ,i, "桥柱")

list = []
with open("../atomic.txt", encoding="utf-8") as fo:
    for line in fo.readlines():
        list.append(line.strip())

print(len(set(list)))