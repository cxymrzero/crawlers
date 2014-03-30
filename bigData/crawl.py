#-*-coding:utf-8-*-
import requests
from xlrd import open_workbook
from xlutils.copy import copy
from time import localtime, time, strftime

d = {}
for i in range(1, 26): #共25页
    post_data = {'pageIndex':str(i), 'pageSize':'20'}
    post_url = "http://102.alibaba.com/competition/addDiscovery/queryTotalRank.json"
    r = requests.post(post_url, post_data)
    jsonData = r.json()['returnValue']['datas']

    #以大学名为key
    for j in range(0, 20):
        uname = jsonData[j]['university']
        if d.has_key(uname):
            d[uname].append(jsonData[j])
        else:
            d[uname] = [jsonData[j]]

#for i in d.keys():
#    print i, d[i]

rb = open_workbook('data.xlsx')
wb = copy(rb)
ws = wb.get_sheet(0)

row = 1
for dkey in d.keys():
    dvalueList = d[dkey]
    for dvalueItem in dvalueList:
        #dvalueItem -> dict
        ws.write(row, 0, dvalueItem['recall'])
        ws.write(row, 1, dvalueItem['university'])
        ws.write(row, 2, dvalueItem['precision'])
        ws.write(row, 3, dvalueItem['rank'])
        ws.write(row, 4, dvalueItem['dateString'])
        ws.write(row, 5, dvalueItem['score'])
        ws.write(row, 6, dvalueItem['teamName'])
        ws.write(row, 7, dvalueItem['date'])
        ws.write(row, 8, dvalueItem['id'])

        row += 1

#wb.save('data.xlsx')
timeData = localtime(time())
timeStr = strftime('%Y-%m-%d-ali-data.xls', timeData)

wb.save(timeStr)
