#!/usr/bin/python
# -*- coding: utf-8 -*-

ori = open('ori.txt', 'r')
des = open('des.txt', 'w')

content = ori.readlines()

for eachLine in content:
	lineStr = eachLine.strip()
	if ':' in lineStr:
		ind = lineStr.index(':')
		subStr = lineStr[:ind]
		if '"'in subStr:
			finallyStr = subStr.lstrip('"').rstrip('"')
			propertyStr = '@property (nonatomic,  copy) NSString *' + finallyStr + ';\n'
			des.write(propertyStr)

ori.close()
des.close()