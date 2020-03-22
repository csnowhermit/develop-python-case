import tensorflow as tf

'''
    从数组中加载数据集
    从一个张量创建一个数据集，遍历这个集合，并对每个输入输出y=x^2的值
'''

# 从一个数组创建数据集
input_data = [1, 2, 3, 4, 5]
dataset = tf.data.Dataset.from_tensor_slices(input_data)    # 表明数据集是从张量中构建的

# 定义一个迭代器遍历数据集。因为上面没有用placeholder作为输入参数，所以这里可以使用最简单的one_shot_iterator
iterator = dataset.make_one_shot_iterator()

x = iterator.get_next()
y = x * x

with tf.Session() as sess:
    for i in range(len(input_data)):
        print(sess.run(y))
