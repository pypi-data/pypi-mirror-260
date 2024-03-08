#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
author：yannan1
since：2023-06-06
"""

from typing import Tuple

import numpy as np

from ..common import AbstractTransform

__all__ = [
    'OCR',
]


# TODO 换个ocr源
class OCR(AbstractTransform):

    def __init__(self, lang: str = 'ch_sim') -> None:
        """OCR, 光学字符识别, 识别

        Args:
            lang: Language codes, 识别语言, {"ch_sim", "en", "ko", "ja"}, "ch_sim"
        """
        super().__init__(use_gpu=False)

        try:
            import easyocr
        except ImportError:
            raise RuntimeError(
                'The OCR module requires "easyocr" package. '
                'You should install it by "pip install easyocr".'
            )

        def _reformat_input(image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
            if len(image.shape) == 2:
                return np.tile(image[:, :, None], (1, 1, 3)), image
            elif len(image.shape) == 3:
                if image.shape[-1] == 1:
                    return np.tile(image, (1, 1, 3)), image[:, :, 0]
                elif image.shape[-1] == 3:
                    return image, np.mean(image, -1)
            raise RuntimeError(f'Invalid image shape {image.shape}.')

        setattr(easyocr.easyocr, 'reformat_input', _reformat_input)
        self.reader = easyocr.Reader([lang], gpu=False)

    def _apply(self, sample):

        if sample.image is None:
            return sample

        sample.ocr = self.reader.readtext(sample.image)

        return sample
