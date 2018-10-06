#!/usr/bin/python26
# encoding=utf-8

"""
    Python操作word文档：字符串替换
"""

import sys
import importlib

from win32com.client import Dispatch, constants
from io import StringIO

import win32clipboard
import win32com
from PIL import Image

importlib.reload(sys)


def setImageToClipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()


def getImageFromClipboard():
    win32clipboard.OpenClipboard()
    d = win32clipboard.GetClipboardData(win32clipboard.CF_DIB)
    win32clipboard.CloseClipboard()
    return d


def getDocObject(docpath):
    w = win32com.client.Dispatch('Word.Application')  # 打开word应用程序
    w.Visible = 0  # 后台运行，不显示
    w.DisplayAlerts = 0  # 不警告
    doc = w.Documents.Open(docpath)  # 打开word文件
    return (w, doc)


def replaceTextValue(w, oldStr, newStr):
    """
    正文文字替换
    :param w:
    :param oldStr:
    :param newStr:
    :return:
    """
    w.Selection.Find.ClearFormatting()
    # doc.Selection.Find.MatchWholeWord=True#全词匹配替换
    w.Selection.Find.Replacement.ClearFormatting()
    w.Selection.Find.Execute(oldStr, False, False, False, False, False, True, 1, True, newStr, 2)


def closeAll(w, doc):
    if doc is not None:
        doc.close()
    if w is not None:
        w.quit()


def main():
    # filepath = 'd:/fengjing.jpg'
    # image = Image.open(filepath)
    # output = StringIO()
    # # image.convert("RGB").save(output, "BMP")
    # data = output.getvalue()[14:]
    # print("data: %s" % data)
    # output.close()

    # setImageToClipboard(win32clipboard.CF_DIB, data)
    # content = getImageFromClipboard()

    (w, doc) = getDocObject("d:/数字测试.docx")
    print('----------------')
    print('段落数: ', len(doc.Paragraphs))

    # # 根据下标遍历段落
    # for i in range(len(doc.Paragraphs)):
    #     print("%d ==> %s", i, doc.Paragraphs)
    #
    # # 直接遍历段落
    # for param in doc.Paragraphs:
    #     print(param)

    replaceTextValue(w, "pic", "newPic")
    doc.SaveAs("d:/clipboard_test2.docx")

    # closeAll(w, doc)


if __name__ == '__main__':
    main()
