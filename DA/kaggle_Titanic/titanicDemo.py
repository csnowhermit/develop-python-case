import pandas as pd

'''
    数据分析Demo：分析不同指标对生存率/获救率的影响
'''

df = pd.read_csv("Titanic.csv")
print(df.shape)
print(df.describe())

df['Age'] = df['Age'].fillna(df['Age'].median)    # 年龄为空处补数据：补平均值
print(df.describe())