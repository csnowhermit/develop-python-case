import cv2
import matplotlib.pyplot as plt
import numpy as np

'''
    图像的开闭运算，参考：https://homepages.inf.ed.ac.uk/rbf/HIPR2/morops.htm
    开运算：先腐蚀，再扩张；
    闭运算：先扩张，再腐蚀；
'''

# file = "C:/Users/ASUS/Desktop/广州南站.jpg"
file = "D:/logs/before.jpg"
img = cv2.imdecode(np.fromfile(file, dtype=np.uint8), cv2.IMREAD_COLOR)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Apply the operations
kernel = np.ones((9, 9), np.uint8)
img_open = cv2.morphologyEx(img, op= cv2.MORPH_OPEN, kernel=kernel)          # 开运算：先腐蚀，后扩张
img_close = cv2.morphologyEx(img, op= cv2.MORPH_CLOSE, kernel=kernel)        # 闭运算：先扩张，后腐蚀
img_grad = cv2.morphologyEx(img, op= cv2.MORPH_GRADIENT, kernel=kernel)      # 梯度滤波：扩张结果图与腐蚀结果图之差
img_tophat = cv2.morphologyEx(img, op= cv2.MORPH_TOPHAT, kernel=kernel)      # 顶帽：开运算结果图与原始图像之差
img_blackhat = cv2.morphologyEx(img, op= cv2.MORPH_BLACKHAT, kernel=kernel)  # 黑帽：闭运算结果图与原始图像之差

# Plot the images
images = [img, img_open, img_close, img_grad,
          img_tophat, img_blackhat]
fig, axs = plt.subplots(nrows = 2, ncols = 3, figsize = (15, 15))
for ind, p in enumerate(images):
    # print(ind//3, ind%3)
    ax = axs[ind//3, ind%3]    # 子图像按行摆放
    ax.imshow(p, cmap = 'gray')
    ax.axis('off')
plt.show()

for ind, im in enumerate(images):
    im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
    cv2.imwrite("image_open_close_" + str(ind//3) + "_" + str(ind%3) + ".jpg", im)