"""[summary]
搜狗微信公众号文章--爬虫入口
[description]
"""
import os,time
import requests
import urllib
import json

from thirdFileUtil import weiyun,baiduyunpan
# #初始化微云服务器
# weiyun.init()
# rootDirKey,mainDirKey = weiyun.getRootAndMainDirKey()
# dir_key,pdir_key=weiyun.wy_diskDirCreate(mainDirKey,rootDirKey,"A_AA")
# print("创建文件夹dir_key:%s,pdir_key:%s"%(dir_key,pdir_key))
# share_url=weiyun.wy_shareUrl("a909c646e6ee65d91adc576c9bf1f5e7",
#             "b20bd248-d3b5-4005-bc0c-5885c698da8e", "1.png")
# print("分享地址:",share_url)
# aim_url=weiyun.wy_filePath(share_url,"video")
# print(aim_url)

# 百度云盘初始化

# baiduyunpan.init()
# baiduFolder="/A_我的站点"
# flag=baiduyunpan.createFolder(baiduFolder)
# if flag == True :
# 	print("文件夹创建成功")
# else :
# 	print("文件夹创建失败")
# baiduFilePath=baiduFolder+"/1.mp4"
# localFilePath="C:\\Users\\Administrator\\Desktop\\新建文件夹\\1.mp4"
# fs_id=baiduyunpan.uploadFile(baiduFilePath ,localFilePath)
# print("上传百度视频ID:",fs_id)
# # 获取分享文件地址
# shareUrl,pwd=baiduyunpan.getShareUrl(fs_id)
# print("分享地址:"+shareUrl+",分享密码:"+pwd)