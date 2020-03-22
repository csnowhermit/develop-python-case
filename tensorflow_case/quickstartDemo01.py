import tensorflow as tf
from numpy.random import RandomState

'''
    TensorFlow神经网络：Demo01
    windows下进入tensorflow环境：activate tensorflow
    离开tensorflow环境：deactivate
'''

# 定义训练数据batch的大小
batch_size = 8

# 定义神经网络的参数
# tf.Variable()作用：保存和更新神经网络的参数
w1 = tf.Variable(tf.random_normal([2, 3], stddev=1, seed=1))
w2 = tf.Variable(tf.random_normal([3, 1], stddev=1, seed=1))

'''
在shape的一个维度上使用None可以方便使用不同的batch大小。在训练时需要把数据分成比较小的batch，但是在测试时，可以一次性使用全部的数据。
当数据集比较小时这样比较方便测试，但是数据集比较大时，将大量数据放入一个batch可能导致内存溢出。
'''
x = tf.placeholder(tf.float32, shape=(None, 2), name='x-input')
y_ = tf.placeholder(tf.float32, shape=(None, 1), name='y-input')

# 定义神经网络前向传播的过程
'''
    w1：输入层各节点到隐藏层各节点边的权重
    w2：隐藏层各节点到输出层各节点边的权重
    x：输入层：[m*n]矩阵，行m列n
    a：隐藏层，该Demo只有一个隐藏层：[n*z]矩阵，第一行为上一层第一个节点到本层所有节点的边的权重，第二行为上一行第二个节点到本层所有节点的权重，以此类推
    y：输出层：[m*z]矩阵，最终结果该矩阵各列相加
'''
a = tf.matmul(x, w1)    # tf.matmul()做矩阵乘法
y = tf.matmul(a, w2)

# 非线性激活函数
y = tf.sigmoid(y)

'''
    计算交叉熵
    y_：正确结果
    y：预测结果
    tf.clip_by_value()：对于y集合，将小于1e-10的值都替换成1e-10，将大于1.0的值都替换成1.0；目的是将一个张量中的数值限制到一个范围内，避免出现一些运算错误
    科学计数法：1e-10表示 1*10^(-10)次方
    交叉熵的乘法直接使用*相乘(每个位置上对应元素的乘积)，矩阵相乘用tf.matmul()
    p * tf.log(p)：交叉熵损失函数
    tf.reduce_mean()：求平均
'''
cross_entropy = -tf.reduce_mean(
    y_ * tf.log(tf.clip_by_value(y, 1e-10, 1.0))
    + (1 - y) * tf.log(tf.clip_by_value(1 - y, 1e-10, 1.0))
)

learning_rate = 0.001
# 定义反向传播的方法来优化神经网络的参数（反向传播的优化方法）：0.001为learning rate，
# .minimize(cross_entropy)，最小化交叉熵（损失函数值）
train_step = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cross_entropy)

# 通过随机数生成一个模拟数据集
rdm = RandomState(1)
dataset_size = 128
X = rdm.rand(dataset_size, 2)
'''
定义规则来给出样本的标签。在这里所有x1+x2<1的样例都被认为是正样本（比如零件合格），而其他为负样本（比如零件不合格）。
和TensorFlow游乐场中的表示法不大一样的地方是，在这里使用0来表示负样本，1来表示正样本。
大部分解决分类问题的神经网络都会采用0和1的表示方法。
'''
Y = [[int(x1 + x2 < 1)] for (x1, x2) in X]

# 创建一个绘画来运行tensorflow程序
with tf.Session() as sess:
    init_op = tf.global_variables_initializer()  # 初始化变量
    sess.run(init_op)

    # 打印训练之前的参数值
    print(sess.run(w1))
    print(sess.run(w2))

    # 设定训练的轮数
    STEPS = 5000
    for i in range(STEPS):
        # 每次选取batch_size个样本进行训练
        start = (i * batch_size) % dataset_size
        end = min(start + batch_size, dataset_size)

        # 通过选取的样本训练神经网络并更新参数
        sess.run(train_step,
                 feed_dict={x: X[start:end], y_: Y[start:end]})
        if i % 1000 == 0:
            # 每隔一段时间计算在所有数据上的交叉熵并输出
            total_cross_entrypy = sess.run(
                cross_entropy, feed_dict={x: X, y_: Y}
            )

            # 随着训练的进行，发现交叉熵不断变小。交叉熵越小说明预测结果与真实结果的差距越小。
            print("After %d training steps, cross entrypu on all data is %g" % (i, total_cross_entrypy))

    # 打印训练之后的参数值
    print(sess.run(w1))
    print(sess.run(w2))
