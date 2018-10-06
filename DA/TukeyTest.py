#!/usr/bin/python26
# encoding=utf-8

"""
    异常值检测
    使用算法：Tukey's Test
"""

import numpy as np
import stats as sts

list = [1, 4, 8, 90, 98, 44, 35, 56, 2, 41, 11, 24, 23, 45, 500, 150]
print(list)

# 求四分位数
print('下四分位数：', sts.quantile(list, p=0.25))
print('上四分位数：', sts.quantile(list, p=0.75))
q1 = sts.quantile(list, p=0.25)
q3 = sts.quantile(list, p=0.75)

# k=1.5  中度异常
k1 = 1.5
g_min_m = q1 - k1 * (q3 - q1)
g_max_m = q3 + k1 * (q3 - q1)

# k=3 重度异常
k2 = 3
g_min_b = q1 - k2 * (q3 - q1)
g_max_b = q3 + k2 * (q3 - q1)

# g_min_b, g_min_m, g_max_m, g_max_b
print(g_min_b, g_min_m, g_max_m, g_max_b)
for i in list:
    if i < g_min_b or i > g_max_b:
        print('重度异常值：', i)
    elif i > g_min_b and i < g_min_m:
        print('中度异常值：', i)
    elif i > g_max_m and i < g_max_b:
        print('中度异常值：', i)
