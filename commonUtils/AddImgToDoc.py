#!/usr/bin/python26
# encoding=utf-8

"""
    将图片添加到word文档中
"""

import win32com.client as win32

word = win32.gencache.EnsureDispatch("Word.Application")
doc = word.Documents.Add()
word.Selection.InlineShapes.AddPicture(FileName="d:/fengjing.jpg", LinkToFile=False, SaveWithDocument=True)
doc.SaveAs("d:/test.doc")
doc.Close(True)
word.Application.Quit()
