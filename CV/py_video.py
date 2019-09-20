import numpy as np
import cv2

#调用笔记本内置摄像头，所以参数为0，如果有其他的摄像头可以调整参数为1，2
cap=cv2.VideoCapture(0)

while True:
    sucess,img=cap.read()     #从摄像头读取图片

    # gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)    #转为灰度图片
    # cv2.imshow("img",gray)    #显示摄像头，背景是灰度。

    cv2.imshow("img",img)

    k=cv2.waitKey(1)    #保持画面的持续。
    if k == 27:
        cv2.destroyAllWindows()    #通过esc键退出摄像
        break
    elif k==ord("s"):
        cv2.imwrite("image2.jpg",img)   #通过s键保存图片，并退出。
        cv2.destroyAllWindows()
        break

#关闭摄像头
cap.release()