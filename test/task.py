import time
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

def my_job():
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    time.sleep(10)
    sched.add_job(my_job, 'date', run_date=datetime.datetime.now())

def my_job1():
    print("my_job1:%s"%(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
    time.sleep(5)
    sched.add_job(my_job1, 'date', run_date=datetime.datetime.now())

sched = BlockingScheduler()
# sched.add_job(my_job, 'interval', seconds=5)
sched.add_job(my_job, 'date', run_date=datetime.datetime.now())
sched.add_job(my_job1, 'date', run_date=datetime.datetime.now())
sched.start()