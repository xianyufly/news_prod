#!/usr/bin/python
# -*- coding: utf-8 -*-
'''[summary]
模块
正则替换图片
[description]
'''
import re
import time
import os
import urllib
import shutil
import sys
sys.path.append("..")
from thirdFileUtil import weiyun

# dir_name 文件夹名称 dir_key 微云文件夹key p_dir_key 微云父文件夹key文件
dir_name, dir_key, p_dir_key,account_str = "", "", "",""

'''[summary]
初始化环境
[description]
'''
def initEnv(p_dir_name):
	global dir_name, dir_key, p_dir_key,account_str
	dir_name = str(time.time())
	begTime = time.time()
	account_str=weiyun.init()
	endTime = time.time()
	print("微云初始化时间:%s"%(str(endTime-begTime)))
	rootDirKey, mainDirKey = weiyun.getRootAndMainDirKey()
	# 先在主文件夹下创建父文件夹
	begTime = time.time()
	dir_key, pdir_key = weiyun.wy_diskDirCreate(
	    mainDirKey, rootDirKey, p_dir_name)
	endTime = time.time()
	print("父文件夹时间:%s"%(str(endTime-begTime)))
 	# 再在父文件夹下创建文章文件夹
	begTime = time.time()
	dir_key, p_dir_key = weiyun.wy_diskDirCreate(dir_key, pdir_key, dir_name)
	endTime = time.time()
	print("子文件夹时间:%s"%(str(endTime-begTime)))
	return dir_name, dir_key, p_dir_key,account_str

def regSuffix(url):
	result=re.search(r'wx_fmt=(.*?)&',url)
	if result == None :
		result=re.search(r'wx_fmt=(.*?)$',url)
	r_str=""
	try :
		r_str=result.group(1)
		if(r_str=='other'):
			r_str="jpeg"
	except Exception as err:
		r_str="jpeg"
	return r_str

def switchSrc(matched):
	global dir_name, dir_key, p_dir_key
	img = matched.group("img")
	src = matched.group("src")
	dataSrc = matched.group("dataSrc")
	# 下载文件到本地文件夹
	# 图片下载文件夹
	workfolder = os.getcwd()
	aimfolder = workfolder+"/temp/"+str(int(time.time()))
	if os.path.exists(aimfolder) != True:
	    # 创建文件夹
	    os.makedirs(aimfolder)
	imgName="img_"+str(int(time.time()))
	#
	#正则处理出图片后缀
	tempImg=aimfolder+"/"+imgName+"."+regSuffix(dataSrc)
	# begTime = time.time()
	urllib.request.urlretrieve(dataSrc, tempImg)
	# endTime = time.time()
	# print("下载文件时间:%s"%(str(endTime-begTime)))
	# 上传图片到微云
	# begTime = time.time()
	file_id, filename=weiyun.wy_fileUpload(dir_key,p_dir_key,tempImg)
	# endTime = time.time()
	# print("上传文件到微云时间:%s"%(str(endTime-begTime)))
	# begTime = time.time()
	share_url=weiyun.wy_shareUrl(dir_key,file_id, filename)
	# endTime = time.time()
	# print("生成分享地址时间:%s"%(str(endTime-begTime)))
	# begTime = time.time()
	if share_url != "" :
		aim_url=weiyun.wy_filePath(share_url,"img")
	else :
		aim_url="https://www.17sobt.com?error=100"
	aim_url=aim_url+"&pdir_key="+dir_key+"&file_id="+file_id+"&account_str="+account_str
	# endTime = time.time()
	# print("生成最终地址时间:%s"%(str(endTime-begTime)))
	shutil.rmtree(aimfolder)
	aimSrc = aim_url
	img=img.replace(src,aimSrc)
	img=img.replace(dataSrc,aimSrc)
	return img

def regReplaceImgSrc(content):
	weiyun.initWebDriver()
	newStr = re.sub(
	    r"(?P<img><img [^>]*data-src=[\'\"](?P<dataSrc>[^\'\"]+)[^>]* [^>]*src=[\'\"](?P<src>[^\'\"]+)[^>]*?>)", switchSrc, content)
	newStr = regReplaceBackImg(newStr)
	#退出WebDriver浏览器
	weiyun.quitWebDriver()
	return newStr

def swithchBack(matched):
	global dir_name, dir_key, p_dir_key
	img = matched.group("style")
	src = matched.group("src")
	dataSrc = src
	# 下载文件到本地文件夹
	# 图片下载文件夹
	workfolder = os.getcwd()
	aimfolder = workfolder+"/temp/"+str(int(time.time()))
	if os.path.exists(aimfolder) != True:
	    # 创建文件夹
	    os.makedirs(aimfolder)
	imgName="img_"+str(int(time.time()))
	#正则处理出图片后缀
	tempImg=aimfolder+"/"+imgName+"."+regSuffix(dataSrc)
	urllib.request.urlretrieve(dataSrc, tempImg)
	file_id, filename=weiyun.wy_fileUpload(dir_key,p_dir_key,tempImg)
	share_url=weiyun.wy_shareUrl(dir_key,file_id, filename)
	if share_url != "" :
		aim_url=weiyun.wy_filePath(share_url,"img")
	else :
		aim_url="https://www.17sobt.com?error=100"
	aim_url=aim_url+"&pdir_key="+dir_key+"&file_id="+file_id+"&account_str="+account_str
	shutil.rmtree(aimfolder)
	aimSrc = aim_url
	img=img.replace(src,aimSrc)
	return img
def regReplaceBackImg(content):
	newStr = re.sub(
	    r"(?P<style>style=[\'\"][^\'\"]*background-image: url\(&quot;(?P<src>[^\(\)\"\']+)&quot;\)[^\'\"]*?[\'\"])", swithchBack, content)
	return newStr
def uploadImgByUrl(imgUrl,dir_name, dir_key, p_dir_key):
	weiyun.initWebDriver()
	workfolder = os.getcwd()
	aimfolder = workfolder+"/temp/"+str(int(time.time()))
	if os.path.exists(aimfolder) != True:
	    # 创建文件夹
	    os.makedirs(aimfolder)
	imgName="img_"+str(int(time.time()))
	tempImg=aimfolder+"/"+imgName+"."+regSuffix(imgUrl)
	# begTime = time.time()
	urllib.request.urlretrieve(imgUrl, tempImg)
	# endTime = time.time()
	# print("下载文件时间:%s"%(str(endTime-begTime)))
	# 上传图片到微云
	# begTime = time.time()
	file_id, filename=weiyun.wy_fileUpload(dir_key,p_dir_key,tempImg)
	# endTime = time.time()
	# print("上传文件到微云时间:%s"%(str(endTime-begTime)))
	# begTime = time.time()
	share_url=weiyun.wy_shareUrl(dir_key,file_id, filename)
	# endTime = time.time()
	# print("生成分享地址时间:%s"%(str(endTime-begTime)))
	# begTime = time.time()
	print("封面地址:"+share_url)
	if share_url != "" :
		aim_url=weiyun.wy_filePath(share_url,"img")
	else :
		aim_url= ""
	# endTime = time.time()
	# print("生成最终地址时间:%s"%(str(endTime-begTime)))
	shutil.rmtree(aimfolder)
	weiyun.quitWebDriver()
	aimSrc = aim_url
	return aimSrc

if __name__ == '__main__':
    content = '<section class="" powered-by="xiumi.us" style="box-sizing: border-box;"><section style="box-sizing: border-box;"><section class="" powered-by="xiumi.us" style="box-sizing: border-box;"><section style="font-size: 58px;text-align: center;box-sizing: border-box;"><section style="margin: auto;box-sizing: border-box;display: inline-block;vertical-align: bottom;width: 3em;height: 3em;border-radius: 100%;background-position: 100% 0%;background-repeat: no-repeat;background-size: 150.754%;background-image: url(&quot;https://mmbiz.qpic.cn/mmbiz_jpg/6nJRMH45vic3dibMyzDwwjtIe3iaaUVtW2ekQos7qoFQB6EvqnWzHRicm0JIjH8NDWd7ibkj0ARAmIQX9NDpaB1KBLQ/640?wx_fmt=jpeg&quot;);"></section></section></section></section><section style="text-align: center;box-sizing: border-box;"><span style="font-size: 16px;color: rgb(136, 136, 136);max-width: 100%;box-sizing: border-box !important;word-wrap: break-word !important;"></span><br></section><section style="text-align: center;box-sizing: border-box;"><strong><span style="font-size: 16px;color: rgb(136, 136, 136);max-width: 100%;box-sizing: border-box !important;word-wrap: break-word !important;">覃晔</span></strong></section></section>'
    temp=regReplaceBackImg(content)
    print()