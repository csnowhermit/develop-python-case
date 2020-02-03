import os
from PIL import Image
from PIL import ImageChops
import cv2
import numpy as np

'''
    图像对比：输出两张图片的不同点到图片文件
'''

def compare_images(path_one, path_two, diff_save_location):
    """
    比较图片，如果有不同则生成展示不同的图片

    @参数一: path_one: 第一张图片的路径
    @参数二: path_two: 第二张图片的路径
    @参数三: diff_save_location: 不同图的保存路径
    """
    image_one = Image.open(path_one).convert('L')    # 打开并转为灰度图
    image_two = Image.open(path_two).convert('L')
    try:
        diff = ImageChops.difference(image_one, image_two)

        if diff.getbbox() is None:
            # 图片间没有任何不同则直接退出
            print("【+】We are the same!")
        else:
            diff.show(title="Compare")
            diff.save(diff_save_location)
    except ValueError as e:
        text = ("表示图片大小和box对应的宽度不一致，参考API说明：Pastes another image into this image."
                "The box argument is either a 2-tuple giving the upper left corner, a 4-tuple defining the left, upper, "
                "right, and lower pixel coordinate, or None (same as (0, 0)). If a 4-tuple is given, the size of the pasted "
                "image must match the size of the region.使用2纬的box避免上述问题")
        print("【{0}】{1}".format(e, text))

'''
    grabcut方法进行图片语义分析，并返回结果图片
'''
def grabcutImageAndSave(source_path):
    img = cv2.imread(source_path)
    OLD_IMG = img.copy()
    mask = np.zeros(img.shape[:2], np.uint8)
    SIZE = (1, 65)
    bgdModle = np.zeros(SIZE, np.float64)
    fgdModle = np.zeros(SIZE, np.float64)
    rect = (1, 1, img.shape[1], img.shape[0])
    cv2.grabCut(img, mask, rect, bgdModle, fgdModle, 10, cv2.GC_INIT_WITH_RECT)

    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    img *= mask2[:, :, np.newaxis]

    path = source_path[0:source_path.rfind("/") + 1]    # 目录
    filename = source_path[source_path.rfind("/") + 1: source_path.rfind(".")]    # 文件名
    postfix = source_path[source_path.rfind("."):]    # 后缀
    dest_path = os.path.join(path, filename + "_dest" + postfix)
    print("new filename: ", dest_path)

    cv2.imwrite(dest_path, img)    # 将处理过的图片保存至文件
    return dest_path

if __name__ == '__main__':
    # 原图比较
    left = "D:/data/ss/gz03.jpg"
    right = "D:/data/ss/gz03c.jpg"
    result = "D:/data/ss/我们不一样.jpg"
    # compare_images(left,
    #                right,
    #                result)    # 图片所有内容比较

    left_dest = grabcutImageAndSave(left)
    right_dest = grabcutImageAndSave(right)
    compare_images(left_dest,
                   right_dest,
                   result)      # 图像分割后部分比较（降低不必比较部分的噪音的干扰）

    from CV.pictureCompare.PictureCompareDemo02 import image_contrast

    similarityDegree = image_contrast(left_dest, right_dest)    # 计算两图片的差异值
    print("差异值", similarityDegree)