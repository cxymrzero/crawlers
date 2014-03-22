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

class get_question:
    def __init__(self, session, url):
        #self.s = session
        #self.url = url
        self.r = session.get(url)
        self.soup = BeautifulSoup(self.r.text, 'html.parser') 
        #要加上html.parser，不同解析器能解析出的标签不同

    def question(self):
        #获取问题
        lst = self.soup.find_all('a', {'class':'question_link'})
        res = []
        for item in lst:
            question = item.text
            res.append(question)
        return res

    def count(self):
        #回答人数
        pass
    def type(self):
        #话题类别
        pass
    def watched(self):
        #关注人数
        pass

class get_answer:
    pass

class get_user:
    pass
