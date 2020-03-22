import tensorflow as tf
import numpy as np
import threading
import time

'''
    Tensorflow多线程
'''

'''
    线程中运行的程序：每隔1s判断是否需要停止并打印自己的ID
'''
def MyLoop(coord, worker_id):
    # 使用tf.Coordinator类提供的协同工具判断当前线程是否需要停止
    while not coord.should_stop():
        if np.random.rand()<0.1:
            print("Stoping from id: ", worker_id)
            coord.request_stop()    # 通知其他线程停止
        else:
            print("Working on id: ", worker_id)

        time.sleep(1)

coord = tf.train.Coordinator()
threads = [threading.Thread(target=MyLoop, args=(coord, i, )) for i in range(5)]
# 启动所有的线程
for t in threads:
    t.start()

# 等待所有线程退出
coord.join(threads)