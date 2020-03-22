import tensorflow as tf

'''
    TF中包含两种队列：FIFOQueue和RandomShuffleQueue。
    RandomShuffleQueue在出队时随机挑选元素出队。在训练神经网络时希望每次使用的训练数据尽量随机，所以更适合使用RandomShuffleQueue。
'''

# 创建一个先进先出队列，指定队列中最多可以保存2个元素，并指定数据类型为整数
q = tf.FIFOQueue(2, "int32")

# 使用enqueue_many函数来初始化队列中的元素。和变量初始化类似，在使用队列之前需要明确调用这个初始化过程
init = q.enqueue_many(([0, 10], ))
# 使用Dequeue函数将队列中的第一个元素出队列。这个元素的值将被存在变量x中。
x = q.dequeue()
y = x + 1

# 将加1后的值重新加入队列
q_inc = q.enqueue([y])

with tf.Session() as sess:
    # 进行初始化队列的操作
    init.run()
    for _ in range(5):
        # 运行q_inc将执行数据出队，+1，入队的整个过程
        v, _ = sess.run([x, q_inc])
        print(v)

