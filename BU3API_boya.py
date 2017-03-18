# -*-coding:utf-8 -*-
from bs4 import BeautifulSoup
import bs4
import requests
import re
import os

#博雅课程的网站不知道用了什么前端黑科技
class BoYa_Notice():
    def __init__(self,url):
        try:
            page_temp=requests.get(url)
            self.bsobj=BeautifulSoup(page_temp.text,'lxml')
        except:
            print "ERROR:打开页面错误"
    def get_info(self):
        out=[]
        tag=self.bsobj.find(id='lbl_newstitle')#标题
        out.append(tag.string)
        tag=self.bsobj.find(id='lbl_visit')#点击量
        out.append(tag.string)
        tag=self.bsobj.find(id='lbl_date')#时间
        out.append(tag.string)
        return out
    def get_page(self):
        tag=self.bsobj.find(class_='lbl_content')
        return tage.prettify()
def BoYa_get_url(subsection):#返回课程预告和课程新闻两个模块的首页新闻链接列表
    out=[]
    url_dict={
            'kcyg':'courseForecast.aspx',#课程预告
            'kcxw':'NewsList.aspx'#课程新闻
            }
    page_temp=requests.get('http://bykt.buaa.edu.cn/'+url_dict[subsection])
    page_temp.encoding='utf-8'
 
    bsobj=BeautifulSoup(page_temp.text,'lxml')
    tag=bsobj.find(id="UpdatePanel1")
    for child in tag.descendants:
        if isinstance(child,bs4.element.Tag):
            if child.name=='tr':
                for td in child:
                    if isinstance(td,bs4.element.Tag) and td.name=='td':
                        for a in td:
                            if isinstance(a,bs4.element.Tag) and a.name=='a':
                                if a.has_attr('href'):
                                    if  a['href'].find('javascript')==-1:
                                        out.append('http://bykt.buaa.edu.cn/'+a['href'])
    return out
        
    

        

    
    


        
        
        




        
        
        

            
            
   
