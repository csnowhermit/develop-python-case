import cv2
import matplotlib.pyplot as plt
import numpy as np

'''
    图像的阀值化：利用图像像素点分布规律，设定阀值进行像素点分割，进而得到图像的二值图像。
    只取一个阀值并不能满足我们全部需求。如果有一张在多个不同区域亮度差异较多的情况，则将一个值应用于整个图像不利于我们的图像处理任务。
    so，自适应阀值化，通过对图像邻域内阀值的计算，可以得到不同光照条件下的较好效果。
'''

file = "C:/Users/ASUS/Desktop/广州南站.jpg"
# file = "D:/logs/before.jpg"
img = cv2.imdecode(np.fromfile(file, dtype=np.uint8), cv2.IMREAD_COLOR)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

_, thresh_0 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)        # 二进制阀值化
_, thresh_1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)    # 反二进制阀值化
_, thresh_2 = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO)        # 阀值化到0
_, thresh_3 = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO_INV)    # 反阀值化到0
_, thresh_4 = cv2.threshold(img, 127, 255, cv2.THRESH_TRUNC)         # 阀值截断
# Plot the images
images = [img, thresh_0, thresh_1, thresh_2, thresh_3, thresh_4]
fig, axs = plt.subplots(nrows = 2, ncols = 3, figsize = (13, 13))
for ind, p in enumerate(images):
    # print(ind//3, ind%3)
    ax = axs[ind//3, ind%3]    # 子图像按行摆放
    ax.imshow(p)
plt.show()

for ind, im in enumerate(images):
    im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
    cv2.imwrite("image_thresholding_img_" + str(ind//3) + "_" + str(ind%3) + ".jpg", im)