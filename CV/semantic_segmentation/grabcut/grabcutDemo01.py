import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

'''
    grab cut方式进行图像语义分割
    分割之后的图：背景为黑色，其余地方不变
'''

img = cv2.imread('D:/data/ss/gz03c.jpg')
OLD_IMG = img.copy()
mask = np.zeros(img.shape[:2], np.uint8)
SIZE = (1, 65)
bgdModle = np.zeros(SIZE, np.float64)
fgdModle = np.zeros(SIZE, np.float64)
rect = (1, 1, img.shape[1], img.shape[0])
cv2.grabCut(img, mask, rect, bgdModle, fgdModle, 10, cv2.GC_INIT_WITH_RECT)

mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
img *= mask2[:, :, np.newaxis]

# plt.subplot(121), plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
# plt.title("grabcut"), plt.xticks([]), plt.yticks([])
# plt.subplot(122), plt.imshow(cv2.cvtColor(OLD_IMG, cv2.COLOR_BGR2RGB))
# plt.title("original"), plt.xticks([]), plt.yticks([])
#
# plt.show()

plt.imshow(img), plt.colorbar(), plt.show()
cv2.imwrite("D:/data/ss/gz03_new.jpg", img)