
import tensorflow as tf

'''
    LeNet-5的keras实现
    LeNet-5：conv1-->pool-->conv2-->pool2-->fc
'''

model = tf.keras.models.Sequential([
    # conv1，20个特征图，卷积核5×5，步长strides=1，input_shape=(h, w, c)
    tf.keras.layers.Conv2D(20, (5, 5), strides=1, input_shape=(28, 28, 1),
                           padding='valid', activation='relu', kernel_initializer='uniform'),     # conv1之后：20*24*24

    tf.keras.layers.MaxPooling2D(pool_size=(2, 2), strides=2),     # maxPool：20*12*12

    tf.keras.layers.Conv2D(50, (5, 5), strides=1, input_shape=(12, 12, 1),
                           padding='valid', activation='relu', kernel_initializer='uniform'),     # conv2之后：50*8*8

    tf.keras.layers.MaxPooling2D((2, 2), strides=2),     # pool2：50*4*4

    tf.keras.layers.Flatten(),     # 扁平化

    tf.keras.layers.Dense(500, activation='relu'),     # 全连接层，激活函数用relu：神经元数目500

    tf.keras.layers.Dense(10, activation='softmax')    # 第二个全连接层，激活函数用softmax（将输出变为各类别的概率分布）：神经元数目10
])

# 网上的实现
def LeNet():
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Conv2D(32,(5,5),strides=(1,1),input_shape=(28,28,1),padding='valid',activation='relu',kernel_initializer='uniform'))
    model.add(tf.keras.layers.MaxPooling2D(pool_size=(2,2)))
    model.add(tf.keras.layers.Conv2D(64,(5,5),strides=(1,1),padding='valid',activation='relu',kernel_initializer='uniform'))
    model.add(tf.keras.layers.MaxPooling2D(pool_size=(2,2)))
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(100,activation='relu'))
    model.add(tf.keras.layers.Dense(10,activation='softmax'))
    return model

if __name__ == '__main__':
    LeNet()