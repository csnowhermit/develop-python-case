import cv2
import matplotlib.pyplot as plt
import numpy as np

'''
    自适应阀值化
'''

# file = "C:/Users/ASUS/Desktop/广州南站.jpg"
file = "D:/logs/loss.jpg"
img = cv2.imdecode(np.fromfile(file, dtype=np.uint8), cv2.IMREAD_COLOR)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

_, thresh_binary = cv2.threshold(img, thresh = 127, maxval = 255, type = cv2.THRESH_BINARY)
adap_mean_2 = cv2.adaptiveThreshold(img, 255,
                                    cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY, 7, C=2)
adap_mean_2_inv = cv2.adaptiveThreshold(img, 255,
                                        cv2.ADAPTIVE_THRESH_MEAN_C,
                                        cv2.THRESH_BINARY_INV, 7, C=2)
adap_mean_8 = cv2.adaptiveThreshold(img, 255,
                                    cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY, 7, C=8)
adap_gaussian_8 = cv2.adaptiveThreshold(img, 255,
                                    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY, 7, C=8)    # 当C越大时，图像越显式。C表示从均值或加权均值中减去值的大小。

images = [img, thresh_binary, adap_mean_2, adap_mean_2_inv,
          adap_mean_8, adap_gaussian_8]
fig, axs = plt.subplots(nrows = 2, ncols = 3, figsize = (15, 15))
for ind, p in enumerate(images):
    # print(ind%2, ind//2)
    ax = axs[ind%2, ind//2]    # 子图像按列摆放
    ax.imshow(p, cmap = 'gray')
    ax.axis('off')
plt.show()

for ind, im in enumerate(images):
    im = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)
    cv2.imwrite("image_adaptive_thresholding_img_" + str(ind%2) + "_" + str(ind//2) + ".jpg", im)