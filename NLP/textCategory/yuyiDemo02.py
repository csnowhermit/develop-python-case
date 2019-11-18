# -*- coding:utf-8 -*-

import jieba

'''
    分类：贝叶斯或决策树
    1.关键字、珠海方向c打头车站、其他方向车站
    2.原语句中具体地名要替换为地名1（珠海方向），地名2（其他方向）
    
'''

jieba.load_userdict("./atomic.txt")    # 不可切分词

'''
    获取所有关键字
'''
def getAllKeywords():
    keywords = []
    with open("./keywords_intention.txt", encoding="utf-8") as fo:
        lines = fo.readlines()
        for line in lines:
            arr = line.strip().split("\t")
            for k in arr[0].strip().split(","):
                # if k in zhuhai_c:
                keywords.append(k)
            # print(arr[1], " ==> ", arr[0])
    return set(keywords)

'''
    获取珠海方向C开头的各站
'''
def getStationInZhuhai_c():
    zhuhai_c = []
    with open("./zhuhai.txt", encoding="utf-8") as fo:
        for line in fo.readlines():
            zhuhai_c.append(line.strip())
    return set(zhuhai_c)

'''
    获取其他方向各站
'''
def getOtherStation():
    others = []
    with open("./others.txt", encoding="utf-8") as fo:
        for line in fo.readlines():
            others.append(line.strip())
    return set(others)

'''
    构建特征向量
    1.切词，具体地名换乘地名1（珠海方向），地名2（其他方向）
    2.特征向量跟keywords匹配，构建0/1序列特征；（地名1、地名2和“地名”如何匹配？）
    3.生成“特征==>意图”，构建决策树
    
    新来消息：
    按例切词，构建特征向量，输入进模型（贝叶斯/决策树）求取结果
'''
def buildFeatureVector(keywords, zhuhai_c, others):
    # with open("./keywords_intention.txt", encoding="utf-8") as fo:
    #     for line in fo.readlines():
    #         arr = line.strip().split("\t")
    #         for k in set(keywords):
    #             for a in arr[0].strip().split(","):
    #                 pass
    with open("./原始例句.txt", encoding="utf-8") as fo:
        lines = fo.readlines()
        for line in lines:
            line = line.strip()
            arr = line.split("\t")
            print(arr[0], "\t", "/ ".join(list(jieba.cut(arr[0]))))




def main():
    keywords = getAllKeywords()
    zhuhai_c = getStationInZhuhai_c()
    others = getOtherStation()

    print(keywords)
    print(zhuhai_c)
    print(others)
    buildFeatureVector(keywords, zhuhai_c, others)

if __name__ == '__main__':
    main()





# # 1.对原始句子进行切词，看能不能切出我们需要的词语
#


