
import pika
import json
import configparser
from Logger import *


logfile = 'D:/data/portrait.log'
log = Logger(logfile, level='info')

def getRabbitConn(nodeName):
    cf = configparser.ConfigParser()
    cf.read("../kdata/config.conf")
    host = str(cf.get(nodeName, "host"))
    port = int(cf.get(nodeName, "port"))
    username = str(cf.get(nodeName, "username"))
    password = str(cf.get(nodeName, "password"))
    EXCHANGE_NAME = str(cf.get(nodeName, "EXCHANGE_NAME"))
    vhost = str(cf.get(nodeName, "vhost"))
    routingKey = str(cf.get(nodeName, "routingKey"))
    queueName = str(cf.get(nodeName, "QUEUE_NAME"))

    credentials = pika.PlainCredentials(username=username, password=password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port, virtual_host=vhost, credentials=credentials))
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE_NAME,
                             exchange_type='direct')    # 声明交换机
    channel.queue_declare(queue=queueName)    # 声明队列。消费者需要这样代码，生产者不需要
    channel.queue_bind(queue=queueName, exchange=EXCHANGE_NAME, routing_key=routingKey)    # 绑定队列和交换机

    return channel, EXCHANGE_NAME, queueName, routingKey


# 定义一个回调函数来处理，这边的回调函数就是将信息打印出来。
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    recvStr = str(body, encoding="utf-8")
    recvJson = json.loads(recvStr)    # 接收到的json，包含字段：
    log.logger.info(recvJson)



    print("之后进行人物画像识别")
    # 在这里写人物画像识别的逻辑
    # 1.先识别人（bbox按大小降序排序，先过滤人脸）
    # 2.再识别性别年龄
    # 3.识别表情


if __name__ == '__main__':
    consumer_channel, consumer_EXCHANGE_NAME, consumer_queueName, consumer_routingKey = getRabbitConn("rabbit2portrait")
    log.logger.info("rabbit consumer2portrait 已启动：%s %s %s %s" % (consumer_channel, consumer_EXCHANGE_NAME, consumer_queueName, consumer_routingKey))
    print("rabbit consumer2portrait 已启动：%s %s %s %s" % (consumer_channel, consumer_EXCHANGE_NAME, consumer_queueName, consumer_routingKey))

    consumer_channel.basic_consume(queue=consumer_queueName, on_message_callback=callback, auto_ack=True)    # 这里写的是QUEUE_NAME，而不是routingKey

    print(' [*] Waiting for messages. To exit press CTRL+C')

    # 开始接收信息，并进入阻塞状态，队列里有信息才会调用callback进行处理。按ctrl+c退出。
    consumer_channel.start_consuming()