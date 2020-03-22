import matplotlib.pyplot as plt
import tensorflow as tf

'''
    调整图片的大小
    原始图像的大小不固定，但神经网络的输入节点个数是固定的。
    所以在将图像的像素作为输入提供给神经网络之前，需要将图像的大小统一，这是需要进行大小调整。
    图像大小调整：通过算法使得新图像尽量保存原始图像的所有信息。
    TensorFlow提供了4种不同的方法，在tf.image.resize_images()函数中。
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

    # 1.将图片数据转化成实属类型。这一步将0-255的像素值转化为0.0-1.0范围内的实数。
    # 大多数图像处理API支持整数和实数类型的输入。如果输入为整数，则会在内部转为实数后处理，再将输出转为整数。
    # 如果处理步骤过多，则在整数和实数之间反复转换将导致精度损失，因此推荐在图像处理前转为实属类型。
    img_data = tf.image.convert_image_dtype(img_data, dtype=tf.float32)

    # 2.通过tf.image.resize_images()调整图像的大小。
    # 注意：如果输入数据为unit8格式，那么输出为0～255之内的实数，不方便后续处理。
    # method=0：双线性插值法
    resized = tf.image.resize_images(img_data, [300, 300], method=0)

    # 3.通过pyplot将resize后的图像可视化
    plt.imshow(resized.eval())
    plt.title(u"method=0：双线性插值法")
    plt.show()

    # method=1：最近邻居法
    resized = tf.image.resize_images(img_data, [300, 300], method=1)

    # 3.通过pyplot将resize后的图像可视化
    plt.imshow(resized.eval())
    plt.title(u"method=1：最近邻居法")
    plt.show()

    # method=2：双三次插值法
    resized = tf.image.resize_images(img_data, [300, 300], method=2)

    # 3.通过pyplot将resize后的图像可视化
    plt.imshow(resized.eval())
    plt.title(u"method=2：双三次插值法")
    plt.show()

    # method=3：面积插值法
    resized = tf.image.resize_images(img_data, [300, 300], method=3)

    # 3.通过pyplot将resize后的图像可视化
    plt.imshow(resized.eval())
    plt.title(u"method=3：面积插值法")
    plt.show()

    # tf.image.resize_image_with_crop_or_pad()函数调整图像大小
    # 原图像：1440*900；当目标图像大小小于原图像时，自动截取图像居中部分；当目标图像大小大于原图像时，在四周自动填充0背景；
    croped = tf.image.resize_image_with_crop_or_pad(img_data, 1000, 1000)
    padded = tf.image.resize_image_with_crop_or_pad(img_data, 3000, 3000)

    plt.imshow(croped.eval())
    plt.title(u"croped")
    plt.show()

    plt.imshow(padded.eval())
    plt.title(u"padded")
    plt.show()

    # 按比例裁剪图像
    central_cropped = tf.image.central_crop(img_data, 0.5)
    plt.imshow(central_cropped.eval())
    plt.title(u"central_cropped：按比例裁剪图像")
    plt.show()