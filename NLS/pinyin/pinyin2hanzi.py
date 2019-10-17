
'''
    拼音转汉字
'''

def pinyin_2_hanzi(pinyinList):
    from Pinyin2Hanzi import DefaultDagParams
    from Pinyin2Hanzi import dag
    dagParams = DefaultDagParams()
    result = dag(dagParams, pinyinList, path_num=10, log=True) #10代表侯选值个数
    for item in result:
        socre = item.score
        res = item.path # 转换结果
        print(socre, res)

if __name__ == '__main__':
    lists1 = ['dong', 'bei', 'jun', 'de', 'yi', 'xie', 'ai', 'guo', 'jiang', 'shi', 'ye', 'fen', 'qi', 'kang', 'zhan']
    pinyin_2_hanzi(lists1)