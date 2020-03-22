import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np

'''
    图像色彩调整
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

    # 将图像亮度-0.5
    adjusted = tf.image.adjust_brightness(img_data, -0.5)
    plt.imshow(adjusted.eval())
    plt.title(u"图像亮度-0.5")
    plt.show()

    '''
        色彩调整的API可能导致像素的实数值超出0.0～1.0的范围，因此在输出最终图像前需要将其值clip(0.0, 1.0)，
        否则图像不仅无法正常可视化，以此为输入的神经网络的训练质量也可能受到影响。
    '''
    '''
        如果对图像进行多项处理操作，那么这一截断过程应当在所有处理完成后进行。
        举例而言，假如对图像依次提高亮度和减少对比度，那么第二个操作可能将第一个操作生成的部分过亮的像素拉回到不超过1.0的范围内，因此在第一个操作后不应该立即截断。
    '''

    # # 截断操作在最终可视化图像前进行
    # adjusted = tf.clip_by_value(np.array(adjusted), 0.0, 1.0)
    # plt.imshow(adjusted.eval())
    # plt.title(u"图像亮度-0.5, clip_by_value(0.0, 1.0)")
    # plt.show()

    # 将图像亮度+0.5
    adjusted = tf.image.adjust_brightness(img_data, 0.5)
    plt.imshow(adjusted.eval())
    plt.title(u"图像亮度+0.5")
    plt.show()

    # 在[-max_delta, max_delta]的范围内随机调整图像的亮度
    x = np.random.rand(1, 1)[0][0]
    adjusted = tf.image.random_brightness(img_data, max_delta=x)
    plt.imshow(adjusted.eval())
    plt.title(u"图像亮度随机调整：%s" % x)
    plt.show()

    # 如何调整图像的对比度
    # 将图像的对比度减少到0.5倍
    adjusted = tf.image.adjust_contrast(img_data, 0.5)
    plt.imshow(adjusted.eval())
    plt.title(u"图像对比度减少到0.5倍")
    plt.show()

    # 将图像的对比度增加到5倍
    adjusted = tf.image.adjust_contrast(img_data, 5)
    plt.imshow(adjusted.eval())
    plt.title(u"图像对比度增加到5倍")
    plt.show()

    # 在[lower, upper]的范围内随机调整图像的亮度
    lower, upper = 0.5, 5
    x = np.random.rand(1, 1)[0][0]
    adjusted = tf.image.random_contrast(img_data, lower, upper)
    plt.imshow(adjusted.eval())
    plt.title(u"图像对比度随机调整：%s" % x)
    plt.show()

    # 调整图像的色相：色相分别相加0.1，0.3，0.6，0.9
    arr = [0.1, 0.3, 0.6, 0.9]
    for x in arr:
        adjusted = tf.image.adjust_hue(img_data, x)
        plt.imshow(adjusted.eval())
        plt.title(u"图像色相调整：%s" % x)
        plt.show()

    # 在[-max_delta, max_delta]的范围内随机调整图像色相
    x = np.random.rand(1, 1)[0][0]
    adjusted = tf.image.random_hue(img_data, max_delta=x)
    plt.imshow(adjusted.eval())
    plt.title(u"图像色相随机调整：%s" % x)
    plt.show()

    # 调整图像的饱和度
    # 图像饱和度-5
    adjusted = tf.image.adjust_saturation(img_data, -5)
    plt.imshow(adjusted.eval())
    plt.title(u"图像饱和度-5")
    plt.show()

    # 图像饱和度+5
    adjusted = tf.image.adjust_saturation(img_data, 5)
    plt.imshow(adjusted.eval())
    plt.title(u"图像饱和度+5")
    plt.show()

    # 在[lower, upper]的范围内随机调整图像的饱和度
    lower, upper = 0.5, 5
    x = np.random.rand(1, 1)[0][0]
    adjusted = tf.image.random_saturation(img_data, lower, upper)
    plt.imshow(adjusted.eval())
    plt.title(u"图像饱和度随机调整：%s" % x)
    plt.show()



