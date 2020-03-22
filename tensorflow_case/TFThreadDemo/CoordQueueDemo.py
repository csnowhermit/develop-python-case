import tensorflow as tf

'''
    使用tf.Coordinator和tf.QueueRunner管理多线程队列操作
'''

queue = tf.FIFOQueue(100, "float")
# 定义队列入队操作
enquence_op = queue.enqueue([tf.random_normal([1])])

# 表示需要启动5个线程，每个线程中运行的是enquence_op操作
qr = tf.train.QueueRunner(queue, [enquence_op] * 5)

# 将定义过的QueueRunner加入TensorFlow计算图上指定的集合
tf.train.add_queue_runner(qr)

# 定义出队操作
out_tensor = queue.dequeue()

with tf.Session() as sess:
    coord = tf.train.Coordinator()

    # 使用tf.train.QueueRunner时，需要明确调用tf.train.start_queue_runners()来启动所有线程。
    # 否则因为没有线程进行入队操作，当调用出队操作时，程序会一直等待入队操作被运行。
    # tf.train.start_queue_runners()函数会默认启动tf.GraphKeys.QUEUE_RUNNERS集合所有的QueueRunner，因为这个函数只支持自动指定集合中的QueueRunner。
    # 一般tf.train.start_queue_runners()函数和tf.GraphKeys.QUEUE_RUNNERS()函数会指定同一个集合。
    threads = tf.train.start_queue_runners(sess=sess, coord=coord)

    # 获取队列中的取值
    for _ in range(3):
        print(sess.run(out_tensor)[0])

    # 使用tf.train.Coordinator来停止所有的线程
    coord.request_stop()
    coord.join()