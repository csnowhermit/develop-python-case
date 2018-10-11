
import time

print(time.strftime("%Y%m%d_%H%M%S", time.localtime()))

'''
    获取n秒后的时间，n为负数则为获取n秒前的时间
'''
def getSpecifyTime(n, fmt):
    now = time.time()
    before = now + n

    return time.strftime(fmt, time.localtime(before))

print(getSpecifyTime(-86400, "%Y%m%d_%H%M%S"))
print(getSpecifyTime(-86400, "%Y%m%d"))