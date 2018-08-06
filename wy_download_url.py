"""[summary]
微云服务器--上传
[description]
"""
import os
import time
import requests
import urllib
import json
import re
import random 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
# sha1 加密算法
from hashlib import sha1
import base64
# 导入支持双击操作的模块
from selenium.webdriver import ActionChains

#数据库操作库
import pymysql
#ORM 框架
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.WyCookie import WyCookie
from models.WyQq import WyQq
import getopt
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from thirdFileUtil import ipPool

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#获取传递参数
options,args = getopt.getopt(sys.argv[1:], "", ["python_sql=","chrome_driver_path=","qq=","file_list="])

if options != []:
    for name,value in options:
        if name == '--python_sql':
            python_sql = urllib.parse.unquote(value)
        if name == '--chrome_driver_path':
            chrome_driver_path = urllib.parse.unquote(value)
        if name == '--qq':
            qq = urllib.parse.unquote(value)
        if name == '--file_list':
            file_list = urllib.parse.unquote(value)
            file_list = json.loads(file_list)



pymysql.install_as_MySQLdb()
#链接数据库
engine = create_engine(python_sql)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()

'''
初始化driver
'''
def initChromeDriver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument("--no-sandbox")
    # 对应的chromedriver的放置目录
    driver = webdriver.Chrome(executable_path=(
        chrome_driver_path), chrome_options=chrome_options)
    return driver


# 微云账号
# account_str = "1187383721"
# pwd_str = "mirror0402"

# 公用变量
web_wx_rc = ""
pgv_pvi = ""
pgv_si = ""
ptisp = ""
ptui_loginuin = ""
pt2gguin = ""
uin = ""
skey = ""
ptcz = ""
p_uin = ""
pt4_token = ""
p_skey = ""
wyctoken = ""

# 全局变量
rootDirKey, mainDirKey = "", ""
'''
返回根目录key
'''


def getRootAndMainDirKey():
    global rootDirKey, mainDirKey
    return rootDirKey, mainDirKey


'''
返回cookie内容
'''


def getCookieByParam(cookieData, key, domain=""):
    val = ""
    # 初始化要获取的cookie
    for item in cookieData:
        if domain == "" and item["name"] == key:
            val = item["value"]
        elif domain != "" and item["name"] == key and item["domain"] == domain:
            val = item["value"]
    return val

proxy_addr = None

'''
代理请求--普通post请求
'''
def proxyRquest_normal(url,data,headers):
    global proxy_addr
    targeturl = "https://www.weiyun.com"
    flag = True
    while flag:
        try :
            if proxy_addr == None :
                proxy_addr=ipPool.randomGetIp(targeturl)
            proxies = {
              "http": "http://"+proxy_addr,
              "https": "http://"+proxy_addr,
            }
            flag=False
            result = requests.request('POST' , url, proxies = proxies, data=json.dumps(
                data), headers=headers, verify=False,timeout = 5)
        except requests.exceptions.ProxyError as err:
            proxy_addr=None
            flag=True
    return result


'''
微云--初始化
参数

返回

'''


def init():
    global web_wx_rc, pgv_pvi, pgv_si, ptisp, ptui_loginuin, pt2gguin, uin, skey, ptcz, p_uin, pt4_token, p_skey, wyctoken
    global rootDirKey, mainDirKey
    global qq

    #
    session = DB_Session()
    qq=session.query(WyQq).filter(WyQq.account_str == qq).first()
    if qq != None :
        account_str=qq.account_str
        pwd_str=qq.pwd_str
    else :
        account_str='1187383721'
        pwd_str='mirror0402'
    #从数据库查询cookie
    wycookieTeamp = session.query(WyCookie).filter(WyCookie.account_str == account_str).first()
    if(wycookieTeamp):
        web_wx_rc = wycookieTeamp.web_wx_rc
        pgv_pvi = wycookieTeamp.pgv_pvi
        pgv_si = wycookieTeamp.pgv_si
        ptisp = wycookieTeamp.ptisp
        ptui_loginuin = wycookieTeamp.ptui_loginuin
        pt2gguin = wycookieTeamp.pt2gguin
        uin = wycookieTeamp.uin
        skey = wycookieTeamp.skey
        ptcz = wycookieTeamp.ptcz
        p_uin = wycookieTeamp.p_uin
        pt4_token = wycookieTeamp.pt4_token
        p_skey = wycookieTeamp.p_skey
        wyctoken = wycookieTeamp.wyctoken
        rootDirKey = wycookieTeamp.rootDirKey
        mainDirKey = wycookieTeamp.mainDirKey
        #验证cookie是否可以使用
        flag=wy_safeBox()
        if flag :
            return;
    try:
        driver = initChromeDriver()
        url = "https://www.weiyun.com"
        driver.get(url)
        driver.switch_to_frame("qq_login_iframe")
        switch = driver.find_element_by_id("switcher_plogin")
        switch.click()
        account = driver.find_element_by_id("u")
        account.send_keys(account_str)
        pwd = driver.find_element_by_id("p")
        pwd.send_keys(pwd_str)
        loginButton = driver.find_element_by_id("login_button")
        loginButton.click()
        driver.switch_to.default_content()
        # 获取root_dir_key
        flag = True
        reg = re.compile(r'\"root_dir_key\":\"(.*?)\"')

        while flag:
            try:
                rootDirKeyArray = reg.findall(driver.page_source)
                rootDirKey = rootDirKeyArray[0]
                flag = False
            except:
                flag = True
            finally:
                time.sleep(0.1)
        # 获取 main_dir_key
        flag = True
        reg = re.compile(r'\"main_dir_key\":\"(.*?)\"')
        while flag:
            try:
                mainDirKeyArray = reg.findall(driver.page_source)
                mainDirKey = mainDirKeyArray[0]
                flag = False
            except:
                flag = True
            finally:
                time.sleep(0.1)
        # 获取网站cookie
        cookie = driver.get_cookies()
        web_wx_rc = getCookieByParam(cookie, "web_wx_rc", ".weiyun.com")
        pgv_pvi = getCookieByParam(cookie, "pgv_pvi", ".weiyun.com")
        pgv_si = getCookieByParam(cookie, "pgv_si", ".weiyun.com")
        ptisp = getCookieByParam(cookie, "ptisp", ".weiyun.com")
        ptui_loginuin = getCookieByParam(cookie, "ptui_loginuin", ".weiyun.com")
        pt2gguin = getCookieByParam(cookie, "pt2gguin", ".weiyun.com")
        uin = getCookieByParam(cookie, "uin", ".weiyun.com")
        skey = getCookieByParam(cookie, "skey", ".weiyun.com")
        ptcz = getCookieByParam(cookie, "ptcz", ".weiyun.com")
        p_uin = getCookieByParam(cookie, "p_uin", ".weiyun.com")
        pt4_token = getCookieByParam(cookie, "pt4_token", ".weiyun.com")
        p_skey = getCookieByParam(cookie, "p_skey", ".weiyun.com")
        wyctoken = getCookieByParam(cookie, "wyctoken", ".weiyun.com")
        #删除旧数据
        wycookie=WyCookie(account_str=account_str,web_wx_rc=web_wx_rc,pgv_pvi=pgv_pvi,pgv_si=pgv_si,ptisp=ptisp,ptui_loginuin=ptui_loginuin
            ,pt2gguin=pt2gguin,uin=uin,skey=skey,ptcz=ptcz,p_uin=p_uin,pt4_token=pt4_token,p_skey=p_skey,wyctoken=wyctoken,rootDirKey=rootDirKey,mainDirKey=mainDirKey)
        if(wycookieTeamp):
            session.delete(wycookieTeamp)
        session.add(wycookie)
        session.commit()
    except Exception as err:
        print("fail")
    finally:
        session.close()
        # 关闭浏览器
        driver.quit()

'''[summary]
微云 - 获取腾讯微云下载地址
参数
pdir_key:上级目录
file_id: 文件ID
file_name:文件名称
[description]
'''
def wy_safeBox():
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "content-type": "application/json;charset=UTF-8",
        "accept-language": "zh-CN,zh;q=0.9",
        "cookie": "web_wx_rc=%s; pgv_pvi=%s; pgv_si=%s; ptisp=%s; ptui_loginuin=%s; pt2gguin=%s; uin=%s; skey=%s; ptcz=%s; p_uin=%s; pt4_token=%s; p_skey=%s; wyctoken=%s" % (web_wx_rc, pgv_pvi, pgv_si, ptisp, ptui_loginuin, pt2gguin, uin, skey, ptcz, p_uin, pt4_token, p_skey, wyctoken),
        "origin": "https://www.weiyun.com",
        "referer": "https://www.weiyun.com/disk",
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
    }
    req_header = {
        "seq": int(str(int(time.time()))+'6484240'),
        "type": 1,
        "cmd": 2402,
        "appid": 30013,
        "version": 3,
        "major_version": 3,
        "minor_version": 3,
        "fix_version": 3,
        "wx_openid": "",
        "user_flag": 0
    }
    req_body = {
        "ReqMsg_body": {
            "ext_req_head": {
                "token_info": {
                    "token_type": 0,
                    "login_key_type": 1,
                    "login_key_value": skey
                }
            },
            ".weiyun.SafeBoxCheckStatusMsgReq_body":  {
            }
        }
    }
    data = {
        "req_header": json.dumps(req_header),
        "req_body": json.dumps(req_body)
    }
    url = "https://www.weiyun.com/webapp/json/weiyunSafeBox/SafeBoxCheckStatus?refer=chrome_windows&g_tk="+wyctoken+"&r="+str(random.random())
    # result = requests.request('POST', url, data=json.dumps(
    #     data), headers=headers, verify=False)
    result = proxyRquest_normal(url,data,headers)
    flag =True
    try :
        successBean = result.json()
        if successBean['data']:
            flag =True
    except Exception as err:
        print(err)
        flag=False
    return flag

'''[summary]
微云 - 获取腾讯微云下载地址
参数
pdir_key:上级目录
file_id: 文件ID
file_name:文件名称
[description]
'''


def wy_downloadUrl(file_list):
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "content-type": "application/json;charset=UTF-8",
        "accept-language": "zh-CN,zh;q=0.9",
        "cookie": "web_wx_rc=%s; pgv_pvi=%s; pgv_si=%s; ptisp=%s; ptui_loginuin=%s; pt2gguin=%s; uin=%s; skey=%s; ptcz=%s; p_uin=%s; pt4_token=%s; p_skey=%s; wyctoken=%s" % (web_wx_rc, pgv_pvi, pgv_si, ptisp, ptui_loginuin, pt2gguin, uin, skey, ptcz, p_uin, pt4_token, p_skey, wyctoken),
        "origin": "https://www.weiyun.com",
        "referer": "https://www.weiyun.com/disk",
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
    }
    req_header = {
        "seq": int(str(int(time.time()))+'6484240'),
        "type": 1,
        "cmd": 2402,
        "appid": 30013,
        "version": 3,
        "major_version": 3,
        "minor_version": 3,
        "fix_version": 3,
        "wx_openid": "",
        "user_flag": 0
    }
    req_body = {
        "ReqMsg_body": {
            "ext_req_head": {
                "token_info": {
                    "token_type": 0,
                    "login_key_type": 1,
                    "login_key_value": skey
                }
            },
            ".weiyun.DiskFileBatchDownloadMsgReq_body":  {
                "file_list": file_list,
                "download_type": 16
            }
        }
    }
    data = {
        "req_header": json.dumps(req_header),
        "req_body": json.dumps(req_body)
    }
    url = "https://www.weiyun.com/webapp/json/weiyunQdiskClient/DiskFileBatchDownload?refer=chrome_windows&g_tk="+wyctoken+"&r="+str(random.random())
    # result = requests.request('POST', url, data=json.dumps(
    #     data), headers=headers, verify=False)
    result = proxyRquest_normal(url,data,headers)
    successBean = result.json()
    if successBean["data"]["rsp_header"]["retcode"] == 0:
        download_url = []
        filelist=successBean["data"]["rsp_body"]["RspMsg_body"]["file_list"]
        for file in filelist :
            download_url.append(file["download_url"])
        return download_url
    else:
        return []





try:
    #创建文件夹
    init()
    download_url=wy_downloadUrl(file_list)
    print(download_url)
except Exception as err:
    print(err)
