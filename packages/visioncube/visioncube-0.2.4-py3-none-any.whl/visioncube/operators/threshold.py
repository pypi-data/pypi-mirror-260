#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
author：yannan1
since：2023-11-29
"""
import cv2 as cv
import numpy as np

from ..common import AbstractTransform

__all__ = [
    "ThresholdingImage",
    "InRangeThreshold",
]


class ThresholdingImage(AbstractTransform):

    def __init__(
            self,
            threshold: float = 0,
            threshold2: float = 255,
            method: str = 'auto',
            kernel_size: int = 3,
            offset: int = 0,
            kernel_mode='mean',
    ) -> None:
        """图像二值化, 颜色变换

        Args:
            threshold: Threshold, 图像阈值/双阈值法中的第一个阈值, [0, 255, 1], 0
            threshold2: Threshold2, 双阈值法中的第二个阈值（其他方法不需要此参数）, [0, 255, 1], 255
            method: Method, 计算阈值的方法, {'auto', 'single_thr', 'triangle', 'adaptive', 'double_thr'}, "auto"
            kernel_size: Kernel size, adaptive方法的核尺寸, (0, 500, 1), 3
            offset: Offset, adaptive方法中阈值要减去的偏移量, [0, 255, 1], 0
            kernel_mode: Kernel mode, adaptive方法使用的核类型, {'mean', 'gaussian'}, 'mean'

        """
        super().__init__(use_gpu=False)
        
        self.thr = threshold
        self.thr2 = threshold2
        if method not in ['auto', 'single_thr', 'triangle', 'adaptive', 'double_thr']:
            raise ValueError("Method Error!")
        self.method = method
        self.kernel_size = kernel_size
        self.offset = offset

        if kernel_mode.lower() not in ['mean', 'gaussian']:
            raise ValueError("Kernel mode error!")
        if kernel_mode.lower() == 'mean':
            self.kernel_mode = cv.ADAPTIVE_THRESH_MEAN_C
        elif kernel_mode.lower() == 'gaussian':
            self.kernel_mode = cv.ADAPTIVE_THRESH_GAUSSIAN_C

    def _apply(self, sample):
        if sample.image is None:
            return sample

        image = sample.image
        if len(image.shape) == 3 and image.shape[-1] == 3:
            image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        mask = np.zeros(sample.shape, dtype=np.uint8)

        if self.method == 'auto':
            ret, mask = cv.threshold(image, 0, 255, cv.THRESH_OTSU)
        elif self.method == 'single_thr':
            ret, mask = cv.threshold(image, self.thr, 255, cv.THRESH_BINARY)
        elif self.method == 'double_thr':
            thr_min = min(self.thr, self.thr2)
            thr_max = max(self.thr, self.thr2)
            ret1, threshold1 = cv.threshold(image, thr_min, 255, cv.THRESH_BINARY)
            ret2, threshold2 = cv.threshold(image, thr_max, 255, cv.THRESH_BINARY_INV)
            mask = np.bitwise_and(threshold1, threshold2)
        elif self.method == 'triangle':
            ret, mask = cv.threshold(image, 0, 255, cv.THRESH_TRIANGLE)
        elif self.method == 'adaptive':
            mask = cv.adaptiveThreshold(image, 255, self.kernel_mode, cv.THRESH_BINARY,
                                        self.kernel_size, self.offset)

        sample.image = np.repeat(mask[..., np.newaxis], repeats=3, axis=-1)

        return sample


class InRangeThreshold(AbstractTransform):

    def __init__(
            self,
            low_h_thr: int = 0,
            low_s_thr: int = 0,
            low_v_thr: int = 0,
            high_h_thr: int = 180,
            high_s_thr: int = 30,
            high_v_thr: int = 255,
    ) -> None:
        """分割图片中的指定HSV颜色范围, 颜色变换

        Args:
            low_h_thr: HJue low threshold, 目标颜色范围的H下限, (0, 180, 1], 0
            low_s_thr: Saturation low threshold, 目标颜色范围的S下限, (0, 255, 1], 0
            low_v_thr: Value low threshold, 目标颜色范围的V下限, (0, 255, 1], 0
            high_h_thr: Hue high threshold, 目标颜色范围的H上限, (0, 180, 1], 180
            high_s_thr: Saturation high threshold, 目标颜色范围的S上限, (0, 255, 1], 255
            high_v_thr: Value high threshold, 目标颜色范围的V上限, (0, 255, 1], 255
        """
        super().__init__(use_gpu=False)

        self.low_thr = (low_h_thr, low_s_thr, low_v_thr)
        self.high_thr = (high_h_thr, high_s_thr, high_v_thr)

    def _apply(self, sample):
        if sample.image is None:
            return sample

        image_hsv = cv.cvtColor(sample.image, cv.COLOR_RGB2HSV)
        image = cv.inRange(image_hsv, self.low_thr, self.high_thr)
        sample.image = np.repeat(image[..., np.newaxis], repeats=3, axis=-1)

        return sample
