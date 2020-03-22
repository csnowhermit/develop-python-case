import matplotlib.pyplot as plt
import tensorflow as tf

'''
    TensorFlow读取图片（RGB色彩模式）
'''

# 读取图像的原始数据，二进制读取
image_row_data = tf.gfile.FastGFile('./xp.jpg', 'rb').read()

with tf.Session() as sess:
    img_data = tf.image.decode_jpeg(image_row_data)    # 对图像进行jpeg的格式解码得到图像对应的三维矩阵
    print(img_data.eval())    # 输出解码之后的三维矩阵

    # 使用pyplot工具可视化得到的图像
    plt.imshow(img_data.eval())
    plt.show()

    # 将表示一张图像的三维矩阵重新按照jpeg格式编码并存入文件中。打开这张图像，可以得到和原图像一样的图像。
    encoded_image = tf.image.encode_jpeg(img_data)
    with tf.gfile.GFile('./newxp.jpg', 'wb') as f:
        f.write(encoded_image.eval())
