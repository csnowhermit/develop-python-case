# -*- coding:utf-8 -*-

with open("./keywords_intention.txt", encoding="utf-8") as fo:
    lines = fo.readlines()
    for line in lines:
        arr = line.strip().split("\t")
        print(arr[1], " ==> ", arr[0])