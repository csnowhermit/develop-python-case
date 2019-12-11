# -*- coding:utf-8 -*-

from NLP.textCategory.bayes.bayes_train import keywords, atomic_file
from NLP.textCategory.utils.genAllStations import genStationList

'''
    自动生成atomic.txt，切词时确保指定词不切开
    词语来源：NLP.textCategory.bayes.bayes_train.keywords
'''

'''
    基于keywords，依据len(keyword)降序排序，生成atomic.txt
    1.全国地名、车站名确保完整切词；
    2.指定关键词确保完整切词；
'''
def genAtoFile():
    mydict = {}

    station_names = genStationList()
    for station in station_names:       # 处理全国地名、火车站名
        mydict[station] = len(station)

    for key in keywords:        # 处理关键词
        mydict[key] = len(key)

    # 默认升序排序，加reverse=True，降序排序
    sort_tuple_list = sorted([(value, key) for (key, value) in mydict.items()], reverse=True)
    print(sort_tuple_list)

    # 写入文件
    with open(atomic_file, encoding="utf-8", mode="w") as fo:
        for tuple in sort_tuple_list:
            fo.write(tuple[1] + "\n")
            # fo.writelines(tuple[1])
    print("finished")

def main():

    genAtoFile()

if __name__ == '__main__':
    main()