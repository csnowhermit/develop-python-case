#!/usr/bin/python26
#encoding=utf-8

import sys
import win32com
from win32com.client import Dispatch, constants
from io import StringIO
import win32clipboard
import win32com
from PIL import Image
import importlib

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

filepath = 'd:/fengjing.jpg'
image = Image.open(filepath)
output = StringIO()
# image.convert("RGB").save(output, "BMP")
data = output.getvalue()[14:]
print("data: %s" % data)
output.close()

#
setImageToClipboard(win32clipboard.CF_DIB, data)
content=getImageFromClipboard()

#
w = win32com.client.Dispatch('Word.Application')
# 后台运行，不显示，不警告
w.Visible = 0
w.DisplayAlerts = 0
doc = w.Documents.Open("d:/数字测试.docx")

search=u"pic"
repalce="newPic"

# 正文文字替换
w.Selection.Find.ClearFormatting()
#doc.Selection.Find.MatchWholeWord=True#全词匹配替换
w.Selection.Find.Replacement.ClearFormatting()
#WordApplication1.Selection.Find.Execute(FindText, MatchCase, MatchWholeWord,MatchWildcards, MatchSoundsLike, MatchAllWordForms, Forwards,Wrap, Format, ReplaceWith, Replace);
#w.Selection.Find.Execute(search, False, True, False, False, False, True, 1, True, repalce, 2)
w.Selection.Find.Execute(search, False, True, False, False, False, True, 1, True, "^c", 2)

doc.SaveAs("d:/demo2.docx")
doc.Close()
w.Quit()