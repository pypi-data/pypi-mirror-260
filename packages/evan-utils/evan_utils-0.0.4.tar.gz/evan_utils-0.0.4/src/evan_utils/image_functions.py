#! /usr/bin/env python
# -*- coding: utf-8 -*-
__all__ = ('copy_image', 'image_float2uint',
           'what_type_image', 'fetch_image_paths', 'show_images_in_one_folder', 'plot_image', 'subplot_images',
           'cv_read_image', 'cv_save_image', 'pil_read_image', 'pil_save_image', 'read_and_show_image',
           'transform_image_clinic', 'text2qrimg',
           'plot_one_box', 'plot_group_boxes', 'plot_predicts_and_annotations',
           'mask2box_coord', 'mask2box', 'box_match', 'box_iou')

import imghdr
import os
import qrcode
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from basic_functions import check_command


def image_float2uint(nd_arr):
    """将0~1范围的float 图片准换为0~255的uint8格式"""
    return (nd_arr * 255).astype(np.uint8)


def copy_image(source_path, target_folder):
    # work_dir = os.getcwd()
    # # 先进入源文件夹
    # os.chdir(source_folder)
    # 图片复制
    copy_command = f'cp {source_path} {target_folder}'
    copy_command = check_command(copy_command)
    os.system(copy_command)
    
    # 回到原工作路径
    # os.chdir(work_dir)


def what_type_image(image_file):
    """接受图片路径或数据流作为输入，返回图片类型或None"""
    if os.path.isdir(image_file):
        return None
    return imghdr.what(image_file)


def fetch_image_paths(folder):
    """获取文件夹中所有图片的路径"""
    image_paths = []
    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)
        if what_type_image(file_path):
            image_paths.append(file_path)
    return image_paths


def text2qrimg(text, save_path):
    """
    # 要生成二维码的字符串
    text = "臭宝宝"
    """
    # 生成二维码
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(text)
    qr.make(fit=True)
    
    # 生成二维码图片
    img = qr.make_image(fill_color="black", back_color="white")
    
    # 保存二维码图片
    img.save(save_path)


def show_images_in_one_folder(folder):
    """读取并显示一个文件夹内的所有图片"""
    image_paths = fetch_image_paths(folder)
    for image_path in image_paths:
        read_and_show_image(image_path)


def plot_image(image, title=None, grey=False):
    if grey:
        image = cv.cvtColor(image, cv.COLOR_GRAY2RGB)
    if title:
        plt.title(title)
    plt.imshow(image)
    plt.show()


def subplot_images(subplot_size, images, save_path=None, show=True):
    """subplot several images
    Args:
        subplot_size (tuple, list): e.g. (2, 2) or (1, 3)
        images (tuple, list): a tuple of ndarray images
        save_path (str): path to save plot
        show (bool): whether show this plot or not
    """
    height, width = subplot_size
    for image_index in range(height * width):
        plt.subplot(height, width, image_index + 1)
        plt.imshow(images[image_index])
    if save_path is not None:
        plt.savefig(save_path)
    if show:
        plt.show()


def cv_read_image(image_path):
    """adjust opencv imread to get an rgb image
    Args:
        image_path (str):

    Returns:
        image (nd): rgb
    """
    image = cv.imread(image_path)
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    return image


def pil_read_image(image_path, to_array=True):
    """比opencv还快"""
    image = Image.open(image_path)
    if to_array:
        image = np.array(image)
    return image


def pil_save_image(ndarray, image_path):
    """图片的后缀可以自行设置"""
    im = Image.fromarray(ndarray)
    im.save(image_path)


def read_and_show_image(image_path):
    """(eog:46085): Gtk-WARNING **: 16:24:52.266: cannot open display: """
    image = Image.open(image_path)
    plot_image(image, title=image_path)


def cv_save_image(ndarray, image_path):
    """ndarray是rgb格式，图片的后缀可以自行设置，比PIL快三倍左右
    如果是bgr格式，不需要cvtColor"""
    cv.imwrite(image_path, cv.cvtColor(ndarray, cv.COLOR_RGB2BGR))


def transform_image_clinic(image, resize_size=None):
    """pil image, 将长宽不相等的rgba四通道图片转换成适合模型输入的正方形图片"""
    image = np.array(image)[:, :, :3]
    image = cv.resize(image, (resize_size, resize_size))
    # image = T.ToTensor()(image)
    return image


def plot_one_box(xyxy, im, color=(0, 0, 0), label=None, name=None, line_thickness=1, show=False):
    """Plots one bounding box on image 'im' using OpenCV
    xyxy: 1d, left-top and then right-bottom
    x: horizontal, y: vertical"""
    assert im.data.contiguous, 'Image not contiguous. Apply np.ascontiguousarray(im) to plot_on_box() input image.'
    tl = line_thickness or round(0.002 * (im.shape[0] + im.shape[1]) / 2) + 1  # line/font thickness
    c1, c2 = (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3]))
    cv.rectangle(im, c1, c2, color, thickness=tl, lineType=cv.LINE_AA)
    # if name:
    #     cv.putText(im, name, (10, 10), 0, tl / 3, color, thickness=tl, lineType=cv.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] + t_size[1] + 5
        # cv.rectangle(im, c1, c2, color, -1, cv.LINE_AA)  # filled 字体底色
        cv.putText(im, label, (c1[0], c2[1] - 2), 0, tl / 3, color, thickness=tf, lineType=cv.LINE_AA)
    if show:
        plot_image(im)


def plot_group_boxes(image, boxes, labels, color=(255, 0, 0), line_thickness=1, target=False, show=False):
    """在图上画一组box并标注label
    Args:
        image (ndarray):
        boxes (list of list / ndarray):
        labels (list):
        color (tuple): 例如 (255, 0, 0)
        line_thickness (float): 线条粗细，影响字符粗细
        target (bool): labels属于预测出的（False）还是真实标注（True）
        show (bool): 是否直接显示
    """
    num_annotate = len(labels)
    for i in range(num_annotate):
        box = boxes[i]
        label = labels[i]
        # score = scores[i].item()
        if target:
            text = 'true{}'.format(label)
        else:
            text = '{}'.format(label)
        plot_one_box(box, image, label=text, color=color, line_thickness=line_thickness, show=False)
    if show:
        plot_image(image)


def plot_predicts_and_annotations(image, predict_boxes, predict_labels, target_boxes, target_labels):
    """在图上同时画出预测及标注
    Args:
        image (ndarray):
        predict_boxes:
        predict_labels:
        target_boxes:
        target_labels:
    """
    plot_group_boxes(image, predict_boxes, predict_labels, color=(255, 0, 0))
    plot_group_boxes(image, target_boxes, target_labels, color=(0, 255, 0), target=True)


def mask2box_coord(mask, grey=False):
    """take a mask as input, return box coord, very efficient
    Args:
        mask ():
        grey (bool, True): if True, we take mask as a grey image.

    Returns:
        x, y, w, h (int): x-from left to right columns, y-from up to down rows
    """
    if grey:
        x, y, w, h = cv.boundingRect(mask)
    else:
        mask_gray = cv.cvtColor(mask, cv.COLOR_RGB2GRAY)
        x, y, w, h = cv.boundingRect(mask_gray)
    return x, y, w, h  # x, y, x+w, y+w


def mask2box(mask):
    """may be not efficient
    Args:
        mask (nd): e.g.(1024, 1024, ...), not necessarily to be 2d

    Returns:
        box
    """
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    
    return rmin, cmin, rmax + 1, cmax + 1  # x1, y1, x2, y2


def box_iou(bb1, bb2):
    """
    Calculate the Intersection over Union (IoU) of two bounding boxes.
    Parameters
    ----------
    bb1 : nd1d [x1, y1, x2, y2]
        The (x1, y1) position is at the top left corner,
        the (x2, y2) position is at the bottom right corner
    bb2 : the same
    Returns
    -------
    float
        in [0, 1]
    """
    assert bb1[0] < bb1[2]
    assert bb1[1] < bb1[3]
    assert bb2[0] < bb2[2]
    assert bb2[1] < bb2[3]
    
    # determine the coordinates of the intersection rectangle
    x_left = max(bb1[0], bb2[0])
    y_top = max(bb1[1], bb2[1])
    x_right = min(bb1[2], bb2[2])
    y_bottom = min(bb1[3], bb2[3])
    
    if x_right < x_left or y_bottom < y_top:
        return {'bool_intersect': False}
    
    # The intersection of two axis-aligned bounding boxes is always an
    # axis-aligned bounding box
    intersection_area = (x_right - x_left) * (y_bottom - y_top)
    
    # compute the area of both AABBs
    bb1_area = (bb1[2] - bb1[0]) * (bb1[3] - bb1[1])
    bb2_area = (bb2[2] - bb2[0]) * (bb2[3] - bb2[1])
    
    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
    assert iou >= 0.0
    assert iou <= 1.0
    return {'bool_intersect': True, 'iou': iou,
            'intersection': intersection_area, 'intersection_coord': [x_left, y_top, x_right, y_bottom],
            'box1': bb1_area, 'box2': bb2_area}


def box_match(box1, box2, threshold=0.5):
    """根据两个框左上角和右下角的坐标，判断是否能认为是同一个框，标准见机行事
    Args:
        box1 (nd1d):
        box2 (nd1d):
        threshold (float 0~1): 据此判断是否可认为是一个框

    Returns:
        bool
    """
    iou_dict = box_iou(box1, box2)
    if isinstance(iou_dict, dict):
        iou, intersection, box1_area, box2_area = iou_dict['iou'], iou_dict['intersection'], \
            iou_dict['box1'], iou_dict['box2']
        if ((intersection / box1_area) > threshold) or ((intersection / box2_area) > threshold):
            return 1
        else:
            return 0
    else:
        return 0
