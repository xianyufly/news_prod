import re
import time
#模拟浏览器框架
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--disable-dev-shm-usage')
# 对应的chromedriver的放置目录
driver = webdriver.Chrome(executable_path=(
    r'/usr/local/chromedriver'), chrome_options=chrome_options)
url = "https://www.weiyun.com"
# 微云账号
account_str = "1187383721"
pwd_str = "mirror0402"
driver.get(url)
print(driver.title)
# driver.switch_to_frame("qq_login_iframe")
# switch = driver.find_element_by_id("switcher_plogin")
# switch.click()
# account = driver.find_element_by_id("u")
# account.send_keys(account_str)
# pwd = driver.find_element_by_id("p")
# pwd.send_keys(pwd_str)
# loginButton = driver.find_element_by_id("login_button")
# loginButton.click()
# driver.switch_to.default_content()
driver.get_screenshot_as_file(".\\weiyun.png")
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
driver.quit()