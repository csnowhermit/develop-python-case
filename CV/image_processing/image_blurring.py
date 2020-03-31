import cv2
import matplotlib.pyplot as plt
import numpy as np

'''
    图像模糊化
    cv2.bulr()：均值模糊；
    cv2.boxfilter()：方框滤波；
    cv2.Guassiannblur()：高斯模糊；
    cv2.()：中值模糊；
    
    模糊化：溶解噪声，平滑边缘。
    双边滤波：去除噪声的同时保持边缘锐化。原因：它不仅使用高斯分布值，同时考虑了距离和像素值的差异。因此需要指定sigmaSpace和sigmaColor两个参数。
'''

# Import the image and convert to RGB
# file = "C:/Users/ASUS/Desktop/广州南站.jpg"
file = "D:/logs/before.jpg"
img = cv2.imdecode(np.fromfile(file, dtype=np.uint8), cv2.IMREAD_COLOR)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# Plot the image with different kernel sizes
kernels = [5, 11, 17]
fig, axs = plt.subplots(nrows = 1, ncols = 3, figsize = (20, 20))
for ind, s in enumerate(kernels):
    img_blurred = cv2.blur(img, ksize = (s, s))
    ax = axs[ind]
    ax.imshow(img_blurred)
    ax.axis('off')
plt.show()

img_0 = cv2.blur(img, ksize = (7, 7))    # 均值模糊
img_1 = cv2.GaussianBlur(img, ksize = (7, 7), sigmaX = 0)    # 高斯模糊
img_2 = cv2.medianBlur(img, 7)    # 中值模糊
img_3 = cv2.bilateralFilter(img, 7, sigmaSpace = 75, sigmaColor =75)    # 双边滤波（相比前三者，双边滤波最清晰）
# Plot the images
images = [img_0, img_1, img_2, img_3]
fig, axs = plt.subplots(nrows = 1, ncols = 4, figsize = (20, 20))
for ind, p in enumerate(images):
    ax = axs[ind]
    ax.imshow(p)
    ax.axis('off')
plt.show()

for ind, im in enumerate(images):
    # plt.show(im)
    im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
    cv2.imwrite("image_blurring_img_" + str(ind) + ".jpg", im)