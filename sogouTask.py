import time
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import sogouSubject

def my_job():
    sogouSubject.task()
    print("*******************任务结束*******************")
    sched.add_job(my_job, 'date', run_date=datetime.datetime.now())


sched = BlockingScheduler()
sched.add_job(my_job, 'date', run_date=datetime.datetime.now())
sched.start()
