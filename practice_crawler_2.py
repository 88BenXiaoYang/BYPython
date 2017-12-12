#参考资料：http://cuiqingcai.com/993.html
# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import sys

reload(sys)
sys.setdefaultencoding('utf8')

#处理页面标签类
class Tool:
    #去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        #strip()将前后多余内容删除
        return x.strip()

#百度贴吧爬虫类
class BDTB:

    #初始化，传入基地址，是否只看楼主的参数
    def __init__(self,baseUrl,seeLZ,contentFile):
        self.baseURL = baseUrl
        self.seeLZ = '?see_lz='+str(seeLZ)
        self.contentFile = open(contentFile, 'w')
        self.filePath = contentFile
        self.tool = Tool()
        self.totalContentNum = 0

    #传入页码，获取该页帖子的代码
    def getPage(self,pageNum):
        try:
            url = self.baseURL+ self.seeLZ + '&pn=' + str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            # conStr = response.read()
            # self.contentFile.write(conStr)
            return response.read().decode('utf-8')
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"连接百度贴吧失败,错误原因",e.reason
                return None
        finally:
            self.contentFile.close()

    def getTitle(self):
        page = self.getPage(1)
        regularStr = '<h3 class="core_title_txt.*?>(.*?)</h3>'
        pattern = re.compile(regularStr, re.S)
        result = re.search(pattern, page)

        if result:
            print 'search success !!!'
            print result.group(1)
        else:
            print 'search fail !!!'
            return None

    def getPageNum(self):
        page = self.getPage(1)
        regularStr = '<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>'
        pattern = re.compile(regularStr, re.S)
        result = re.search(pattern, page)

        if result:
            print 'pageNum :'
            print result.group(1).strip()
        else:
            print 'getPageNum fail !!!'

    def getContent(self):
        page = self.getPage(1)
        regularStr = '<div id="post_content_.*?>(.*?)</div>'
        pattern = re.compile(regularStr, re.S)
        result = re.findall(pattern, page) # result is kind of list

        if result:
            self.contentFile = open(self.filePath, 'w')
            for eachItem in result:
                self.totalContentNum += 1
                contentStr = self.tool.replace(eachItem)
                conStr = '---------------\n' + contentStr + '\n---------------\n'
                self.contentFile.write(conStr)

            self.contentFile.close()
            # print 'tottal_content_num:' + str(self.totalContentNum)
            # print id(self.totalContentNum)
        else:
            print 'get content fail !!!' 

print u"请输入帖子代号"
baseURL = 'http://tieba.baidu.com/p/' + str(raw_input(u'http://tieba.baidu.com/p/'))
seeLZ = raw_input("是否只获取楼主发言，是输入1，否输入0\n")
floorTag = raw_input("是否写入楼层信息，是输入1，否输入0\n")
bdtb = BDTB(baseURL,seeLZ,floorTag)

"""
baseURL = 'http://tieba.baidu.com/p/3138733512'
contentFile = 'content.txt'
bdtb = BDTB(baseURL,1,contentFile)
# bdtb.getPage(1)
# bdtb.getTitle()
# bdtb.getPageNum()
bdtb.getContent()
"""