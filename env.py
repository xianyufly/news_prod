'''[summary]
环境变量模块

[description]
'''
import platform


sysstr = platform.system()

def initEnv():
	env={
		"chrome_driver_path":"",
		"python_sql":""
	}
	if(sysstr =="Windows"):
		#window平台
		env["chrome_driver_path"]="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe"
		env["python_sql"]="mysql+mysqldb://root:xian0402@localhost:3306/news"
	elif(sysstr == "Linux"):
		#linux平台
		env["chrome_driver_path"]="/usr/local/chromedriver"
		env["python_sql"]="mysql+mysqldb://17sobt.com:17sobt.com@123456@localhost:6306/news"
	return env