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
	aim_url=weiyun.wy_filePath(share_url,"img")
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
	#退出WebDriver浏览器
	weiyun.quitWebDriver()
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
	aim_url=weiyun.wy_filePath(share_url,"img")
	# endTime = time.time()
	# print("生成最终地址时间:%s"%(str(endTime-begTime)))
	shutil.rmtree(aimfolder)
	weiyun.quitWebDriver()
	aimSrc = aim_url
	return aimSrc