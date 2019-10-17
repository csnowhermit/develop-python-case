
'''
    汉字转拼音
'''

from xpinyin import Pinyin

pin = Pinyin()
test1 = pin.get_pinyin("大河向东流")   #默认分割符为-
print(test1)

test2 = pin.get_pinyin("大河向东流", "")
print(test2)