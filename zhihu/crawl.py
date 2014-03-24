#!/usr/bin/env python
#-*-coding:utf-8-*-
import zhihu
from xlrd import open_workbook
from xlutils.copy import copy

rb = open_workbook('test.xlsx')
wb = copy(rb)

sheetTopic = wb.get_sheet(0)
sheetAnswer = wb.get_sheet(1)
sheetUser = wb.get_sheet(2)

s = zhihu.login()

