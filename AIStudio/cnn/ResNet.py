
import tensorflow as tf

'''
    ResNet网络的keras实现
'''

def Conv2d_BN(x, nb_filter, kernel_size, strides=(1, 1), padding='same', name=None):
    if name is not None:
        bn_name = name + '_bn'
        conv_name = name + '_conv'
    else:
        bn_name = None
        conv_name = None

    x = tf.keras.layers.Conv2D(nb_filter, kernel_size, padding=padding, strides=strides, activation='relu', name=conv_name)(x)
    x = tf.keras.layers.BatchNormalization(axis=3, name=bn_name)(x)
    return x

'''
    :param with_conv_shortcut 传参，确定是否需要走shortcut
'''
def Conv_Block(inpt, nb_filter, kernel_size, strides=(1, 1), with_conv_shortcut=False):
    x = Conv2d_BN(inpt, nb_filter=nb_filter[0], kernel_size=(1, 1), strides=strides, padding='same')
    x = Conv2d_BN(x, nb_filter=nb_filter[1], kernel_size=(3, 3), padding='same')
    x = Conv2d_BN(x, nb_filter=nb_filter[2], kernel_size=(1, 1), padding='same')
    if with_conv_shortcut:
        shortcut = Conv2d_BN(inpt, nb_filter=nb_filter[2], strides=strides, kernel_size=kernel_size)
        x = tf.keras.layers.add([x, shortcut])
        return x
    else:
        x = tf.keras.layers.add([x, inpt])
        return x


def ResNet50():
    inpt = tf.keras.layers.Input(shape=(224, 224, 3))
    x = tf.keras.layers.ZeroPadding2D((3, 3))(inpt)    # 用0填充
    x = Conv2d_BN(x, nb_filter=64, kernel_size=(7, 7), strides=(2, 2), padding='valid')
    x = tf.keras.layers.MaxPooling2D(pool_size=(3, 3), strides=(2, 2), padding='same')(x)

    x = Conv_Block(x, nb_filter=[64, 64, 256], kernel_size=(3, 3), strides=(1, 1), with_conv_shortcut=True)
    x = Conv_Block(x, nb_filter=[64, 64, 256], kernel_size=(3, 3))
    x = Conv_Block(x, nb_filter=[64, 64, 256], kernel_size=(3, 3))

    x = Conv_Block(x, nb_filter=[128, 128, 512], kernel_size=(3, 3), strides=(2, 2), with_conv_shortcut=True)
    x = Conv_Block(x, nb_filter=[128, 128, 512], kernel_size=(3, 3))
    x = Conv_Block(x, nb_filter=[128, 128, 512], kernel_size=(3, 3))
    x = Conv_Block(x, nb_filter=[128, 128, 512], kernel_size=(3, 3))

    x = Conv_Block(x, nb_filter=[256, 256, 1024], kernel_size=(3, 3), strides=(2, 2), with_conv_shortcut=True)
    x = Conv_Block(x, nb_filter=[256, 256, 1024], kernel_size=(3, 3))
    x = Conv_Block(x, nb_filter=[256, 256, 1024], kernel_size=(3, 3))
    x = Conv_Block(x, nb_filter=[256, 256, 1024], kernel_size=(3, 3))
    x = Conv_Block(x, nb_filter=[256, 256, 1024], kernel_size=(3, 3))
    x = Conv_Block(x, nb_filter=[256, 256, 1024], kernel_size=(3, 3))

    x = Conv_Block(x, nb_filter=[512, 512, 2048], kernel_size=(3, 3), strides=(2, 2), with_conv_shortcut=True)
    x = Conv_Block(x, nb_filter=[512, 512, 2048], kernel_size=(3, 3))
    x = Conv_Block(x, nb_filter=[512, 512, 2048], kernel_size=(3, 3))
    x = tf.keras.layers.AveragePooling2D(pool_size=(7, 7))(x)
    x = tf.keras.layers.Flatten()(x)
    x = tf.keras.layers.Dense(1000, activation='softmax')(x)

    model = tf.keras.models.Model(inputs=inpt, outputs=x)
    return model

if __name__ == '__main__':
    ResNet50()