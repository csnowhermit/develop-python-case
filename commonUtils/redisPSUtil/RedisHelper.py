import redis


class RedisHelper:
    def __init__(self):
        self.connection_pool = redis.ConnectionPool(host="192.168.117.134", port=6379, password="123456")
        self.__conn = redis.Redis(connection_pool=self.connection_pool)  # 连接redis
        # self.__conn = redis.Redis(host="192.168.117.134", port=6379, password="123456")

    def publish(self, pub, msg):
        self.__conn.publish(pub, msg)  # 根据提供的频道进行消息发布
        return True

    def subscribe(self, sub):
        pub = self.__conn.pubsub()  # 打开收音机
        pub.subscribe(sub)  # 调频道
        pub.parse_response()  # 准备接收
        return pub
