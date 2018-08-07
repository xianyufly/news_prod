"""[summary]
搜狗微信公众号--爬虫
[description]
"""
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

''' [summary]
 解析搜狗文章地址
[description]
'''
def parserUrlHtml(driver,url) :
	# 新开一个窗口，通过执行js来新开一个窗口
	js='window.open(\"'+url+'\");'
	driver.execute_script(js)
	main_handle=driver.current_window_handle # 输出当前窗口句柄（百度）
	handles = driver.window_handles # 获取当前窗口句柄集合（列表类型）
	for handle in handles:# 切换窗口（切换到新开启页面
	    if handle!=main_handle:
	        driver.switch_to_window(handle)
	        break
	try:
	    js_content=driver.find_element_by_id("js_content")
	    content=js_content.get_attribute("outerHTML")
	except Exception as err:
		print("获取不到js_content")
		content=""
	finally :
		driver.close() #关闭当前窗口
		driver.switch_to_window(main_handle) #切换回主页面
	return content
'''[summary]
代理请求
[description]
'''

def proxyRequest(url,header):
	targeturl="http://weixin.sogou.com"
	flag = True
	while flag:
		try :
			flag=False
			proxy_addr=ipPool.randomGetIp(targeturl)
			proxy = urllib.request.ProxyHandler({'http': proxy_addr,'https': proxy_addr})
			opener = urllib.request.build_opener(proxy, urllib.request.ProxyHandler)
			urllib.request.install_opener(opener)
			req = urllib.request.Request(url, None, headers=header)
			response = urllib.request.urlopen(req)
			html=response.read().decode('UTF-8')
		except urllib.error.URLError as err:
			print(err)
			flag=True
	return html
	
	

def task():
	global _env
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	chrome_options.add_argument("--no-sandbox")
	chrome_options.add_argument('lang=zh_CN.utf-8')
	# chrome_options.add_argument("user-data-dir=C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data");
	# chrome_options.add_extension("C:\\Users\\Administrator\\Downloads\\Set-Character-Encoding_v0.42.crx");
	# 对应的chromedriver的放置目录
	driver = webdriver.Chrome(executable_path=(
	    _env["chrome_driver_path"]), chrome_options=chrome_options)


	#链接数据库
	engine = create_engine(_env["python_sql"])
	DB_Session = sessionmaker(bind=engine)
	session = DB_Session()
	rows = session.query(TSubject).filter(TSubject.sub_status == '0').all()
	for row in rows :
		print(row.sub_name)
		page = 1
		subject = row.sub_code
		# while page<3 : 
		driver.get("http://www.baidu.com")
		# url = "http://weixin.sogou.com/pcindex/pc/"+subject+"/"+str(page)+".html"
		url = "http://weixin.sogou.com/pcindex/pc/"+subject+"/"+subject+".html"
		#url = "http://weixin.sogou.com/pcindex/pc/"+subject+"/"+"2.html"
		print("查询地址:"+url)
		page = page+1;
		header ={ 		
			'Host':'weixin.sogou.com',
			'Connection':'keep-alive',
			'Cache-Control':'max-age=0',
			'Accept': 'text/html, */*; q=0.01',
			'X-Requested-With': 'XMLHttpRequest',
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
			'Referer': 'http://weixin.sogou.com/',
			'Accept-Language': 'zh-CN,zh;q=0.8,ja;q=0.6'
		}
		# targeturl="http://weixin.sogou.com"
		# proxy_addr=ipPool.randomGetIp(targeturl)
		# proxy_addr="218.60.8.99:9999"
		# proxy = urllib.request.ProxyHandler({'http': proxy_addr,'https': proxy_addr})
		# opener = urllib.request.build_opener(proxy, urllib.request.ProxyHandler)
		# urllib.request.install_opener(opener)
		# req = urllib.request.Request(url, None, headers=header)
		# response = urllib.request.urlopen(req)
		# html=response.read().decode('UTF-8')
		html=proxyRequest(url,header)
		htmlDom = etree.HTML(html)
		news_li_array=htmlDom.xpath("//li")
		for item in news_li_array :
			try :
			#文章名称
				dom=item.xpath("./div[@class='txt-box']/h3/a/text()")
				title=""
				if len(dom)>0 :
					title=dom[0]
				#文章简介
				dom=item.xpath("./div[@class='txt-box']/p[@class='txt-info']/text()")
				memo=""
				if len(dom)>0 :
					memo=dom[0]
				#文章地址
				dom=item.xpath("./div[@class='txt-box']/h3/a/@href")
				articleUrl=""
				if len(dom)>0 :
					articleUrl=dom[0]
				#文章缩略图
				dom=item.xpath("./div[@class='img-box']/a/img/@src")
				smallPic=""
				if len(dom)>0 :
					smallPic=dom[0]
				#文章来源
				dom=item.xpath("./div[@class='txt-box']/div[@class='s-p']/a/text()")
				source=""
				if len(dom)>0 :
					source=dom[0]
				#文章发布时间
				dom=item.xpath("./div[@class='txt-box']/div[@class='s-p']/span[@class='s2']/@t")
				pubDate=""
				if len(dom)>0 :
					pubDate=dom[0]
				# print("标题:%s\n简介:%s\n文章地址:%s\n缩略图:%s\n发布时间:%s\n文章来源:%s"%(title,memo,articleUrl,smallPic,pubDate,source))
				num=session.query(TArticle).filter(TArticle.title==title).count()
				print(title)
				if num == 0 :
					#articleUrl="https://mp.weixin.qq.com/s?src=11&timestamp=1532503813&ver=1019&signature=V1NWQ1eZLCxrJsM5qn7bdRbJ04Fm2r6-7W0NS7fmzlj6OFYSpocMXnfQ*RB0*YT6*JzSXV9r5ZeHgVRP6Nlgh4l885LtMOjsBvqulay6sF0aMAdTeCyxKXRYXYYeoTtH&new=1"
					content=parserUrlHtml(driver,articleUrl);
					if content!="" :
						dir_name, dir_key, p_dir_key,account_str=imgReg.initEnv(subject)
						content=imgReg.regReplaceImgSrc(content)
						try :
							smallPic=imgReg.uploadImgByUrl("http:"+smallPic,dir_name, dir_key, p_dir_key)
						except Exception as err:
							print("缩略图出错")
							smallPic=""
						#替换文章资源
						aricle=TArticle(dir_name=dir_name,dir_key=dir_key,p_dir_key=p_dir_key,art_type=subject,title=title,memo=memo,content=content,source_url=articleUrl,small_pic=smallPic,source=source,pub_date=datetime.datetime.utcfromtimestamp(int(pubDate)),qq=account_str)
						session.add(aricle)
						session.commit()
				print("=====================================分割线==================================")
			except Exception as err:
				print(err)
				break;
		time.sleep(10)
		# break;	
	session.close();		
	driver.quit()	


if __name__ == '__main__':
    task()