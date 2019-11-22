# -*- coding: utf-8 -*-

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.response_selection import get_most_frequent_response
from NLP.textCategory.bayes.bayes_train import *

chatbot = ChatBot('Training Example',
                  storage_adapter='chatterbot.storage.SQLStorageAdapter',
                  logic_adapters=[
                      'chatterbot.logic.BestMatch',
                      'chatterbot.logic.MathematicalEvaluation',
                      # 'chatterbot.logic.TimeLogicAdapter',
                      'chatterbot.logic.SpecificResponseAdapter'
                  ],
                  response_selection_method=get_most_frequent_response    # 返回最常用的结果
                  )

trainer = ChatterBotCorpusTrainer(chatbot)

# 训练语料库，目录：D:\Anaconda3\Lib\site-packages\chatterbot_corpus\data\chinese
trainer.train(
    # "chatterbot.corpus.chinese"     # 中文
    "chatterbot.corpus.mytrain.zuoche"
)

# while True:
#     try:
#         print(">>> ", end="")
#         response = chatbot.get_response(input())
#         print(response)
#     except(KeyboardInterrupt, EOFError, SystemExit):
#         break

questions = ["贵州遵义的高铁是在这边坐车吗",
"我从贵州遵义过来南站换乘在哪换乘",
"贵州遵义的高铁在哪上三楼",
"汕头的高铁是在这边坐车吗",
"我从汕头过来南站换乘在哪换乘",
"汕头的高铁在哪上三楼",
"要去哪里坐车",
"哎，帅哥问我这个，我去哪里坐车呢",
"都要到哪里去坐车找不到啊？第1次来",
"不好意思，我想问一下这是在哪坐车",
"是是我走错了找不着了写大名好，城轨也是在这坐车吧",
"他这个坐车从哪里上去啊",
"我去小榄那边，我到哪里去坐车啊",
"我这怎么坐车啊？这个",
"那我要怎么坐车啊",
"就是不知道怎么坐车啊",
"这是从哪里做坐车",
"唉，您好，我想问一下高铁往哪个方向",
"进站进高铁站去阳江都在哪边啊",
"从哪里上高铁",
"我想问一下去坐高铁从哪个进口进去的",
"虎门的高铁是在这边坐车吗",
"我从东莞过来转车该怎么上三楼",
"我从虎门过来南站换乘在哪换乘",
"虎门的高铁在哪上三楼",
"我买了票了，南站到汕头了，往那边走真的是走到头之后上3楼啊",
"问一下哪里上3楼",
"那你好，问一下这个是直接上3楼吗？在这里可以上吗",
"怎么上3楼去啊",
"3楼怎么上去",
"我买了票了，南站到汕头了，怎么上去上去3楼啊",
"问一下哪里能到3楼",
"那你好，问一下这个是能到3楼吗？在这里可以上吗",
"总之走到头之后就直接到3楼，直走到头是吗",
"怎么上去3楼",
"西出口的出发厅在什么位置",
"我就说是有人来接我，他在出发厅等我",
"西出口的出发厅怎么上去",
"东出口的出发厅怎么走",
"东出口的出发厅在什么位置",
"东出口出发厅在哪，有人在那接我",
"东出发平台在哪个位置",
"出发平台有人等我，怎么过去",
"出发平台等人，怎么走",
"出发平台进站是在几楼",
"就哪进站呢",
"进站进高铁站去阳江都在哪边啊",
"这个路那个进站口在哪里",
"哪里是进站口啊",
"那个进站口是在哪里啊",
"那进站口怎么进去啊",
"检票进站了",
"你好，请问一下这个从哪里进站的",
"请问一下那个我们要去候车室进站口往哪里走",
"如果进站的话是从正门进吗",
"进站地点在哪里",
"3层怎么上去",
"我买了票了，南站到汕头了，怎么上去3层啊",
"那我直接到3层啊，就出发了吗",
"问一下哪里能到3层",
"那你好，问一下这个是能到3层吗？在这里可以上吗",
"怎么上去3层",
"东出发平台怎么走",
"西出发平台怎么走"]

for q in questions:
    words = get_words(str(q))    # 用entity代替具体实体
    s = ""
    for w in words:
        s = s + w
    print(s)
    # print(chatbot.get_response(q))
