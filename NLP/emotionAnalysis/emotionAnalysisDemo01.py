import time
import jieba

'''
    基于词典的社交媒体内容的情感分析
    https://blog.csdn.net/xyisv/article/details/79440711
'''

emotion_dic = {}
filename = 'BosonNLP_sentiment_score.txt'  # txt文件和当前脚本在同一目录下，所以不用写具体路径
with open(filename, 'rb') as file:
    while True:
        try:
            senList = file.readline().decode('utf-8')
            # print(senList)
            senList = senList[:-1]
            senList = senList.split(' ')
            emotion_dic[senList[0]] = senList[1]
        except IndexError:
            break

def get_emotion(score):
    emotion_archive = ['绝望，十分愤怒，对生活不在抱有希望',
                       '难过，失望，抑郁',
                       '有点小难过或者小愤怒',
                       '轻微的难受或者不屑，想得太多啦，洗洗睡觉吧',
                       '生活也就这样吧',
                       '有点小开心或者小激动',
                       '蛮开心的，生活多美好',
                       '喜笑颜开，每天的太阳都是新的，生活充满了希望']
    if score <= -3.9:
        return emotion_archive[0]
    elif -3.9 < score <= -2.5:
        return emotion_archive[1]
    elif -2.5 < score <= -1:
        return emotion_archive[2]
    elif -1 < score <= 0:
        return emotion_archive[3]
    elif 0 < score <= 1:
        return emotion_archive[4]
    elif 1 < score <= 2.5:
        return emotion_archive[5]
    elif 2.5 < score < 3.9:
        return emotion_archive[6]
    else:
        return emotion_archive[7]


# test = "才拒绝做爱情代罪的羔羊"
test = "" """
   五号线8点30到9点间，从区庄前开始一直到五羊邨之间临停四次！！！请给一个合理解释！！！！直接导致上班耽误！误工费怎么赔偿？本人保留向广州地铁追偿的权利！
"""

seg_list = jieba.cut(test, cut_all=True)
string = "/ ".join(seg_list)
string_list = string.split('/')
emotion_index = 0
time.sleep(1)
print("-5分为极端消极，5分为非常高兴")

for _ in range(len(string_list)):
    if string_list[_] in emotion_dic:
        emotion_index += float(emotion_dic[string_list[_]])
print(emotion_index)
print(get_emotion(emotion_index))
