# -*- coding: utf-8 -*-
# 微信测试

import itchat
import matplotlib.pyplot as plt
import jieba
from wordcloud import WordCloud, ImageColorGenerator


# 设置自动登录
itchat.auto_login(hotReload=True)
# 抓取好友信息
friends = itchat.get_friends(update=True)[0:]

# print(friends)

for i in friends:
    print(i)




