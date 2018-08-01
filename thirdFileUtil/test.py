import os
import shutil
def deleteFolder():
	workfolder = os.getcwd()
	aimfolder = workfolder+"/temp/1"
	shutil.rmtree(aimfolder)