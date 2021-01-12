from CV.ImageStich.Stitcher import Stitcher
import cv2

'''
    图像拼接
    opencv包需降级：
        pip install opencv-python==3.4.2.16
        pip install opencv-contrib-python==3.4.2.16
'''

# 读取拼接图片：A为左，B为右
imageA = cv2.imread("left_01.png")
imageB = cv2.imread("right_01.png")


# 把图片拼接成全景图
stitcher = Stitcher()
(result, vis) = stitcher.stitch([imageA, imageB], showMatches=True)

# 显示所有图片
cv2.imshow("Image A", imageA)
cv2.imshow("Image B", imageB)
cv2.imshow("Keypoint Matches", vis)
cv2.imshow("Result", result)
cv2.waitKey(0)
cv2.destroyAllWindows()