"""[summary]
搜狗栏目抓取--爬虫
[description]
"""
import os,time,datetime
import requests
import urllib
import json
import re
import random
from thirdFileUtil import imgReg
from models.TSubject import TSubject

from requests.packages.urllib3.exceptions import InsecureRequestWarning

#数据库操作库
import pymysql
import env
#ORM 框架
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#模拟浏览器框架
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
pymysql.install_as_MySQLdb()

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
#系统变量
_env=env.initEnv()
# 对应的chromedriver的放置目录
driver = webdriver.Chrome(executable_path=(
    _env["chrome_driver_path"]), chrome_options=chrome_options)

url = "http://weixin.sogou.com/"
driver.get(url)
driver.delete_all_cookies()
cookie_ppinf={
	"name":"ppinf",
	"value":"5|1530259052|1531468652|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxODolRTklOUElOTAlRTklOUElOTB8Y3J0OjEwOjE1MzAyNTkwNTJ8cmVmbmljazoxODolRTklOUElOTAlRTklOUElOTB8dXNlcmlkOjQ0Om85dDJsdUlYY1hTc2p2OGtCWUtUUVAyeW9aMW9Ad2VpeGluLnNvaHUuY29tfA"
}
driver.add_cookie(cookie_ppinf)
cookie_pprdig={
	"name":"pprdig",
	"value":"heLCzh3P-FyUczVfW62TekXb5VNdzRYxg9VGXtd0P9xpOFPJvEwcNuupp8Ygg1hTasPkrutL0vdWEQqniTkB_xVlx9hTI1n4CtmBE8dwanw-ZomkhsOYSMetYdi3lYek5vo5kRc3gQR4ng8MyNfF2ADYvl4B44NFGOeRrAukfVE"
}
driver.add_cookie(cookie_pprdig)
driver.get(url)
type_tab=driver.find_element_by_id("type_tab")

type_a_array=type_tab.find_elements_by_tag_name("a")
#链接数据库
engine = create_engine(_env["python_sql"])
DB_Session = sessionmaker(bind=engine)
session = DB_Session()
try :
	for type_a in type_a_array :
		id=type_a.get_property("id")
		name=type_a.get_attribute("innerText")
		if id!= None and id.find("pc_") >-1 :
			print("菜单ID:%s,菜单名称:%s"%(id,name))
			subject=TSubject(sub_code=id,sub_name=name)
			session.add(subject)
			print("=====================================分割线==================================")
finally:
	session.commit()
	driver.quit()