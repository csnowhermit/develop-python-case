import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np

'''
    图像的标准化：将图像的亮度均值变为0，方差变为1
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

    # 将图像亮度的均值变为0，方差变为1
    adjusted = tf.image.per_image_standardization(img_data)
    plt.imshow(adjusted.eval())
    plt.title(u"标准化后")
    plt.show()


