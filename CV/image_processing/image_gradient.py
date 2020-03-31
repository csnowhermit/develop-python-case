import cv2
import matplotlib.pyplot as plt
import numpy as np

'''
    图像梯度
    拉普拉斯计算：使用两个方向上的二阶导数
'''

# file = "C:/Users/ASUS/Desktop/广州南站.jpg"
file = "D:/logs/before.jpg"
img = cv2.imdecode(np.fromfile(file, dtype=np.uint8), cv2.IMREAD_COLOR)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

sobel_x = cv2.Sobel(img, cv2.CV_64F, dx = 1, dy = 0, ksize = 5)    # x方向上做高斯平滑和梯度（清楚看到垂直方向的边缘）
sobel_y = cv2.Sobel(img, cv2.CV_64F, dx = 0, dy = 1, ksize = 5)    # y方向上做高斯平滑和梯度（清楚看到水平方向的边缘）
blended = cv2.addWeighted(src1=sobel_x, alpha=0.5,
                          src2=sobel_y, beta=0.5, gamma=0)    # 两个方向过滤器加权求和，实现两个方向上的梯度求解及图像滤波
laplacian = cv2.Laplacian(img, cv2.CV_64F)    # 做拉普拉斯计算（两个方向都有）

# Plot the images
images = [sobel_x, sobel_y, blended, laplacian]
plt.figure(figsize = (20, 20))
for i in range(len(images)):
    plt.subplot(1, 4, i+1)
    plt.imshow(images[i], cmap = 'gray')
    plt.axis('off')
plt.show()

for i in range(len(images)):
    # im = cv2.cvtColor(images[i], cv2.COLOR_GRAY2BGR)
    cv2.imwrite("image_gradient_img_" + str(i) + ".jpg", images[i])