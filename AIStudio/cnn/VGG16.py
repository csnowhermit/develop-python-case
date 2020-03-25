import tensorflow as tf

'''
    VGG16的keras实现
    VGG16：13 conv + 3 fc
'''

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(64, (3, 3), strides=(1, 1), input_shape=(224, 224, 3),
                           padding='same', activation='relu', kernel_initializer='uniform'),
    tf.keras.layers.Conv2D(64, (3, 3), strides=(1, 1),
                           padding='same', activation='relu', kernel_initializer='uniform'),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

    tf.keras.layers.Conv2D(128, (3, 3), strides=(1, 1),
                           padding='same', activation='relu', kernel_initializer='uniform'),
    tf.keras.layers.Conv2D(128, (3, 3), strides=(1, 1),
                           padding='same', activation='relu', kernel_initializer='uniform'),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

    tf.keras.layers.Conv2D(256, (3, 3), strides=(1, 1),
                           padding='same', activation='relu', kernel_initializer='uniform'),
    tf.keras.layers.Conv2D(256, (3, 3), strides=(1, 1),
                           padding='same', activation='relu', kernel_initializer='uniform'),
    tf.keras.layers.Conv2D(256, (3, 3), strides=(1, 1),
                           padding='same', activation='relu', kernel_initializer='uniform'),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

    tf.keras.layers.Conv2D(512, (3, 3), strides=(1, 1),
                           padding='same', activation='relu', kernel_initializer='uniform'),
    tf.keras.layers.Conv2D(512, (3, 3), strides=(1, 1),
                           padding='same', activation='relu', kernel_initializer='uniform'),
    tf.keras.layers.Conv2D(512, (3, 3), strides=(1, 1),
                           padding='same', activation='relu', kernel_initializer='uniform'),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

    tf.keras.layers.Conv2D(512, (3, 3), strides=(1, 1),
                           padding='same', activation='relu', kernel_initializer='uniform'),
    tf.keras.layers.Conv2D(512, (3, 3), strides=(1, 1),
                           padding='same', activation='relu', kernel_initializer='uniform'),
    tf.keras.layers.Conv2D(512, (3, 3), strides=(1, 1),
                           padding='same', activation='relu', kernel_initializer='uniform'),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

    tf.keras.layers.Flatten(),     # 扁平化
    tf.keras.layers.Dense(4096, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(4096, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(1000, activation='softmax')    # 输出层，将输出值转成概率分布
])


def VGG_16():
    model = tf.keras.models.Sequential()

    model.add(tf.keras.layers.Conv2D(64, (3, 3), strides=(1, 1), input_shape=(224, 224, 3), padding='same', activation='relu',
                     kernel_initializer='uniform'))
    model.add(tf.keras.layers.Conv2D(64, (3, 3), strides=(1, 1), padding='same', activation='relu', kernel_initializer='uniform'))
    model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(tf.keras.layers.Conv2D(128, (3, 3), strides=(1, 1), padding='same', activation='relu', kernel_initializer='uniform'))
    model.add(tf.keras.layers.Conv2D(128, (3, 3), strides=(1, 1), padding='same', activation='relu', kernel_initializer='uniform'))
    model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(tf.keras.layers.Conv2D(256, (3, 3), strides=(1, 1), padding='same', activation='relu', kernel_initializer='uniform'))
    model.add(tf.keras.layers.Conv2D(256, (3, 3), strides=(1, 1), padding='same', activation='relu', kernel_initializer='uniform'))
    model.add(tf.keras.layers.Conv2D(256, (3, 3), strides=(1, 1), padding='same', activation='relu', kernel_initializer='uniform'))
    model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(tf.keras.layers.Conv2D(512, (3, 3), strides=(1, 1), padding='same', activation='relu', kernel_initializer='uniform'))
    model.add(tf.keras.layers.Conv2D(512, (3, 3), strides=(1, 1), padding='same', activation='relu', kernel_initializer='uniform'))
    model.add(tf.keras.layers.Conv2D(512, (3, 3), strides=(1, 1), padding='same', activation='relu', kernel_initializer='uniform'))
    model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(tf.keras.layers.Conv2D(512, (3, 3), strides=(1, 1), padding='same', activation='relu', kernel_initializer='uniform'))
    model.add(tf.keras.layers.Conv2D(512, (3, 3), strides=(1, 1), padding='same', activation='relu', kernel_initializer='uniform'))
    model.add(tf.keras.layers.Conv2D(512, (3, 3), strides=(1, 1), padding='same', activation='relu', kernel_initializer='uniform'))
    model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(4096, activation='relu'))
    model.add(tf.keras.layers.Dropout(0.5))
    model.add(tf.keras.layers.Dense(4096, activation='relu'))
    model.add(tf.keras.layers.Dropout(0.5))
    model.add(tf.keras.layers.Dense(1000, activation='softmax'))

    return model

if __name__ == '__main__':
    VGG_16()