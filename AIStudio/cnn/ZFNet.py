import tensorflow as tf

'''
    ZF-Net的Keras实现
'''

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(96, (7, 7), strides=(2, 2), input_shape=(227, 227, 3),
                           padding='valid', activation='relu', kernel_initializer='uniform'),    # conv1
    tf.keras.layers.MaxPooling2D(pool_size=(3, 3), strides=(2, 2)),
    tf.keras.layers.Conv2D(256, (5, 5), strides=(2, 2),
                           padding='same', activation='relu', kernel_initializer='uniform'),    # conv2
    tf.keras.layers.MaxPooling2D(pool_size=(3, 3), strides=(2, 2)),
    tf.keras.layers.Conv2D(384, (3, 3), strides=(1, 1),
                           padding='same', activation='relu', kernel_initializer='uniform'),    # conv3
    tf.keras.layers.Conv2D(384, (3, 3), strides=(1, 1),
                           padding='same', activation='relu', kernel_initializer='uniform'),    # conv4
    tf.keras.layers.Conv2D(256, (3, 3), strides=(1, 1),
                           padding='same', activation='relu', kernel_initializer='uniform'),    # conv5
    tf.keras.layers.MaxPooling2D(pool_size=(3, 3), strides=(2, 2)),

    tf.keras.layers.Flatten(),     # 扁平化，准备全连接层

    tf.keras.layers.Dense(4096, activation='relu'),    # fc1
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(4096, activation='relu'),    # fc2
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(1000, activation='softmax')    # fc3
])

def AlexNet():
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Conv2D(96,(7,7),strides=(2,2),input_shape=(227,227,3),padding='valid',activation='relu',kernel_initializer='uniform'))
    model.add(tf.keras.layers.MaxPooling2D(pool_size=(3,3),strides=(2,2)))
    model.add(tf.keras.layers.Conv2D(256,(5,5),strides=(2,2),padding='same',activation='relu',kernel_initializer='uniform'))
    model.add(tf.keras.layers.MaxPooling2D(pool_size=(3,3),strides=(2,2)))
    model.add(tf.keras.layers.Conv2D(384,(3,3),strides=(1,1),padding='same',activation='relu',kernel_initializer='uniform'))
    model.add(tf.keras.layers.Conv2D(384,(3,3),strides=(1,1),padding='same',activation='relu',kernel_initializer='uniform'))
    model.add(tf.keras.layers.Conv2D(256,(3,3),strides=(1,1),padding='same',activation='relu',kernel_initializer='uniform'))
    model.add(tf.keras.layers.MaxPooling2D(pool_size=(3,3),strides=(2,2)))
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(4096,activation='relu'))
    model.add(tf.keras.layers.Dropout(0.5))
    model.add(tf.keras.layers.Dense(4096,activation='relu'))
    model.add(tf.keras.layers.Dropout(0.5))
    model.add(tf.keras.layers.Dense(1000,activation='softmax'))
    return model

if __name__ == '__main__':
    AlexNet()