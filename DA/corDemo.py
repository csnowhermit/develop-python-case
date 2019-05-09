import pandas as pd
import pylab as plt
import numpy as np

import cx_Oracle as cxo

'''
    计算相关性
'''

dsn_tnsstr = cxo.makedsn('localhost', '1521', 'ORCLPDB')
dsn_tns = dsn_tnsstr.replace('SID', 'SERVICE_NAME')
conn = cxo.connect("test", "123456", dsn_tns)
curs = conn.cursor()

rs = curs.execute("select substr(TEMPERATURE, 0, length(TEMPERATURE)-1), substr(HUMIDITY, 0, length(HUMIDITY)-1), substr(WINP, 0, length(WINP)-1), TEMP from w_weather")
result = rs.fetchall()

df = pd.DataFrame(list(result))
print(df.shape)
print(df.head())

print(df.corr())              # pearson相关系数
print(df.corr("kendall"))    # kendall Tau相关系数
print(df.corr('spearman'))   # spearman秩相关

# for res in result:
#     print(res[0][0:len(str(res[0]))-1], res[1][0:len(str(res[1]))-1], res[2][0:len(str(res[2]))-1], res[3])
