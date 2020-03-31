import cv2
import matplotlib.pyplot as plt
import numpy as np

'''
    角点检测：Harris角点检测、Shi-Tomasi角点检测
    算法：检测到各个方向上像素强度有很大变化的点，构建矩阵，提取特征值，通过特征值进行评分决定它是否是一个角。
'''

file = "C:/Users/ASUS/Desktop/广州南站.jpg"
# file = "D:/logs/before.jpg"
img = cv2.imdecode(np.fromfile(file, dtype=np.uint8), cv2.IMREAD_COLOR)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

harris_dst = cv2.cornerHarris(img_gray, blockSize = 2, ksize = 3, k = .04)    # Harris角点检测
img_2 = img.copy()
img_2[harris_dst > 0.01 * harris_dst.max()] = [255, 0, 0]    # 用红色标注出角点

cv2.imwrite("image_corner_detect_harris.jpg", cv2.cvtColor(img_2, cv2.COLOR_RGB2BGR))
plt.figure(figsize = (20, 20))
plt.subplot(1, 2, 1); plt.imshow(img)
plt.axis('off')
plt.subplot(1, 2, 2); plt.imshow(img_2)
plt.axis('off')
plt.show()

# Shi-Tomasi角点检测
corners = cv2.goodFeaturesToTrack(img_gray, maxCorners = 50,
                                  qualityLevel = 0.01,
                                  minDistance = 10)
corners = np.int0(corners)
# Spot the detected corners
img_2 = img.copy()
for i in corners:
    x,y = i.ravel()
    cv2.circle(img_2, center = (x, y),
               radius = 5, color = 255, thickness = -1)
cv2.imwrite("image_corner_detect_shi-Tomasi.jpg", cv2.cvtColor(img_2, cv2.COLOR_RGB2BGR))
plt.figure(figsize = (20, 20))
plt.subplot(1, 2, 1); plt.imshow(img)
plt.axis('off')
plt.subplot(1, 2, 2); plt.imshow(img_2)
plt.axis('off')
plt.show()