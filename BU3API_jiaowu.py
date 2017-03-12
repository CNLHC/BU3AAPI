# -*-coding:utf-8 -*-
from bs4 import BeautifulSoup
import bs4
import requests
import re
import os
class JiaoWu_Notice():#该类的对象分别对应不同的新闻
    def __init__(self,url):
        notice_url=url
        try:
            page_temp=requests.get(notice_url)
            self.bsobj=BeautifulSoup(page_temp.text,'lxml')
        except:
            print "ERROR(xwid=%4d):打开页面错误"%xwid
    def get_info(self):#该方法得到一个有三项的列表，分别存储标题，日期和发布单位 
        '''Input a bsobj of News page
        Return a list:
        first item is title
        second item is date
        third item is department '''
        out=[]
        tag=self.bsobj.find(class_="search_con mt20 text_cen font18 blue LH36 font_hei")
        out.append(tag.string)
        tag=tag.next_sibling.next_sibling
        str_temp=tag.string.strip().split(' ')
        out.append((str_temp[0].split(':'))[-1])
        out.append((str_temp[-1].split(':'))[-1])
        return out
    def get_page(self):
        ''' Get a copy of News,the copy will be named as '[xwid].html'and stored in the './.NoticeCopy/'''
        tag=self.bsobj.find(class_="search_con mt20 LH20 fontcolor")
        return tag.prettify()


#note:北航教务的网站是动态生成的
#获得列表需要用post方法提交一份表单
#其中比较关键的参数是fcdTab:
#02:通知公告
#o3:新闻快讯
#05:下载专区
#08:公式专区
#06:服务中心

def JiaoWu_get_url(subsection='tzgg',pagenum='1'):
    out=[]
    post_dict={
            'tzgg':'02',
            'xwkx':'03',
            'xzzq':'05',
            'fwzx':'06',
            'gszq':'08',
            }
    payload={'fcdTab':post_dict[subsection],
             'pageNo':str(pagenum),
             'pageSize':'10', 
             'cddmTab':'0201',
             'xsfsTab':'2'   ,
             'pageCount':1000,  #这里的PageCount指最大数量，只要别小于pageNo就可以正常工作
                                #要得到这个的精确值需要解析js
            }
    index = requests.post("http://jiaowu.buaa.edu.cn/bhjwc2.0/index/newsList.do",params=payload)
    bsobj=BeautifulSoup(index.text,'lxml')
    tag_list= bsobj.find_all(class_='text')
    for child in tag_list:
        if isinstance(child,bs4.element.Tag):
            pattern=re.compile("onNewsView.'(.*?)',")
            xwid=re.search(pattern,child.prettify())
            out.append('http://jiaowu.buaa.edu.cn/bhjwc2.0/index/newsView.do?xwid='+xwid.group(1))
    return out

        
