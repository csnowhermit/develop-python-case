import os
import cv2
import time
import numpy as np
import torch
from tqdm import tqdm
from argparse import ArgumentParser
from ibug.face_detection import RetinaFacePredictor
from ibug.face_parsing import FaceParser as RTNetPredictor
from ibug.face_parsing.utils import label_colormap


'''
    使用rtnet做人脸语义分割，支持在原图上做分割，https://github.com/hhj1897/face_parsing，该文件放到rtnet项目的根目录下
    将nerf渲染出的图像的人脸部分拼接到原图上
    要求：nerf渲染出的图像中人脸朝向等信息和gt一模一样，否则需要使用逆仿射变换将脸部转回到gt的朝向

    0 : background
    1 : skin (including face and scalp)
    2 : left_eyebrow
    3 : right_eyebrow
    4 : left_eye
    5 : right_eye
    6 : nose
    7 : upper_lip
    8 : inner_mouth
    9 : lower_lip
    10 : hair
'''


def main() -> None:
    # Parse command-line arguments
    parser = ArgumentParser()
    parser.add_argument(
        '--input', '-i', help='Input video path or webcam index (default=0)', default=0)
    parser.add_argument(
        '--output', '-o', help='Output file path', default=None)
    parser.add_argument('--fourcc', '-f', help='FourCC of the output video (default=mp4v)',
                        type=str, default='mp4v')
    parser.add_argument('--benchmark', '-b', help='Enable benchmark mode for CUDNN',
                        action='store_true', default=False)
    parser.add_argument('--no-display', help='No display if processing a video file',
                        action='store_true', default=False)
    parser.add_argument('--threshold', '-t', help='Detection threshold (default=0.8)',
                        type=float, default=0.8)
    parser.add_argument('--encoder', '-e', help='Method to use, can be either rtnet50 or rtnet101 (default=rtnet50)',
                        default='rtnet50') # choices=['rtnet50', 'rtnet101', 'resnet50'])

    parser.add_argument('--decoder', help='Method to use, can be either rtnet50 or rtnet101 (default=rtnet50)',
                        default='fcn', choices=['fcn', 'deeplabv3plus'])
    parser.add_argument('-n', '--num-classes', help='Face parsing classes (default=11)', type=int, default=11)
    parser.add_argument('--max-num-faces', help='Max number of faces',
                        default=50)
    parser.add_argument('--weights', '-w',
                        help='Weights to load, can be either resnet50 or mobilenet0.25 when using RetinaFace',
                        default=None)
    parser.add_argument('--device', '-d', help='Device to be used by the model (default=cuda:0)',
                        default='cuda:0')
    args = parser.parse_args()

    # Set benchmark mode flag for CUDNN
    torch.backends.cudnn.benchmark = args.benchmark

    face_detector = RetinaFacePredictor(threshold=args.threshold, device=args.device,
                                        model=(RetinaFacePredictor.get_model('mobilenet0.25')))
    face_parser = RTNetPredictor(
        device=args.device, ckpt=args.weights, encoder=args.encoder, decoder=args.decoder, num_classes=args.num_classes)

    print('Face detector created using RetinaFace.')

    base_path = "D:/data/imgs/generate_imgs/"
    total_frame = len(os.listdir(base_path))

    for frame_id in tqdm(range(total_frame)):
        gen_filename = "ngp_ep0015_%04d_rgb.png" % frame_id
        frame = cv2.imread(os.path.join(base_path, gen_filename))
        gt_frame = cv2.imread("D:/data/imgs/gt_imgs/%d.jpg" % frame_id)

        faces = face_detector(frame, rgb=False)
        if len(faces) > 0:
            masks = face_parser.predict_img(frame, faces, rgb=False)    # [h, w, 11]
            # print("mask", masks.shape)
            # print(masks[0])

            parsing = masks[0]    # [原图的h, w]

            del_list = [0, 10]
            face_part_x = []
            face_part_y = []

            for i in range(11):
                index = np.where(parsing == i)
                if i not in del_list:
                    # frame[index[0], index[1], :] = [0, 255, 0]
                    face_part_x.extend(index[0])
                    face_part_y.extend(index[1])
                else:
                    # frame[index[0], index[1], :] = [0, 255, 0]
                    continue

            # # 尝试一：直接将face_part部分贴回到原图（脸部pasteback效果良好，但其他部位受腐蚀和膨胀的影响，会变模糊）
            # gt_frame[face_part_x, face_part_y, :] = frame[face_part_x, face_part_y, :]
            # # bulrred = cv2.GaussianBlur(gt_frame, (5, 5), 2)
            # eroded_image = cv2.erode(gt_frame, (3, 3), iterations=4)
            # dilate_image = cv2.dilate(eroded_image, (3, 3), iterations=10)
            # cv2.imwrite("D:/results/bulr_%d.jpg" % frame_id, dilate_image)

            # # 尝试二：只对脸的一圈做高斯滤波（不work，脸盘那一圈花了）
            # print(parsing.shape)
            #
            # mask = np.zeros_like(frame)
            # print(mask.shape)
            # mask[face_part_x, face_part_y, :] = 255    # 设置不规则区域为白色
            # # cv2.imwrite("D:/results/mask_%d.jpg" % frame_id, mask)
            #
            # # 计算图像的梯度
            # gradient = cv2.Laplacian(mask, cv2.CV_64F)
            # # 将梯度图与mask相乘，去除掉mask以外的梯度
            # # gradient = gradient * mask
            #
            # # # 创建一个与图像大小相同的全零数组，作为高斯滤波后的结果
            # # blurred = np.zeros_like(frame)
            # #
            # # # 对梯度不为0的区域应用高斯滤波
            # # indices = np.where(gradient != 0)
            # # blurred[indices] = cv2.GaussianBlur(frame[indices], (0, 0), sigmaX=5, sigmaY=5)
            #
            # # # 对梯度做滤波
            # gradient = cv2.GaussianBlur(gradient, (101, 101), 11)
            # gradient = cv2.GaussianBlur(gradient, (101, 101), 11)
            # cv2.normalize(gradient, gradient)
            #
            # # cv2.imshow("gradient", gradient * 255.)
            # # cv2.waitKey()
            #
            # # # # 对梯度做滤波
            # # mask = cv2.GaussianBlur(mask, (5, 5), 2)
            # #
            # # cv2.imshow("mask", mask)
            # # cv2.waitKey(5)
            # #
            # # # upsample_img = inv_mask_border * img_color + (1 - inv_mask_border) * upsample_img
            # # # gt_frame = gt_frame.astype(np.uint8)
            # output = gradient * bulrred + (1 - gradient) * gt_frame
            # cv2.imwrite("D:/results/%d.jpg" % frame_id, output)
            #
            # print("np.all(output == gt_frame):", np.all(output == gt_frame))


            ######################################################################################
            ## 方法三：参照codeformer的pasteback（work）

            # 做只要脸部区域的mask
            mask = np.zeros_like(frame)
            mask[face_part_x, face_part_y, :] = 1
            print("mask.shape:", mask.shape)

            # 1.先对mask做erode
            mask_erode = cv2.erode(mask, (3, 3), iterations=4)

            pasted_face = mask_erode * frame    # 要贴过去的脸部
            print("pasted_face.shape:", pasted_face.shape)
            # cv2.imshow("pasted_face", pasted_face)
            # cv2.waitKey()

            # 2.基于人脸面积的融合边缘计算
            total_face_area = np.sum(mask_erode)
            print("total_face_area:", total_face_area)

            w_edge = int(total_face_area ** 0.5) // 20
            erosion_radius = w_edge * 2
            mask_center = cv2.erode(mask_erode, np.ones((erosion_radius, erosion_radius), np.uint8))
            blur_size = w_edge * 2
            inv_soft_mask = cv2.GaussianBlur(mask_center, (blur_size + 1, blur_size + 1), 0)
            print(inv_soft_mask.shape)    # [768, 768, 3]
            inv_soft_mask = inv_soft_mask[:, :, None]
            print(inv_soft_mask.shape)    # [768, 768, 1, 3]

            # 3.parse mask
            parse_mask = np.zeros(frame.shape)
            # MASK_COLORMAP = [0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 0, 0]
            # for idx, color in enumerate(MASK_COLORMAP):
            #     parse_mask[out == idx] = color
            parse_mask[face_part_x, face_part_y, :] = 255
            # cv2.imshow("parse_mask:", parse_mask)
            # cv2.waitKey()

            #  blur the mask
            parse_mask = cv2.GaussianBlur(parse_mask, (101, 101), 11)
            parse_mask = cv2.GaussianBlur(parse_mask, (101, 101), 11)
            # remove the black borders
            thres = 10
            parse_mask[:thres, :] = 0
            parse_mask[-thres:, :] = 0
            parse_mask[:, :thres] = 0
            parse_mask[:, -thres:] = 0
            parse_mask = parse_mask / 255.

            inv_soft_parse_mask = parse_mask[:, :, None]    # inv_soft_parse_mask [768, 768, 1, 3]
            # pasted_face = inv_restored
            fuse_mask = (inv_soft_parse_mask < inv_soft_mask).astype('int')    # fuse_mask [768, 768, 1, 3]
            inv_soft_mask = inv_soft_parse_mask * fuse_mask + inv_soft_mask * (1 - fuse_mask)
            print(inv_soft_mask.shape)    # [768, 768, 1, 3]

            inv_soft_mask = np.squeeze(inv_soft_mask)
            print("inv_soft_mask 缩减维度后：", inv_soft_mask.shape)
            final_pasteback_img = inv_soft_mask * pasted_face + (1 - inv_soft_mask) * gt_frame
            # cv2.imshow("final_pasteback_img", final_pasteback_img / 255.)
            # cv2.waitKey()
            cv2.imwrite("D:/results/bulr_%d.jpg" % frame_id, final_pasteback_img)





if __name__ == '__main__':
    main()
