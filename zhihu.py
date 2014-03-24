#-*-coding:utf-8-*-
#知乎的爬虫，用于搜集信息
import requests
from bs4 import BeautifulSoup

def login():
    #模拟登陆，并返回requests.session()对象记住登陆状态
    email = 'cxymrzero@gmail.com'
    password = 'jimchen'
    s = requests.session()
    data = {'email':email, 'password':password}
    s.post('http://www.zhihu.com/login', data) #POST数据到这里
    return s

class topic:
    def __init__(self, session, url):
        #self.s = session
        #self.url = url
        self.r = session.get(url)
        self.soup = BeautifulSoup(self.r.text, 'html.parser') 
        #要加上html.parser，不同解析器能解析出的标签不同

    def links(self):
        #获取当前页问题链接
        lst = self.soup.find_all('a', {'class':'question_link'})
        res = []
        for item in lst:
            link = item['href']
            link = ''.join(['http://www.zhihu.com', link])
            res.append(link)
        return res

    def question(self):
        #获取问题 1,1
        lst = self.soup.find_all('a', {'class':'question_link'})
        res = []
        for item in lst:
            question = item.text
            res.append(question)
        return res

    def vote(self):
        #赞同数 2,2
        lst = self.soup.find_all('a', {'class':'zm-item-vote-count'})
        res = []
        for item in lst:
            vote = item.text
            res.append(vote)
        return res

class answer:
    def __init__(self, session, url):
        self.r = session.get(url)
        self.soup = BeautifulSoup(self.r.text, 'html.parser') 

    def type(self):
        #话题类别 1,3
        res = []
        lst = self.soup.find_all('a', {'class':'zm-item-tag'})
        for item in lst:
            text = item.text.strip('\n') #去除话题两端的换行符
            res.append(text)
        return res
        
    def watched(self):
        #问题关注人数 1,4
        num = self.soup.find('div', {'class':'zh-question-followers-sidebar'}).div.a.text
        #注意是unicode对象
        return num

    def answerednum(self):
        #问题回答人数 1,2
        num = self.soup.find('h3', {'id':'zh-question-answer-num'})
        num = num['data-num']
        return num

    def time(self):
        #问题回答时间 2,3
        res = []
        lst = self.soup.find_all('a', {'class':'answer-date-link meta-item'}, limit=20)
        for item in lst:
            text = item.text
            res.append(text)
        return res

    def wordcount(self):
        #回答字数 2,1
        res = []
        lst = self.soup.find_all('div', {'class':'zm-editable-content'}, limit=22)
        lst.pop(0); lst.pop(0) #去除前两个空白部分
        #test = 0
        for item in lst:
            answerlen = len(item.text)
            #print test
            #print item.text
            #print answerlen
            res.append(answerlen)
            #test += 1
        return res
        
    def isunknown(self):
        #是否匿名 2,5
        #匿名值为1,否则为0
        res = []
        lst = self.soup.find_all('h3', {'class':'zm-item-answer-author-wrap'}, limit=20)
        for item in lst:
            try:
                item.a.text
                res.append(0)
            except AttributeError:
                res.append(1)
        return res

    def havePic(self):
        #有无图 2,4
        #有图为1,无图为0
        res = []
        lst = self.soup.find_all('div', {'class':'zm-editable-content'}, limit=22)
        lst.pop(0); lst.pop(0)
        for item in lst:
            if (item.find('img', recursive=True)):
                res.append(1)
            else:
                res.append(0)
        return res

class user:
    pass
