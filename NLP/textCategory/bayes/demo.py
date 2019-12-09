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


# for i in range(1, 15):
#     print("南", i, "桥柱\t找南" ,i, "桥柱")
#     print("南", i, "桥\t找南" ,i, "桥柱")
#     print("南", i, "柱\t找南" ,i, "桥柱")
#     print("南", i, "桥墩\t找南" ,i, "桥柱")
#     print("南", i, "桥洞\t找南" ,i, "桥柱")
#     print("南", i, "洞口\t找南" ,i, "桥柱")

list = []
with open("../atomic.txt", encoding="utf-8") as fo:
    for line in fo.readlines():
        list.append(line.strip())
print(len(set(list)))

# for i in range(1, 29):
    # print("检票口A", i, "\t找A", i, "检票口")
    # print("A", i, "检票口\t找A", i, "检票口")
    # print("A", i, "\t找A", i, "检票口")
    # print("检票口a", i, "\t找A", i, "检票口")
    # print("a", i, "检票口\t找A", i, "检票口")
    # print("a", i, "\t找A", i, "检票口")
    # print("检票口B", i, "\t找B", i, "检票口")
    # print("B", i, "检票口\t找B", i, "检票口")
    # print("B", i, "\t找B", i, "检票口")
    # print("检票口b", i, "\t找B", i, "检票口")
    # print("b", i, "检票口\t找B", i, "检票口")
    # print("b", i, "\t找B", i, "检票口")
    # print("检票口A", i)
    # print("A", i, "检票口")
    # print("A", i)
    # print("检票口a", i)
    # print("a", i, "检票口")
    # print("a", i)
    # print("检票口B", i)
    # print("B", i, "检票口")
    # print("B", i)
    # print("检票口b", i)
    # print("b", i, "检票口")
    # print("b", i)
    # print(i, "出口\t找", i, "号到达口")
#     # print("到达口", i, "\t找", i, "号到达口")
#     # print("出口", i, "\t找", i, "号到达口")
#     # print(i, "号到达口\t找", i, "号到达口")
#     # print(i, "号出口\t找", i, "号到达口")
#     # print(i, "号口\t找", i, "号到达口")
#     print("到达口", i)
#     print("出口", i)
#     print(i, "号到达口")
#     print(i, "号出口")
#     print(i, "号口")

# for i in range(1, 15):
#     print("北", i, "\t找北", i, "桥柱")
#     print("南", i, "\t找南", i, "桥柱")

for i in range(20, 29):
    # print("检票口C", i, "\t找C", i, "检票口")
    # print("C", i, "检票口\t找C", i, "检票口")
    # print("C", i, "\t找C", i, "检票口")
    # print("检票口c", i, "\t找C", i, "检票口")
    # print("c", i, "检票口\t找C", i, "检票口")
    # print("c", i, "\t找C", i, "检票口")
    # print("检票口D", i, "\t找D", i, "检票口")
    # print("D", i, "检票口\t找D", i, "检票口")
    # print("D", i, "\t找D", i, "检票口")
    # print("检票口d", i, "\t找D", i, "检票口")
    # print("d", i, "检票口\t找D", i, "检票口")
    # print("d", i, "\t找D", i, "检票口")
    print("检票口C", i)
    print("C", i, "检票口")
    print("C", i)
    print("检票口c", i)
    print("c", i, "检票口")
    print("c", i)
    print("检票口D", i)
    print("D", i, "检票口")
    print("D", i)
    print("检票口d", i)
    print("d", i, "检票口")
    print("d", i)