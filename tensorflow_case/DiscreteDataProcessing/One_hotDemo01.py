import tensorflow as tf
import numpy as np

'''
    one-hot编码：对Array编码
'''

x = [0, 1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1, 0]

CLASS = len(list(set(x)))

with tf.Session() as sess:
    label1 = tf.constant(x)
    print("before one hot: \n", sess.run(label1))
    tf.global_variables_initializer()
    b = tf.one_hot(label1, CLASS, 1, 0)
    print("after one hot: \n", sess.run(b))
