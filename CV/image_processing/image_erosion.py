import cv2
import matplotlib.pyplot as plt
import numpy as np

'''
    形态转换：图像腐蚀（Erosion），一种缩小图形形态的技术，通常用在灰度图上。
    过滤器的形状可以是矩形、椭圆和交叉形状，通过过滤器删除给定区域下的全部0值。
'''

# file = "C:/Users/ASUS/Desktop/广州南站.jpg"
file = "D:/logs/before.jpg"
img = cv2.imdecode(np.fromfile(file, dtype=np.uint8), cv2.IMREAD_COLOR)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Create erosion kernels
kernel_0 = np.ones((9, 9), np.uint8)    # 矩形过滤器
kernel_1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))    # 椭圆形过滤器
kernel_2 = cv2.getStructuringElement(cv2.MORPH_CROSS, (9, 9))    # 交叉形状
kernels = [kernel_0, kernel_1, kernel_2]

# Plot the images
plt.figure(figsize = (20, 20))
for i in range(len(kernels)):
    img_copy = img.copy()
    img_copy = cv2.erode(img_copy, kernels[i], iterations = 3)

    cv2.imwrite("image_erosion_" + str(i) + ".jpg", cv2.cvtColor(img_copy, cv2.COLOR_RGB2BGR))
    plt.subplot(1, 3, i+1)
    plt.imshow(img_copy)
    plt.axis('off')
plt.show()