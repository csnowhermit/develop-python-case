# D:/data/南站现场/广南一层中间12306录wav 20191029

import os

dirpath = "D:/data/南站现场/广南一层中间12306录wav20191030/"
for file in os.listdir(dirpath):
    # print(file)
    if file.endswith(".old"):
        # print("===========")
        # print(file[0: file.rfind(".")])
        os.rename(dirpath + file, dirpath + file[0: file.rfind(".")])