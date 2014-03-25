#-*-coding:utf-8-*-
#知乎的爬虫，用于搜集信息
import requests
from bs4 import BeautifulSoup
#from celery.task import task

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
    '''
    def vote(self):
        #赞同数 2,2
        lst = self.soup.find_all('a', {'class':'zm-item-vote-count'})
        res = []
        for item in lst:
            vote = item.text
            res.append(vote)   
        return res
    '''

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
        ret = ', '.join(res)
        return ret
        
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
        lst = self.soup.find_all('a', {'class':'answer-date-link meta-item'}, limit=10)
        for item in lst:
            text = item.text
            res.append(text)
        return res

    def wordcount(self):
        #回答字数 2,1
        res = []
        lst = self.soup.find_all('div', {'class':'zm-editable-content'}, limit=12)
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

    def agree(self):
        #点赞数 2,2
        res = []
        lst = self.soup.find_all('button', {'class':'up'}, limit=10)
        for item in lst:
            res.append(item.find_all('span')[1].text)
        return res
        
    def isunknown(self):
        #是否匿名 2,5
        #匿名值为1,否则为0
        res = []
        lst = self.soup.find_all('h3', {'class':'zm-item-answer-author-wrap'}, limit=10)
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
        lst = self.soup.find_all('div', {'class':'zm-editable-content'}, limit=12)
        lst.pop(0); lst.pop(0)
        for item in lst:
            if (item.find('img', recursive=True)):
                res.append(1)
            else:
                res.append(0)
        return res

    def getUser(self):
        #获取用户主页地址链接
        res = []
        lst = self.soup.find_all('a', {'class':'zm-item-link-avatar'}, limit=10)
        for item in lst:
            link = item['href'].encode('utf-8')
            link = ''.join(['http://www.zhihu.com', link])
            res.append(link)
        return res

class user:
    def __init__(self, session, url):
        self.r = session.get(url)
        self.soup = BeautifulSoup(self.r.text, 'html.parser') 
        self.url = url

    def name(self):
        #用户名 3,1
        urlist = self.url.split('/')
        uname = urlist[-1]
        return uname

    def location(self):
        #居住地 3,2
        try:
            res = self.soup.find('span', {'class':'info-wrap'})
            res = res.span['title']
            return res
        except KeyError:
            res = "no data"
            return res

    def fans(self):
        #粉丝数 3,3
        res = self.soup.find('div', {'class':'zm-profile-side-following zg-clear'})
        res = res.find_all('a')
        res = res[1].strong.text
        return res

    def agree(self):
        #获得赞同数 3,4
        res = self.soup.find('span', {'class':'zm-profile-header-user-agree'})
        res = res.strong.text
        return res

    def answered(self):
        #回答过问题数 3,5
        res = self.soup.find_all('span', {'class':'num'})
        res = res[1].text
        return res

    def raised(self):
        #提问数 3,6
        res = self.soup.find_all('span', {'class':'num'})
        res = res[0].text
        return res

    def goodat(self):
        #擅长话题 3,7
        res = self.soup.find_all('h3', {'class':'zg-gray-darker'})
        lst = []
        for item in res:
            lst.append(item.text)
        return lst

    def job(self):
        #职业 3,8
        try:
            res = self.soup.find('span', {'class':'business'})
            business = res['title']
            return business
        except KeyError:
            res = 'no data'
            return res

    def watching(self):
        #关注话题数 3,9
        lst = []
        res = self.soup.find_all('a', {'class':'zg-link-litblue'})
        for item in res:
            try:
                lst.append(item.strong.text)
            except AttributeError:
                continue
        num = lst[1].split()[0]
        return num

