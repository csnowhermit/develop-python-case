from PIL import Image
import math
import operator
from functools import reduce

'''
    图像对比：计算图像的差异值：越不一样，差异值越大
    通过math.sqrt(直方图)的方式计算差异值
'''

def image_contrast(img1, img2):

    image1 = Image.open(img1).convert('L')    # 打开并转为灰度图
    image2 = Image.open(img2).convert('L')

    h1 = image1.histogram()
    h2 = image2.histogram()

    result = math.sqrt(reduce(operator.add,  list(map(lambda a,b: (a-b)**2, h1, h2)))/len(h1) )
    return result

if __name__ == '__main__':
    left = "D:/logs/before_Laplacian.jpg"
    right = "D:/logs/laplacian.jpg"
    result = image_contrast(left, right)
    print(result)