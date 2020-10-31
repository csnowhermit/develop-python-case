import cv2
import matplotlib.pyplot as plt
import numpy as np

'''
    边缘检测：Canny算法（目前最流行）
    1.使用高斯模糊技术实现降噪：消除噪音的影响；
    2.使用Sobel算子计算梯度；
    3.nms：使用得到的梯度，检测每个像素点及周围像素点，确认该像素点是不是这些局部像素点的最大值，如果不是，则将该点的像素值置为0（完全缺失，黑色）；
    4.需要两个阀值：较小阀值和较大阀值
        if < 较小阀值：非边缘点，丢弃；
        elif > 较大阀值：边缘点；
        else：（介于两者之间），根据其是否与“确认边缘点”之间有无连接来确定，有连接则不丢弃。
'''

file = "G:/workspace/workspace_python/mx_AI/passflow-detect/ml/10.6.8.181_01_20200403174021755.mp4_frame_1610.jpg"
# file = "D:/logs/before.jpg"    # 车厢监控下的图像不需要做bluring（不做bluring时边缘检测效果更好）
img = cv2.imdecode(np.fromfile(file, dtype=np.uint8), cv2.IMREAD_COLOR)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

med_val = np.median(img)    # 基于中值，得到较小阀值和较大阀值
lower = int(max(0, .7*med_val))
upper = int(min(255, 1.3*med_val))

# 直接处理，without bluring
edges = cv2.Canny(image=img, threshold1=127, threshold2=127)

cv2.imwrite("image_edge_detect_without_bluring.jpg", cv2.cvtColor(edges, cv2.COLOR_RGB2BGR))

plt.figure(figsize = (20, 20))
plt.subplot(1, 2, 1); plt.imshow(img)
plt.axis('off')
plt.subplot(1, 2, 2); plt.imshow(edges)
plt.axis('off')
plt.show()

# # 先模糊化再Canny
# # Blurring with ksize = 5
# img_k5 = cv2.blur(img, ksize = (5, 5))
# # Canny detection with different thresholds
# edges_k5 = cv2.Canny(img_k5, threshold1 = lower, threshold2 = upper)
# edges_k5_2 = cv2.Canny(img_k5, lower, upper+100)
#
# # Blurring with ksize = 9，噪音较大时应用较大阀值，处理效果更好
# img_k9 = cv2.blur(img, ksize = (9, 9))
# # Canny detection with different thresholds
# edges_k9 = cv2.Canny(img_k9, lower, upper)
# edges_k9_2 = cv2.Canny(img_k9, lower, upper+100)
#
# # Plot the images
# images = [edges_k5, edges_k5_2, edges_k9, edges_k9_2]
# plt.figure(figsize = (20, 15))
# for i in range(4):
#     cv2.imwrite("image_edge_detect_with_bluring_" + str(i+1) + ".jpg", cv2.cvtColor(images[i], cv2.COLOR_RGB2BGR))
#     plt.subplot(2, 2, i+1)    # 2行2列，位置是i+1的子图
#     plt.imshow(images[i])
#     plt.axis('off')
# plt.show()