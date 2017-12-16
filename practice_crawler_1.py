#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class QSBK:

	def __init__(self, url):
		self.pageIndex = 1
		user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
		self.headers = { 'User-Agent' : user_agent}
		self.url = url
		self.storise = []
		self.enable = False

	def getPage(self, pageIndex):
		try:
			requestUrl = self.url + str(pageIndex)
			request = urllib2.Request(requestUrl, headers = self.headers)
			response = urllib2.urlopen(request)
			pageCode = response.read().decode('utf-8')
			# print pageCode
			# fil = open('tp.txt', 'w')
			# fil.write(pageCode)
			# fil.close()

			return pageCode

		except urllib2.URLError, e:
			if hasattr(e, 'reason'):
				print '请求失败，失败原因：',e.reason
				return None

	def getPageItems(self, pageIndex):
		pageCode = self.getPage(pageIndex)
		# outFile = open('tp.txt', 'r')
		# pageCode = outFile.read
		print 'get page code !!!'
		if not pageCode:
			print 'page load failed !!!'
			return None

		print 'get page success !!!'
		pattern = re.compile('<div.*?class="author.*?>.*?<a.*?</a>.*?<a.*?>(.*?)</a>.*?<div.*?class'+'="content".*?title="(.*?)">(.*?)</div>(.*?)<div class="stats.*?class="number">(.*?)</i>', re.S)
		items = re.findall(pattern, pageCode)
		print 'items -------'
		print items
		pageStories = []
		# file = open('tmp.txt', 'w')
		for item in items:
			# leng = len(item)
			# print 'item length : ' + str(leng)
			# ite = [item[0].strip(), item[1].strip(), item[2].strip(), item[4].strip()]
			# itemContent = '**************************\n' + 	str(ite) + '**************************\n'
			# file.write(itemContent)
			# leng = len(item)
			haveImg = re.search('img', item[3])
			if not haveImg:
				ite = [item[0],strip(), item[1].strip(), item[2].strip(), item[4].strip()]
				pageStories.append(ite)
			# 	print ite
		# file.close()
		return pageStories

	def loadPage(self):
		if self.enable == True:
			if len(self.storise) < 2:
				pageStories = self.getPageItems(self.pageIndex)
				if pageStories:
					self.storise.append(pageStories)
					self.pageIndex += 1

	def getOneStory(self, pageStories, page):
		for story in pageStories:
			inputStr = raw_input()
			self.loadPage()
			if inputStr == 'q':
				self.enable = False
				return
			print u"第%d页\t发布人:%s\t发布时间:%s\n%s\n赞:%s\n" % (page,story[0],story[1],story[2],story[3])

	def start(self):
		print 'reading QB, q to exit'
		self.enable = True
		self.loadPage()
		nowPage = 0
		while self.enable:
			if len(self.storise) > 0:
				pageStories = self.storise[0]
				nowPage += 1
				del self.storise[0]
				self.getOneStory(pageStories, nowPage)

url = 'http://www.qiushibaike.com/hot/page/'
qsbk = QSBK(url)
qsbk.start()
# qsbk.getPage(1)
# qsbk.getPageItem(1)