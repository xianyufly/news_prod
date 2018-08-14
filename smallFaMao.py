import os,time,datetime
import requests
import urllib
import json
import re
import random
import gzip
import io
from thirdFileUtil import imgReg
from thirdFileUtil import ipPool

from requests.packages.urllib3.exceptions import InsecureRequestWarning
#HTML解析库
from lxml import etree

#数据库操作库
import pymysql
#ORM 框架
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#导入model
from models.TArticle import TArticle
from models.TSubject import TSubject
#模拟浏览器框架
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
# 导入支持双击操作的模块
from selenium.webdriver import ActionChains
import env
#系统变量
_env=env.initEnv()


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
pymysql.install_as_MySQLdb()



'''[summary]
代理请求
[description]
'''

def proxyRequest(url,header,data):
	targeturl="http://www.xiaofamao.com/"
	flag = True
	while flag:
		try :
			flag=False
			proxy_addr=ipPool.randomGetIp(targeturl)
			proxy = urllib.request.ProxyHandler({'http': proxy_addr,'https': proxy_addr})
			opener = urllib.request.build_opener(proxy, urllib.request.ProxyHandler)
			urllib.request.install_opener(opener)
			data = urllib.parse.urlencode(data).encode('utf-8')
			req = urllib.request.Request(url, data=data, headers=header,method = 'POST')
			response = urllib.request.urlopen(req)
			html=response.read().decode('UTF-8')
		except urllib.error.URLError as err:
			print(err)
			flag=True
	return html

# header ={ 		
# 	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
# 	"Accept-Language": "zh-CN,zh;q=0.9",
# 	"Cache-Control": "max-age=0",
# 	"Connection": "keep-alive",
# 	"Content-Length": "76",
# 	"Content-Type": "application/x-www-form-urlencoded",
# 	"Cookie": "UM_distinctid=16518c9b89956f-0da9efa946a0fc-6114147a-15f900-16518c9b89b7af; CNZZDATA1273363300=408979688-1533717260-%7C1533717260",
# 	"Host": "www.xiaofamao.com",
# 	"Origin": "http://www.xiaofamao.com",
# 	"Referer": "http://www.xiaofamao.com/",
# 	"Upgrade-Insecure-Requests": "1",
# 	"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
# }

# url="http://www.xiaofamao.com/result.php"

# data={
# 	"contents":"自信与自卑是两个极端，一般来说，我更愿意相信自卑之人，自卑之人知道自己的弱点，在做事情上会最大限度的规避错误，避免风险。而自信之人总是容易陷入盲目自信以及过度自信中去。极度自信者大多浅薄，你仔细推...",
# 	"xfm_uid":"0443e6a06583e46457ee2fc3a484ce14",
# 	"agreement":"on"
# }	

# html=proxyRequest(url,header,data)
# print(html)

chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('lang=zh_CN.utf-8')
targeturl="http://www.xiaofamao.com/"
proxy_addr=ipPool.randomGetIp(targeturl)
print(proxy_addr)
chrome_options.add_argument("--proxy-server=http://"+proxy_addr)
# chrome_options.add_argument("user-data-dir=C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data");
# chrome_options.add_extension("C:\\Users\\Administrator\\Downloads\\Set-Character-Encoding_v0.42.crx");
# 对应的chromedriver的放置目录
driver = webdriver.Chrome(executable_path=(_env["chrome_driver_path"]), chrome_options=chrome_options)
driver.get("http://www.xiaofamao.com/")
