import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np

'''
    图像处理：处理标注框
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

    # 将图像缩小一些，这样可视化让标注框更加清楚
    img_data = tf.image.resize_images(img_data, [180, 267], method=1)    # method=1，最近邻居法

    # tf.image.draw_bounding_boxes()函数要求图像矩阵中的数字为实数，所以需要先将图像矩阵转化为实数类型。
    # tf.image.draw_bounding_boxes()函数图像的输入是一个batch的数组，也就是多张图像组成的思维矩阵，所以需要将解码之后的图像矩阵加一维。
    batched = tf.expand_dims(tf.image.convert_image_dtype(img_data, tf.float32), 0)

    # 给出每一张图像的所有标注框。一个标注框有4个数字，分别代表[Ymin, Xmin, Ymax, Xma]，这里给出的数字都是图像的相对位置。
    # 比如在180*267的图像中，[0.35, 0.47, 0.5, 0.56]代表了从（63, 125）到（90, 150）的图像。
    boxes = tf.constant([[[0.05, 0.05, 0.9, 0.7], [0.35, 0.47, 0.5, 0.56]]])

    # 加上标注框
    result = tf.image.draw_bounding_boxes(batched, boxes)
    plt.imshow(img_data.eval())
    plt.title(u"加入了标注框的图像")
    plt.show()

    # 和随机翻转图像，随机调整颜色类似，随机截取图像上有信息含量的部分也是一个提高模型健壮性的一种方式。这样可以使训练得到的模型不受被识别物体大小的影响。
    # 通过tf.image.sample_distorted_bounding_box()函数完成随机截取图像的过程
    boxes = tf.constant([[[0.05, 0.05, 0.9, 0.7], [0.35, 0.47, 0.5, 0.56]]])
    # 通过提供标注框的方式来告诉随机截取图像的算法哪些部分是“有信息量”的
    begin, size, bbox_for_draw = tf.image.sample_distorted_bounding_box(
        tf.shape(img_data),
        bounding_boxes=boxes,
        min_object_covered=0.4    # 表示截取部分至少包含某个输入框40%的内容
    )

    # 通过标注框可视化截取的图像
    batched = tf.expand_dims(tf.image.convert_image_dtype(img_data, tf.float32), 0)
    image_with_box = tf.image.draw_bounding_boxes(batched, bbox_for_draw)

    # 随机截取出来的图像。因为算法有随机成分，所以每次得到的结果会有所不同。
    distored_image = tf.slice(img_data, begin, size)
    plt.imshow(distored_image.eval())
    plt.title(u"通过标注框随机截取的图像")
    plt.show()
