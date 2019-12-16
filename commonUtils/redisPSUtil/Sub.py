from commonUtils.redisPSUtil.RedisHelper import RedisHelper

rds = RedisHelper()  # 得到实例化对象
while 1:
    data = rds.subscribe("Bao").parse_response()  # 此时会处于一直订阅的状态有数据就会接收过来
    if data:
        print(str(data[2], encoding="utf-8"))
