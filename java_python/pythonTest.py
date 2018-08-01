import getopt
import sys

options,args = getopt.getopt(sys.argv[1:], "", ["caption=","proc_name="])

if options != []:
    for name,value in options:
        if name == '--caption':
            CAPTION = value
        if name == '--proc_name':
            PROC_NAME = value
print(CAPTION)
print(PROC_NAME)
		
