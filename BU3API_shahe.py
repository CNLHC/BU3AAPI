#coding:utf-8
import requests
import sys
from bs4 import BeautifulSoup
import bs4
import re
def News_get_url(pagenum=''):
    out=[]
    index='index'+pagenum
    url='http://shxq.buaa.edu.cn/tzgg/tzzl/'+index+'.htm'
    page=requests.get(url)
    page.encoding='utf-8' #这句非常非常非常重要
    bsobj=BeautifulSoup(page.text,'lxml')
    tag_list=bsobj.find(class_='news_list')
    for  a in tag_list.descendants:
        if isinstance(a,bs4.element.Tag):
            if a.has_attr('href'):
                out.append('http://shxq.buaa.edu.cn/tzgg/tzzl/'+a['href'])
    return out
class News_page():
    def __init__(self,url):
        page_temp=requests.get(url)
        page_temp.encoding='utf-8'
        self.bsobj=BeautifulSoup(page_temp.text,'lxml')
    def get_info(self):#返回一个列表，分别是标题和发布日期
        out=[]
        tag=self.bsobj.find(class_='article_tit clearfix')
        for title in tag.descendants:
            if isinstance(title,bs4.element.Tag) and title.name=='h3':
                out.append(title.string) #得到标题
            if isinstance(title,bs4.element.Tag) and title.name=='span' and title.string!=None:
                pattern=re.compile("(\d\d\d\d-\d\d-\d\d)")
                date=re.search(pattern,title.string)
                if date!=None:
                    out.append(date.group(1))
        return out
    def get_page(self): #返回新闻内容
        tag=self.bsobj.find(class_='article')
        return tag.prettify()
