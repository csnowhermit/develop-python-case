# -*- coding: utf-8 -*-
# 微信测试：获取朋友信息
# 停用词获取：https://github.com/dongxiexidian/Chinese.git

import itchat
import matplotlib.pyplot as plt
import jieba
from wordcloud import WordCloud, ImageColorGenerator


# 设置自动登录
itchat.auto_login(hotReload=True)
# 抓取好友信息，第一条是自己的
friends = itchat.get_friends(update=True)[0:]

friendSavePath = str(friends[0]["UserName"]) + "_friend.txt"

with open(friendSavePath, mode='a', encoding="UTF-8") as f:
    for i in friends:
        # print(i)
        f.write(str(i) + "\n")

# 统计性别
def sex_count():
    sex_list = {}
    male = 'male'
    female = 'female'
    other = 'other'
    for i in friends[1:]:
        sex = i['Sex']  # 获取性别
        if sex == 1:
            sex_list[male] = sex_list.get(male, 0) + 1
        elif sex == 2:
            sex_list[female] = sex_list.get(female, 0) + 1
        else:
            sex_list[other] = sex_list.get(other, 0) + 1

    total = len(friends[1:])
    print("男：", sex_list[male], round(sex_list[male]/total, 2))
    print("女：", sex_list[female], round(sex_list[female]/total, 2))
    print("不明性别：", sex_list[other], round(sex_list[other]/total, 2))


# 画词云
def word_cloud():
    text = ''
    for i in friends[1:]:
        # print(str(i.get('Signature')) + '\n')
        text += str(i.get('Signature'))  # 获取个性签名

    mywordlist = []
    seg_list = jieba.cut(text, cut_all=True)    # 全模式
    liststr = "/ ".join(seg_list)
    # print(liststr)
    stopwords_path = 'stop_words.txt'
    f_stop = open(stopwords_path, mode='r', encoding='utf-8')
    try:
        f_stop_text= f_stop.read()
        # f_stop_text = unicode(f_stop_text, 'utf-8')
    finally:
        f_stop.close()
    f_stop_seg_list = f_stop_text.split('\n')
    for myword in liststr.split('/'):
        mywordlist.append(myword)
        # 过滤掉停用词
        if not (myword.strip() in f_stop_seg_list) and len(myword.strip()) > 1:
            mywordlist.append(myword)

    print(mywordlist)
    wordcloud_xy = WordCloud(background_color="white",width=618,
                          font_path='simhei.ttf',
                          height=384, font_step=3).generate(''.join(mywordlist))
    # backgroud_Image = plt.imread('bg.png')
    # '''设置词云样式'''
    # wordcloud_xy = WordCloud(
    #     background_color='white',  # 设置背景颜色
    #     mask=backgroud_Image,  # 设置背景图片
    #     font_path='C:\Windows\Fonts\STZHONGS.TTF',  # 若是有中文的话，这句代码必须添加，不然会出现方框，不出现汉字
    #     max_words=2000,  # 设置最大现实的字数
    #     max_font_size=150,  # 设置字体最大值
    #     random_state=30  # 设置有多少种随机生成状态，即有多少种配色方案
    # ).generate_from_text(''.join(mywordlist))

    plt.imshow(wordcloud_xy)
    plt.axis("off")
    plt.show()


if __name__ == '__main__':
    word_cloud()
    sex_count()
