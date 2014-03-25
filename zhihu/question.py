#-*-coding:utf-8-*-
from zhihu import topic, answer, user
from xlrd import open_workbook
from xlutils.copy import copy

url1 = "http://www.zhihu.com/topic/19552330/top-answers" #程序员
url2 = "http://www.zhihu.com/topic/19550921/top-answers" #时间管理
url3 = "http://www.zhihu.com/topic/19551137/top-answers" #美食

def GetQ(session, baseurl, row):
    rb = open_workbook('zhihu.xlsx')
    wb = copy(rb)
    ws = wb.get_sheet(0)

    for i in range(1, 11):
        url = ''.join([baseurl, '?page=', str(i)])
        topicObj = topic(session, url)
        row_topic = row
        for ques in topicObj.question():
            ws.write(row_topic, 0, ques)
            row_topic += 1
            print '%d, 1' % row_topic
        links = topicObj.links()
        for link in links:
            try:
                print link
                answerObj = answer(session, link)
                ws.write(row, 1, answerObj.answerednum())
                ws.write(row, 2, answerObj.type())
                ws.write(row, 3, answerObj.watched())
                row += 1
            except TypeError:
                continue
            except AttributeError:
                continue
            print '%d, 123' % row
        wb.save('zhihu.xlsx')

    return row

def GetA(session, url, row):
    rb = open_workbook('zhihu.xlsx')
    wb = copy(rb)
    ws = wb.get_sheet(1)

    topicObj = topic(session, url)
    links = topicObj.links()
    for link in links:
        try:
            answerObj = answer(session, link)
            answerRow = row
            for item in answerObj.wordcount():
                ws.write(answerRow, 0, item)
                answerRow += 1 #1
            answerRow = row
            for item in answerObj.agree():
                ws.write(answerRow, 1, item)
                answerRow += 1 #2
            answerRow = row
            for item in answerObj.time():
                ws.write(answerRow, 2, item)
                answerRow += 1 #3
            answerRow = row
            for item in answerObj.havePic():
                ws.write(answerRow, 3, item)
                answerRow += 1 #4
            answerRow = row
            for item in answerObj.isunknown():
                ws.write(answerRow, 4, item)
                answerRow += 1 #5
            print '%d 1345' % answerRow
            row += 10

        except TypeError:
            continue
        except AttributeError:
            continue
    wb.save('zhihu.xlsx')

def GetUser(session, url, row):
    rb = open_workbook('zhihu.xlsx')
    wb = copy(rb)
    ws = wb.get_sheet(2)

    Topic = topic(session, url)
    QuesUrls = Topic.links()
    for link in QuesUrls:
        Answer = answer(session, link)
        print link
        UserLinks = Answer.getUser()
        for userlink in UserLinks:
            User = user(session, userlink)
            ws.write(row, 0, User.name())
            try:
                ws.write(row, 1, User.location())
            except:
                ws.write(row, 1, 'no data')
            try:
                ws.write(row, 2, User.fans())
            except:
                ws.write(row, 2, 'no data')
            try:
                ws.write(row, 3, User.agree())
            except:
                ws.write(row, 3, 'no data')
            try:
                ws.write(row, 4, User.answered())
            except:
                ws.write(row, 4, 'no data')
            try:
                ws.write(row, 5, User.raised())
            except:
                ws.write(row, 5, 'no data')
            try:
                ws.write(row, 6, User.goodat())
            except:
                ws.write(row, 6, 'no data')
            try:
                ws.write(row, 7, User.job())
            except:
                ws.write(row, 7, 'no data')
            try:
                ws.write(row, 8, User.watching())
            except:
                ws.write(row, 8, 'no data')
            print '%d' % row
            row += 1

    wb.save('zhihu.xlsx')
