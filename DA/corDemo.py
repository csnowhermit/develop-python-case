import pandas as pd
import pylab as plt
import numpy as np

'''
    计算相关性
'''

A = [28, 1, 61, 2, 50, 55, 33, 36, 95, 12, 54, 57, 57, 97, 70, 70, 55, 52, 89, 25]
B = [48, 39, 38, 16, 99, 48, 36, 59, 33, 91, 9, 50, 74, 74, 72, 16, 26, 20, 69, 42]

a = pd.Series(A)
b = pd.Series(B)

print(a.corr(b))
print(b.corr(a))
