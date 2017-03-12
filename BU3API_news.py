#coding:utf-8
import requests
import sys
from bs4 import BeautifulSoup
import bs4
import re
subsection={
        'zhxw':'综合新闻',
        'bhzt':'专题新闻',
        'xyfc':'校园风采',
        'kjzx':'科教在线',
        'mtbh':'媒体北航',
        'wyyd':'文艺园地',
        'xytz':'信息公告',
        'xswh':'学术及文化活动'}
def News_get_url(subsection,pagenum=''):#subsection控制新闻子页面。可选参数pagenum表明抓取的页数,注意从0开始编号
    out=[]
    url='http://news.buaa.edu.cn/'+subsection+'/index'+str(pagenum)+'.htm'
    page=requests.get(url)
    page.encoding='utf-8' #这句非常非常非常重要
    bsobj=BeautifulSoup(page.text,'lxml')
    tag_list=bsobj.find_all(class_='listleftop1 auto')
    for  div in tag_list:
        if isinstance(div,bs4.element.Tag):
            for h2 in div:
                if isinstance(h2,bs4.element.Tag) and h2.name=='h2':
                    for a in h2:
                        if isinstance(a,bs4.element.Tag) and a.name=='a':
                            out.append('http://news.buaa.edu.cn/'+subsection+'/'+a['href'])
    return out
class News_page():
    def __init__(self,url):
        page_temp=requests.get(url)
        page_temp.encoding='utf-8'
        self.bsobj=BeautifulSoup(page_temp.text,'lxml')
    def get_info(self):#返回一个列表，分别是标题，点击量和发布日期
        out=[]
        tag=self.bsobj.find(class_='newslefttit auto')
        for title in tag.children:
            if isinstance(title,bs4.element.Tag):
                out.append(title.string) #得到标题
        tag=self.bsobj.find(class_='ri')
        for item in tag:
            if isinstance(item,bs4.element.Tag): #获取点击量
                temp=requests.get(item['src'])
                pattern=re.compile("write.'(.*)'.")
                count=re.search(pattern,temp.text.encode('utf-8'))
                out.append(int(count.group(1)))#得到点击量
            else :
                pattern=re.compile("(\d\d\d\d-\d\d-\d\d)")
                date=re.search(pattern,item)
                if date!=None:
                    out.append(date.group(0))
        return out
    def get_page(self): #返回新闻内容
        tag=self.bsobj.find(class_='newsleftconbox auto')
        return tag.prettify()
