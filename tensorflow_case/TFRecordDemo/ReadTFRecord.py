import tensorflow as tf

'''
    读取TFRecord文件
'''

reader = tf.TFRecordReader()
filename_queue = tf.train.string_input_producer(['./output_cast2TFRecord.tfrecords'])

# 从文件中读取一个样例，读取多个样例用reader.read_up_to()函数
_, serialized_example = reader.read(filename_queue)

'''
    TensorFlow提供两种不同的属性解析方法：
    tf.FixedLenFeature()：解析结果为一个Tensor；
    tf.VarLenFeature()：解析结果为SparseTensor，用于处理稀疏数据；
    这里解析数据的格式需要和上面程序写入数据的格式一致。
'''
# 解析读入的一个样例，多个样例用tf.parse_example()函数
features = tf.parse_single_example(
    serialized_example,
    features={
        'image_raw': tf.FixedLenFeature([], tf.string),
        'pixels': tf.FixedLenFeature([], tf.int64),
        'label': tf.FixedLenFeature([], tf.int64)
    }
)

images = tf.decode_raw(features['image_raw'], tf.uint8)    # 将字符串解析成图像对应的像素数组
label = tf.cast(features['label'], tf.int32)
pixels = tf.cast(features['pixels'], tf.int32)

sess = tf.Session()
# 启动多个线程处理输入数据
coord = tf.train.Coordinator()
threads = tf.train.start_queue_runners(sess=sess, coord=coord)

# 每次运行可以读取TFRecord文件中的一个样例。当所有样例都读完之后，在此样例程序中再从头读取。
for i in range(10):
    print(sess.run([images, label, pixels]))

sess.close()