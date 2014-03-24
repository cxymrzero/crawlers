#!/usr/bin/env python
#-*-coding:utf-8-*-
import zhihu
from xlrd import open_workbook
from xlutils.copy import copy

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

rb = open_workbook('zhihu.xlsx')
wb = copy(rb)

sheetTopic = wb.get_sheet(0)
sheetAnswer = wb.get_sheet(1)
sheetUser = wb.get_sheet(2)

s = zhihu.login()
topic = zhihu.topic(s, "http://www.zhihu.com/topic/19552330/top-answers")
urls = topic.links()

def insertList(lst, col, row, sheet):
    for i in lst:
        #i = i.encode('utf-8')
        sheet.write(col, row, i)
        col += 1
        return col

def insertItem(item, col, row, sheet):
    sheet.write(col, row, item)

insertList(topic.question(), 1, 0, sheetTopic)
def ProcessTopic(s, urls):
    col = 1
    
    for url in urls:
        answer = zhihu.answer(s, url)
        insertItem(answer.answerednum(), col, 1, sheetTopic)
        insertItem(answer.type(), col, 2, sheetTopic)
        insertItem(answer.watched(), col, 3, sheetTopic)
        col += 1
        insertList(answer.wordcount(), ListCol, 0, sheetAnswer)

def ProcessAnswer(s, urls):
    col = 1
    for url in urls:
        
wb.save('zhihu.xlsx')
