import requests
import urllib
import json,time
header ={ 		
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
	"Accept-Language": "zh-CN,zh;q=0.9",
	"Cache-Control": "max-age=0",
	"Connection": "keep-alive",
	"Cookie": "bid=xkeq5xyAk-0",
	"Host": "api.douban.com",
	"Upgrade-Insecure-Requests": "1",
	"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
}
while True:
	url="https://api.douban.com/v2/book/isbn/9787020008728"
	# proxies = {
	#   "http": "http://124.235.208.252:443",
	#   "https": "http://124.235.208.252:443",
	# }
	# response = requests.get(url, proxies = proxies)
	# obj=json.loads(response.text)
	# print(response)
	# print("书名:%s"%(obj["title"]))
	proxy_addr="124.235.208.252:443"
	proxy = urllib.request.ProxyHandler({'http': proxy_addr,'https': proxy_addr})
	opener = urllib.request.build_opener(proxy, urllib.request.ProxyHandler)
	urllib.request.install_opener(opener)
	req = urllib.request.Request(url, None, headers=header)
	response = urllib.request.urlopen(req)
	html=response.read().decode('UTF-8')
	obj=json.loads(html)
	print("书名:%s"%(obj["title"]))
	time.sleep(0.1)
	print("=====================================分割线==================================")