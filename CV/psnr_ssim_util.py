import math
import os
import cv2
import numpy as np
from scipy.signal import convolve2d

'''
    计算两个图像的PSNR：峰值信噪比，值越大，图像失真越小。最大为100。
'''
def PSNR(img1, img2):
    mse = np.mean((img1/1.0 - img2/1.0) ** 2)
    if mse < 1.0e-10:
        return 100
    return 10 * math.log10(255.0**2/mse)


def matlab_style_gauss2D(shape=(3, 3), sigma=0.5):
    """
    2D gaussian mask - should give the same result as MATLAB's
    fspecial('gaussian',[shape],[sigma])
    """
    m, n = [(ss - 1.) / 2. for ss in shape]
    y, x = np.ogrid[-m:m + 1, -n:n + 1]
    h = np.exp(-(x * x + y * y) / (2. * sigma * sigma))
    h[h < np.finfo(h.dtype).eps * h.max()] = 0
    sumh = h.sum()
    if sumh != 0:
        h /= sumh
    return h


def filter2(x, kernel, mode='same'):
    return convolve2d(x, np.rot90(kernel, 2), mode=mode)

'''
    计算图像的SSIM：结构相似性，衡量亮度、对比度、结构。值越大越好，最大为1。
'''
def compute_ssim(im1, im2, k1=0.01, k2=0.03, win_size=11, L=255):
    if not im1.shape == im2.shape:
        raise ValueError("Input Imagees must have the same dimensions")
    if len(im1.shape) > 2:
        raise ValueError("Please input the images with 1 channel")

    M, N = im1.shape
    C1 = (k1 * L) ** 2
    C2 = (k2 * L) ** 2
    window = matlab_style_gauss2D(shape=(win_size, win_size), sigma=1.5)
    window = window / np.sum(np.sum(window))

    if im1.dtype == np.uint8:
        im1 = np.double(im1)
    if im2.dtype == np.uint8:
        im2 = np.double(im2)

    mu1 = filter2(im1, window, 'valid')
    mu2 = filter2(im2, window, 'valid')
    mu1_sq = mu1 * mu1
    mu2_sq = mu2 * mu2
    mu1_mu2 = mu1 * mu2
    sigma1_sq = filter2(im1 * im1, window, 'valid') - mu1_sq
    sigma2_sq = filter2(im2 * im2, window, 'valid') - mu2_sq
    sigmal2 = filter2(im1 * im2, window, 'valid') - mu1_mu2

    ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigmal2 + C2)) / ((mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2))

    return np.mean(np.mean(ssim_map))

if __name__ == '__main__':
    # lr_path = "D:/testdata/srgan_input/"
    origin_path = "./datasets/cityscapes/train_img"    # 原图
    fake_path = "./results/label2city_1024p/test_latest/images/"    # fake图
    PSNRList = []
    SSIMList = []

    for file in os.listdir(origin_path):
        prefix = file[0:21]
        # print(prefix)

        origin_file = prefix + "leftImg8bit.png"
        fake_file = prefix + "gtFine_labelIds_synthesized_image.jpg"

        img1 = cv2.imread(os.path.join(origin_path, origin_file))
        img2 = cv2.imread(os.path.join(fake_path, fake_file))
        print(img1.shape, img2.shape)
        psnr = PSNR(img1, img2)
        PSNRList.append(psnr)
        print("\tPSNR:", psnr)

        # 转为单通道图
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        ssim = compute_ssim(img1, img2)
        SSIMList.append(ssim)
        print("\tSSIM:", ssim)

    print("final:")
    print("mean psnr:", np.mean(PSNRList))
    print("mean ssim:", np.mean(SSIMList))
