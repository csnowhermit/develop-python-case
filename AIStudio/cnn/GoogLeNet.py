import tensorflow as tf

'''
    GoogLeNet的keras实现
    GoogLeNet：网络加深到22层，引入Inception结构代替简单的卷积+激活
'''

'''
    :param x 输入矩阵
    :param nb_filter filter数量
    :param kernel_size 卷积核大小
'''
def Conv2d_BN(x, nb_filter, kernel_size, padding='same', strides=(1,1), name=None):
    if name is not None:
        bn_name = name + '_bn'
        conv_name = name + '_conv'
    else:
        bn_name = None
        conv_name = None

    x = tf.keras.layers.Conv2D(nb_filter, kernel_size, padding=padding, strides=strides, activation='relu', name=conv_name)(x)
    x = tf.keras.layers.BatchNormalization(axis=3, name=bn_name)(x)
    return x

def Inception(x, nb_filter):
    batches1x1 = Conv2d_BN(x, nb_filter, (1, 1), padding='same', strides=(1, 1), name=None)

    batches3x3 = Conv2d_BN(x, nb_filter, (3, 3), padding='same', strides=(1, 1), name=None)
    batches3x3 = Conv2d_BN(batches3x3, nb_filter, (3, 3), padding='same', strides=(1, 1), name=None)

    batches5x5 = Conv2d_BN(x, nb_filter, (3, 3), padding='same', strides=(1, 1), name=None)
    batches5x5 = Conv2d_BN(batches5x5, nb_filter, (3, 3), padding='same', strides=(1, 1), name=None)

    batchpool = tf.keras.layers.MaxPooling2D(pool_size=(3, 3), strides=(1, 1), padding='same')(x)
    batchpool = Conv2d_BN(batchpool, nb_filter, (1, 1), padding='same', strides=(1, 1), name=None)

    x = tf.keras.layers.concatenate([batches1x1, batches3x3, batches5x5, batchpool], axis=3)
    return x

def GoogLeNet():
    inpt = tf.keras.layers.Input((224, 224, 3))
    x = Conv2d_BN(inpt, nb_filter=64, kernel_size=(7, 7), strides=(2, 2), padding='same')
    x = tf.keras.layers.MaxPooling2D(pool_size=(3, 3), strides=(2, 2), padding='same')(x)

    x = Conv2d_BN(x, nb_filter=192, kernel_size=(3, 3), strides=(1, 1), padding='same')
    x = tf.keras.layers.MaxPooling2D(pool_size=(3, 3), strides=(2, 2), padding='same')(x)

    x = Inception(x, nb_filter=64)  # 256
    x = Inception(x, nb_filter=120)  # 480
    x = tf.keras.layers.MaxPooling2D(pool_size=(3, 3), strides=(2, 2), padding='same')(x)

    x = Inception(x, nb_filter=128)  # 512
    x = Inception(x, nb_filter=128)
    x = Inception(x, nb_filter=128)
    x = Inception(x, nb_filter=132)  # 528
    x = Inception(x, nb_filter=208)  # 832
    x = tf.keras.layers.MaxPooling2D(pool_size=(3, 3), strides=(2, 2), padding='same')(x)

    x = Inception(x, nb_filter=208)
    x = Inception(x, nb_filter=256)  # 1024

    x = tf.keras.layers.AveragePooling2D(pool_size=(7, 7), strides=(7, 7), padding='same')(x)
    x = tf.keras.layers.Dropout(0.4)(x)
    x = tf.keras.layers.Dense(1000, activation='relu')(x)
    x = tf.keras.layers.Dense(1000, activation='softmax')(x)
    model = tf.keras.models.Model(inpt, x, name='inception')
    return model

if __name__ == '__main__':
    GoogLeNet()