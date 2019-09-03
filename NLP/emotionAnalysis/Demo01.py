import jieba
import pandas as pd

'''
    jieba分词后情感分析
    https://blog.csdn.net/qq_41185868/article/details/84864905
'''

data1= '今天上海的天气真好！我的心情非常高兴！如果去旅游的话我会非常兴奋！和你一起去旅游我会更加幸福！'
data2= '今天上海天气真差,非常讨厌下雨,把我冻坏了,心情太不高兴了,不高兴,我真的很生气！'
data3= '美国华裔科学家,祖籍江苏扬州市高邮县,生于上海,斯坦福大学物理系,电子工程系和应用物理系终身教授!'

def readExcel(filename):
    df = pd.DataFrame(pd.read_excel(filename, encoding='gbk'))
    return df

filename = "../data/情感词汇本体/情感词汇本体.xlsx"
df = readExcel(filename)
# print(df['词语'])
posiType = ['PA', 'PE', 'PD', 'PH', 'PG', 'PB', 'PK']
posiDict = list(df[df.情感分类.isin(posiType)]['词语'])    # 积极词汇
negType = ['NB', 'NJ', 'NH', 'PF', 'NI', 'NC', 'NG', 'NE', 'ND', 'NN', 'NK', 'NL']
negDict = list(df[df.情感分类.isin(negType)]['词语'])    # 消极词汇
print(type(negDict))
for n in negDict:
    print(n)


'''
    获取句子的情感得分
'''
# def sentiment_score_list(data):
#     seg_sentence = data.split('。')
#     count1 = []
#     count2 = []
#
#     for sen in seg_sentence:
#         words = jieba.lcut(str(sen), cut_all=False)    # 左侧切分
#         i = 0  # 记录扫描到的词的位置
#         a = 0  # 记录情感词的位置
#
#         poscount = 0  # 积极词的第一次分值
#         poscount2 = 0  # 积极词反转后的分值
#         poscount3 = 0  # 积极词的最后分值（包括叹号的分值）
#         negcount = 0
#         negcount2 = 0
#         negcount3 = 0
#
#         for word in words:
#             if word in posdict:  # 判断词语是否是积极情感词
#                 poscount += 1
#                 c = 0
#                 for w in words[a:i]:  # 扫描情感词前的程度词
#                     if w in mostdict:
#                         poscount *= 4.0
#                     elif w in verydict:
#                         poscount *= 3.0
#                     elif w in moredict:
#                         poscount *= 2.0
#                     elif w in ishdict:
#                         poscount *= 0.5
#                     elif w in deny_word:
#                         c += 1
#                 if judgeodd(c) == 'odd':  # 扫描情感词前的否定词数
#                     poscount *= -1.0
#                     poscount2 += poscount
#                     poscount = 0
#                     poscount3 = poscount + poscount2 + poscount3
#                     poscount2 = 0
#                 else:
#                     poscount3 = poscount + poscount2 + poscount3
#                     poscount = 0
#                 a = i + 1  # 情感词的位置变化
#             elif word in negdict:  # 消极情感的分析，与上面一致
#                 negcount += 1
#                 d = 0
#                 for w in words[a:i]:
#                     if w in mostdict:
#                         negcount *= 4.0
#                     elif w in verydict:
#                         negcount *= 3.0
#                     elif w in moredict:
#                         negcount *= 2.0
#                     elif w in ishdict:
#                         negcount *= 0.5
#                     elif w in degree_word:
#                         d += 1
#                 if judgeodd(d) == 'odd':
#                     negcount *= -1.0
#                     negcount2 += negcount
#                     negcount = 0
#                     negcount3 = negcount + negcount2 + negcount3
#                     negcount2 = 0
#                 else:
#                     negcount3 = negcount + negcount2 + negcount3
#                     negcount = 0
#                 a = i + 1
#             elif word == '！' or word == '!':  ##判断句子是否有感叹号
#                 for w2 in words[::-1]:  # 扫描感叹号前的情感词，发现后权值+2，然后退出循环
#                     if w2 in posdict or negdict:
#                         poscount3 += 2
#                         negcount3 += 2
#                         break
#             i += 1  # 扫描词位置前移
#
#             # 以下是防止出现负数的情况
#             pos_count = 0
#             neg_count = 0
#             if poscount3 < 0 and negcount3 > 0:
#                 neg_count += negcount3 - poscount3
#                 pos_count = 0
#             elif negcount3 < 0 and poscount3 > 0:
#                 pos_count = poscount3 - negcount3
#                 neg_count = 0
#             elif poscount3 < 0 and negcount3 < 0:
#                 neg_count = -poscount3
#                 pos_count = -negcount3
#             else:
#                 pos_count = poscount3
#                 neg_count = negcount3
#
#             count1.append([pos_count, neg_count])
#         count2.append(count1)
#         count1 = []
#     return count2



def sentiment_score():
    pass

def main():
    pass
    # print(sentiment_score(sentiment_score_list(data1)))
    # print(sentiment_score(sentiment_score_list(data2)))
    # print(sentiment_score(sentiment_score_list(data3)))

if __name__ == '__main__':
    main()