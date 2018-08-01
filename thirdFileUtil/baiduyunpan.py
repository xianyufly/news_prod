"""[summary]
微云服务器--上传
[description]
"""
import os,time
import requests
import urllib
import json
import re
import random


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
# 导入支持双击操作的模块
from selenium.webdriver import ActionChains

#百度账号
userName="yong0402"
password="xian0402"

#全局变量
BDUSS,STOKEN="",""
bdstoken=""

'''
初始化driver
'''


def initChromeDriver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    # 对应的chromedriver的放置目录
    driver = webdriver.Chrome(executable_path=(
        r'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe'), chrome_options=chrome_options)
    return driver

'''
百度云盘--初始化
参数

返回

'''
def init():
	global BDUSS,STOKEN,bdstoken
	try :
		driver=initChromeDriver()
		#打开百度网盘进行账号登陆
		url="https://pan.baidu.com/"
		driver.get(url)
		flag = True
		while flag:
			try :
				temp=driver.find_element_by_id("TANGRAM__PSP_4__footerULoginBtn")
				flag= False
			except :
				flag= True
			finally :
				time.sleep(0.1)
		# 登陆面板 TANGRAM__PSP_4__footerULoginBtn
		login_panel=driver.find_element_by_id("TANGRAM__PSP_4__footerULoginBtn")
		login_panel.click()
		# 账号 TANGRAM__PSP_4__userName
		text_userName=driver.find_element_by_id("TANGRAM__PSP_4__userName")
		text_userName.send_keys(userName)
		# 密码 TANGRAM__PSP_4__password
		text_password=driver.find_element_by_id("TANGRAM__PSP_4__password")
		text_password.send_keys(password)
		time.sleep(0.1)
		# 登陆 
		btn_login_submit=driver.find_element_by_id("TANGRAM__PSP_4__submit")
		btn_login_submit.click()

		# 获取bdstoken
		flag = True
		reg=re.compile(r'\"bdstoken\":\"(.*?)\"')
		bdstoken=""
		while flag:
			try :
				bdstokenArray=reg.findall(driver.page_source)
				print("bdstoken:",bdstokenArray[0])
				bdstoken=bdstokenArray[0]
				flag= False
			except :
				flag= True
			finally :
				time.sleep(0.1)

		#获取网站cookie
		cookie=driver.get_cookies()

		'''
		返回cookie内容
		'''
		def getCookieByParam(cookieData,key,domain=""):
			val=""
			#初始化要获取的cookie
			for item in cookieData :
				if domain == "" and  item["name"]==key:
					val = item["value"]
				elif domain != "" and item["name"]==key and item["domain"]== domain:
					val = item["value"]
			return val
		BDUSS=getCookieByParam(cookie,'BDUSS','.baidu.com')
		STOKEN=getCookieByParam(cookie,'STOKEN','.pan.baidu.com')

		print("BDUSS:",BDUSS)
		print("STOKEN",STOKEN)
	finally :
		driver.quit()

'''[summary]
百度网盘--创建文件夹 
参数:
folderPath: 百度文件夹路径 例如: "/A_douyin/1.mp4"
返回:
成功 True OR False
[description]
'''
def createFolder(folderPath) :
	global BDUSS,STOKEN,bdstoken
	header = {
		"Accept": "application/json, text/javascript, */*; q=0.01",
		"Accept-Encoding": "gzip, deflate, br",
		"Accept-Language": "h-CN,zh;q=0.9",
		"Connection": "keep-alive",
		"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
		"Cookie": "BDUSS=%s; STOKEN=%s;" % (BDUSS,STOKEN),
		"Host": "pan.baidu.com",
		"Origin": "https://pan.baidu.com",
		"Referer": "https://pan.baidu.com/disk/home?",
		"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
		"X-Requested-With": "XMLHttpRequest"
	}
	data= {
		"path": folderPath,
		"isdir": "1",
		"block_list": "[]"
	}
	#创建文件夹
	API_CREATE_FOLDER = "https://pan.baidu.com/api/create?a=commit&channel=chunlei&web=1&app_id=250528&bdstoken="+bdstoken+"&logid=5656&clienttype=0"
	#请求接口
	result = requests.request('POST', API_CREATE_FOLDER,data=data, headers=header, verify=False)
	print(result.json())
	successBean = result.json();
	if successBean["errno"] == 0 :
		return True
	else :
		return False
'''[summary]
百度网盘--上传文件
参数:
baiduFilePath: 百度文件地址 例如: "/A_douyin/1.mp4"
localFilePath: 本地文件地址 例如: C:\\Users\\Administrator\\Desktop\\新建文件夹\\1.mp4
返回:
fs_id: 百度文件ID
[description]
'''
def uploadFile(baiduFilePath,localFilePath) :
	global BDUSS,STOKEN,bdstoken
	header = {
		"Accept": "application/json, text/javascript, */*; q=0.01",
		"Accept-Encoding": "gzip, deflate, br",
		"Accept-Language": "h-CN,zh;q=0.9",
		"Connection": "keep-alive",
		"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
		"Cookie": "BDUSS=%s; STOKEN=%s;" % (BDUSS,STOKEN),
		"Host": "pan.baidu.com",
		"Origin": "https://pan.baidu.com",
		"Referer": "https://pan.baidu.com/disk/home?",
		"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
		"X-Requested-With": "XMLHttpRequest"
	}
	data= {
		"path": baiduFilePath,
		"autoinit": "1",
		"block_list": "[\"5910a591dd8fc18c32a8f3df4fdc1761\"]",
		"local_mtime": "1509102995"
	}
	#上传文件前准备
	API_PRE_CREATE = "https://pan.baidu.com/api/precreate?channel=chunlei&web=1&app_id=250528&bdstoken="+bdstoken+"&logid=MTUzMDA2Mjc3NjYxNDAuNjg1MTUzNDE0MDY5MDQ3Ng==&clienttype=0&startLogTime=1530062776614"
	#请求接口
	result = requests.request('POST', API_PRE_CREATE,data=data, headers=header, verify=False)
	print(result.json())
	successBean = result.json();
	if successBean["errno"] == 0 :
		header2 = {
			"Accept": "*/*",
			"Accept-Encoding": "gzip, deflate, br",
			"Accept-Language": "zh-CN,zh;q=0.9",
			"Connection": "keep-alive",
			"Cookie": "BDUSS=%s; STOKEN=%s;" % (BDUSS,STOKEN),
			"Host": "c3.pcs.baidu.com",
			"Origin": "https://pan.baidu.com",
			"Referer": "https://pan.baidu.com/disk/home?errno=0&errmsg=Auth%20Login%20Sucess&&bduss=&ssnerror=0&traceid=",
			"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
		}
		uploadid=successBean["uploadid"]
		path=successBean["path"]
		#上传文件 
		API_UPLOAD_SUPERFILE2="https://c3.pcs.baidu.com/rest/2.0/pcs/superfile2?method=upload&app_id=250528&channel=chunlei&clienttype=0&web=1&BDUSS="+BDUSS+"&logid=MTUzMDA2MjczMzE1MzAuMjAzMzMyMzg2NTM0NzEzNjQ=&path="+path+"&uploadid="+uploadid+"&uploadsign=0&partseq=0"
		files={
			"file":open(localFilePath, "rb")
		}
		result = requests.request('POST', API_UPLOAD_SUPERFILE2,files=files, headers=header2, verify=False)
		print(result.json())
		successBean = result.json();
		if successBean["md5"] :
			md5=successBean["md5"]
			fsize=os.path.getsize(localFilePath)
			#创建文件记录
			data= {
				"path": path,
				"size": fsize,
				"uploadid": uploadid,
				"block_list": "[\""+md5+"\"]",
				"local_mtime": int(time.time())
			}
			#上传文件前准备
			API_RECORD_FILE = "https://pan.baidu.com/api/create?isdir=0&rtype=1&channel=chunlei&web=1&app_id=250528&bdstoken="+bdstoken+"&logid=MTUzMDA2Mjc3NzMzNjAuNzk1MjQxMTgxNTkyMTcyMw==&clienttype=0"
			#请求接口
			result = requests.request('POST', API_RECORD_FILE,data=data, headers=header, verify=False)
			print(result.json())
			successBean = result.json();
			if successBean["errno"] == 0 :
				return successBean["fs_id"]
			else :
				return ""
		else :
			return ""
	else :
		return ""
'''[summary]
百度网盘获取资源的分享地址
参数:
fs_id:百度的文件ID
shorturl: 百度分享地址
pwd: 百度分享密码
返回:
[description]
'''
def getShareUrl(fs_id) :
	global BDUSS,STOKEN,bdstoken
	header = {
		"Accept": "application/json, text/javascript, */*; q=0.01",
		"Accept-Encoding": "gzip, deflate, br",
		"Accept-Language": "h-CN,zh;q=0.9",
		"Connection": "keep-alive",
		"Content-Length": "38",
		"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
		"Cookie": "BDUSS=%s; STOKEN=%s;" % (BDUSS,STOKEN),
		"Host": "pan.baidu.com",
		"Origin": "https://pan.baidu.com",
		"Referer": "https://pan.baidu.com/disk/home?",
		"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
		"X-Requested-With": "XMLHttpRequest"
	}
	pwd=''.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a'], 4))
	data= {
		"fid_list": "["+str(fs_id)+"]",
		"schannel": "4",
		"channel_list": "[]",
		"period": "0",
		"pwd": pwd
	}
	#创建文件夹
	API_SHARE_URL = "https://pan.baidu.com/share/set?channel=chunlei&clienttype=0&web=1&channel=chunlei&web=1&app_id=250528&bdstoken="+bdstoken+"&logid=MTUzMDA4NDA2NzgyMDAuMDgxNDU4MjU5NjQ5OTkwNjU=&clienttype=0"
	#请求接口
	result = requests.request('POST', API_SHARE_URL,data=data, headers=header, verify=False)
	print(result.json())
	successBean = result.json();
	if successBean["errno"] == 0 :
		return successBean["shorturl"],pwd
	else :
		return "",""
'''[summary]
百度云盘文件删除
参数:
baiduFilePath: 百度文件路径 例如: "/A_douyin/1.mp4"
返回:
操作状态
[description]
'''
def deleteFile(baiduFilePath) :
	global BDUSS,STOKEN,bdstoken
	header = {
		"Accept": "application/json, text/javascript, */*; q=0.01",
		"Accept-Encoding": "gzip, deflate, br",
		"Accept-Language": "h-CN,zh;q=0.9",
		"Connection": "keep-alive",
		"Content-Length": "38",
		"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
		"Cookie": "BDUSS=%s; STOKEN=%s;" % (BDUSS,STOKEN),
		"Host": "pan.baidu.com",
		"Origin": "https://pan.baidu.com",
		"Referer": "https://pan.baidu.com/disk/home?",
		"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
		"X-Requested-With": "XMLHttpRequest"
	}
	data= {
		"filelist": "[\""+baiduFilePath+"\"]"
	}
	#创建文件夹
	API_SHARE_URL = "https://pan.baidu.com/api/filemanager?opera=delete&async=2&onnest=fail&channel=chunlei&web=1&app_id=250528&bdstoken="+bdstoken+"&logid=MTUzMDA4NjE4Nzk2MjAuOTU3MzQwMDYwODcwMTIxMg==&clienttype=0"
	#请求接口
	result = requests.request('POST', API_SHARE_URL,data=data, headers=header, verify=False)
	print(result.json())
	successBean = result.json();
	if successBean["errno"] == 0 :
		return True
	else :
		return False
# try :
# 	#创建文件夹
# 	#createFolder(BDUSS, STOKEN , bdstoken , "/A_ceshi/B_ceshi")
# 	# #上传文件
# 	# baiduFilePath="/A_douyin/1.mp4"
# 	# localFilePath="C:\\Users\\Administrator\\Desktop\\新建文件夹\\1.mp4"
# 	# fs_id=uploadFile(BDUSS, STOKEN , bdstoken ,baiduFilePath ,localFilePath)
# 	#获取分享文件地址
# 	# shareUrl,pwd=getShareUrl(BDUSS, STOKEN , bdstoken ,fs_id)
# 	# print("分享地址:"+shareUrl+",分享密码:"+pwd)
# 	# deleteFile(BDUSS, STOKEN , bdstoken ,baiduFilePath)
# finally :
# 	print("关闭浏览器")
# 	driver.quit()
