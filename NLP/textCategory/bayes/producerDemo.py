import pika
import time
import configparser

def getRabbitConn(nodeName):
    cf = configparser.ConfigParser()
    cf.read("../kdata/config.conf")
    print(cf.sections())
    host = str(cf.get(nodeName, "host"))
    port = int(cf.get(nodeName, "port"))
    username = str(cf.get(nodeName, "username"))
    password = str(cf.get(nodeName, "password"))
    EXCHANGE_NAME = str(cf.get(nodeName, "EXCHANGE_NAME"))
    vhost = str(cf.get(nodeName, "vhost"))
    routingKey = str(cf.get(nodeName, "routingKey"))

    credentials = pika.PlainCredentials(username=username, password=password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host, port=port, virtual_host=vhost, credentials=credentials))
    channel = connection.channel()
    # channel.queue_declare(queue=routingKey, durable=True)    # 定义持久化队列
    # channel.queue_declare(queue=routingKey)  # 定义持久化队列

    return channel, EXCHANGE_NAME, routingKey

backstage_channel, backstage_EXCHANGE_NAME, backstage_routingKey = getRabbitConn("rabbit2portrait")

for i in range(10):
    s = "Hello-" + str(i)
    backstage_channel.basic_publish(exchange=backstage_EXCHANGE_NAME,
                                    routing_key=backstage_routingKey,
                                    body=s)    # 将语义识别结果给到后端
    print(s)
    time.sleep(1)