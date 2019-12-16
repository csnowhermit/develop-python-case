from commonUtils.redisPSUtil.RedisHelper import RedisHelper

rds = RedisHelper()
while 1:
    data = str(input("请输入您想推送的数据："))
    if data:
        rds.publish("Bao", data)
        print("finished")
