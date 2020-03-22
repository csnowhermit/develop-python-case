import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import numpy as np

'''
    将mnist输入数据转化为TFRecord格式
'''

# 生成整数型的属性
def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

# 生成字符串型的属性
def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

mnist = input_data.read_data_sets('../../mnist/data', dtype=tf.uint8, one_hot=True)
images = mnist.train.images     # 训练数据的输入
labels = mnist.train.labels     # 训练数据的（正确答案）输出，可以作为一个属性保存在TFRecord中

pixels = images.shape[1]        # 训练数据的图像分辨率，可以作为Example中的一个属性
num_examples = mnist.train.num_examples
filename = "./output_cast2TFRecord.tfrecords"    # 输出TFRecord文件的地址
writer = tf.python_io.TFRecordWriter(filename)       # 创建一个writer来写TFRecord文件

for index in range(num_examples):
    # 1.将图像矩阵转化成一个字符串
    image_raw = str(images[index])

    # 2.将每一个样例转化为Example Protocol Buffer，并将所有的信息写入到这个数据结构
    example = tf.train.Example(features=tf.train.Feature(feature={
        'pixels': _int64_feature(pixels),
        'label': _int64_feature(np.argmax(labels[index])),
        'image_raw': _bytes_feature(image_raw)}
    ))

    # 3.将一个Example写入TFRecord文件
    writer.write(example.SerializeToString())

writer.close()
