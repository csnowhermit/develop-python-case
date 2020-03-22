import tensorflow as tf
import numpy as np

'''
    矩阵操作Demo
'''

x= [[4, 15, 2, 2, 20, 10, 20],
    [2, 30, 2, 2, 30, 11, 10],
    [3, 30, 2, 2, 40, 12, 10],
    [3, 30, 2, 2, 20, 13, 10]]

# 矩阵增加一行
add_row = [4, 20, 2, 3, 25, 13, 12]
print(np.row_stack((x, add_row)))

# 矩阵增加一列
add_column = [5, 6, 7, 8]
print("=====", type(add_column))

# numpy.matrix转换为张量
tx = tf.constant(x, dtype=tf.float32)

# 张量转换为numpy
# print(type(tx.eval))
with tf.Session() as sess:
    print(type(sess.run(tx)))

# numpy.matrix：按列提取数据
x = np.mat(x)    # 先把x变成矩阵才能进行按列或按行提取的操作
print(x[:,[0, 1, 2]])
print(x[:, [3, 4, 5]])

x = np.mat(x)
print(x[[0, 1], :])    # 按行提取数据

for i in range(5):
    print(i)