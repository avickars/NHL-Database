import datetime
from random import randint


def get_time():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nowTime = datetime.datetime.strptime(now, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(seconds=randint(1, 1000))
    return str(nowTime)
