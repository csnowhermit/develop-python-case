# -*- coding:utf-8 -*-

import os
from NLP.textCategory.bayes.bayes_train import *

yuyi = []
with open(keywords_intention_file, encoding="utf-8") as fo:
    for line in fo.readlines():
        arr = line.strip().split("\t")
        yuyi.append(arr[1])

print(len(yuyi))
print(len(set(yuyi)))
print(set(yuyi))

print(os.path.dirname(__file__))
print(bernousNB_save_path)
print(os.path.join(os.path.dirname(__file__), bernousNB_save_path))

if os.path.exists(os.path.join(os.path.dirname(__file__), bernousNB_save_path)):
    # 按文件最后修改时间排序，reverse=True表示降序排序
    filelist = sorted(os.listdir(os.path.join(os.path.dirname(__file__), bernousNB_save_path)), key=lambda x: os.path.getctime(os.path.join(bernousNB_save_path, x)), reverse=True)
    print(os.path.join(bernousNB_save_path, filelist[0]))