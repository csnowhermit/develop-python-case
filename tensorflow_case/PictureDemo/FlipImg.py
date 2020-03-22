import matplotlib.pyplot as plt
import tensorflow as tf

'''
    图像翻转
'''

# 读取图像的原始数据，二进制读取
image_row_data = tf.gfile.FastGFile('./xp.jpg', 'rb').read()

with tf.Session() as sess:
    img_data = tf.image.decode_jpeg(image_row_data)    # 对图像进行jpeg的格式解码得到图像对应的三维矩阵
    print(img_data.eval())    # 输出解码之后的三维矩阵

    # 使plt.title()的中文正常显示
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 使用pyplot工具可视化得到的图像
    plt.imshow(img_data.eval())
    plt.title(u"原图像")
    plt.show()

    # 上下翻转
    flipped = tf.image.flip_up_down(img_data)
    plt.imshow(flipped.eval())
    plt.title(u"flipped：上下翻转")
    plt.show()

    # 左右翻转
    flipped = tf.image.flip_left_right(img_data)
    plt.imshow(flipped.eval())
    plt.title(u"flipped：左右翻转")
    plt.show()

    # 沿对角线翻转
    transposed = tf.image.transpose_image(img_data)
    plt.imshow(flipped.eval())
    plt.title(u"transposed：沿对角线翻转")
    plt.show()

    '''
        在很多图像识别问题中，图像的翻转不会影响识别的结果。
        所以在训练图像识别的神经网络模型时，可以随机地翻转训练图像，这样训练得到的模型可以识别不同角度的实体。
    '''
    # 以50%的概率上下翻转图像
    flipped = tf.image.random_flip_up_down(img_data)
    plt.imshow(flipped.eval())
    plt.title(u"flipped：以50%的概率上下翻转")
    plt.show()

    # 以50%的概率左右翻转图像
    flipped = tf.image.random_flip_left_right(img_data)
    plt.imshow(flipped.eval())
    plt.title(u"flipped：以50%的概率左右翻转")
    plt.show()
