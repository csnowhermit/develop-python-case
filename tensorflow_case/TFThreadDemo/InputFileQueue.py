import tensorflow as tf

# 创建TFRecord文件的帮助函数
def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

'''
    生产数据
'''
def newData():
    # 模拟海量数据情况下将数据写入不同的文件。
    num_shards = 2  # 总共写入多少个文件
    instances_per_shard = 2  # 每个文件中有多少个数据
    for i in range(num_shards):
        # 不同的文件以0000n-of-0000m后缀区分
        filename = ('./data/data.tfrecords-%.5d-of-%.5d' % (i, num_shards))
        writer = tf.python_io.TFRecordWriter(filename)
        # 将数据封装成Example结构并写入TFRecord文件中
        for j in range(instances_per_shard):
            # Example结构仅包含当前样例属于第几个文件以及是当前文件的第几个副本
            example = tf.train.Example(features=tf.train.Features(feature={
                'i': _int64_feature(i),
                'j': _int64_feature(j)
            }))
            writer.write(example.SerializeToString())
    writer.close()

def readData(filepath):
    files = tf.train.match_filenames_once(filepath)
    filename_queue = tf.train.string_input_producer(files, shuffle=False)
    print(type(filename_queue))

    reader = tf.TFRecordReader
    _, serialized_example = reader.read(filename_queue)
    features = tf.parse_single_example(serialized_example, features={
        'i': tf.FixedLenFeature([], tf.int64),
        'j': tf.FixedLenFeature([], tf.int64)
    })

    with tf.Session() as sess:
        tf.local_variables_initializer().run()
        print(sess.run(files))

        # 声明tf.train.start_queue_runners()类来协同不同线程，并启动线程
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess=sess, coord=coord)

        # 多次执行获取数据的操作
        for i in range(6):
            print(sess.run([features['i'], features['j']]))
        coord.request_stop()
        coord.join(threads)


def main():
    # newData()
    filepath = "./data/data-tfrecords-*"
    readData(filepath)

if __name__ == '__main__':
    main()