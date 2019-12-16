# -*- coding：utf-8 -*-

import platform
from ctypes import *

'''
    python2中会显示完整字符串，而python3显示的是第一个字符。
    原因：python2中字符编码存储的是ascii码（1bytes），而python3中存储的是unicode码（2bytes）
    例：'abc'，在python2中为：97 98 99 0（最后一个0代表字符串结束）
        python3中为：97 0 98 0 99 0 0（最后一个0代表字符串结束）
        这时libc.printf()检测到0就认为字符串结束，so，只显示第一个字符。
    解决办法："abc".encode("ascii")
    底层是C/C++，了解C/C++对字符串的处理方式（遇0/\0代表结束，故需给出读取长度）。
'''

if platform.system() == 'Windows':
    libc = cdll.LoadLibrary('msvcrt.dll')
elif platform.system() == 'Linux':
    libc = cdll.LoadLibrary('libc.so.6')

libc.printf("Hello ctypes!".encode("ascii"))