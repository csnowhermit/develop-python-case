import os
import tensorflow as tf

'''
    GPU加速：查看运算的设备
    allow_soft_placement=True：当不能使用GPU进行计算时，自动使用CPU进行计算
    最佳实践：将计算密集型的计算放在GPU上，其他计算放在CPU上；
        尽量将相关的计算放在同一设备上；（计算放入或转出GPU都会耗时，且GPU载入数据会经过内存，也需要额外的时间）
'''

# 指定，只使用第一块GPU。（Tensorflow默认使用所有GPU及显存）
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# 虽然GPU默认会占所有显存
config = tf.ConfigProto()
config.gpu_options.allow_growth = True    # 让Tensorflow按需分配显存

# 或者直接指定固定的比例分配
config.gpu_options.per_process_gpu_memory_fraction = 0.4    # 指定，可使用40%的显存
# sess = tf.Session(config=config, ....)

# 计算时指定设备
with tf.device('/cpu:0'):
    a = tf.constant([1.0, 2.0, 3.0], shape=[3], name='a')
    b = tf.constant([1.0, 2.0, 3.0], shape=[3], name='b')

with tf.device('/gpu:0'):
    c = a + b

# allow_soft_placement=True，当不能使用GPU计算时，自动使用CPU计算
with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as sess:
    sess.run(tf.initialize_local_variables())
    print(sess.run(c))