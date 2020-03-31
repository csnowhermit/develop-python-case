import cv2
import matplotlib.pyplot as plt
import numpy as np

'''
    形态转换：图像扩张（Dilation），图像放大，
'''

# file = "C:/Users/ASUS/Desktop/广州南站.jpg"
file = "D:/logs/before.jpg"
img = cv2.imdecode(np.fromfile(file, dtype=np.uint8), cv2.IMREAD_COLOR)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Apply dilation
kernel = np.ones((9, 9), np.uint8)
img_dilate = cv2.dilate(img, kernel, iterations = 3)
plt.figure(figsize = (20, 10))

cv2.imwrite("image_dilation.jpg", img_dilate)
plt.subplot(1, 2, 1); plt.imshow(img, cmap="gray")
plt.subplot(1, 2, 2); plt.imshow(img_dilate, cmap="gray")
plt.show()