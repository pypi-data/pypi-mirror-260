from __future__ import annotations

import hashlib

import cv2
import numpy as np
from cv2.typing import MatLike


def crop(img: MatLike, rect: tuple[int, int, int, int]):
    """Crops an cv2 image using coordinate and size"""
    img = img[rect[1] : rect[1] + rect[3], rect[0] : rect[0] + rect[2]]
    return img


def get_hash(img: MatLike):
    """Returns the hash of the image"""
    return hashlib.md5(img.tobytes()).hexdigest()


def get_diff(img1: MatLike, img2: MatLike):
    diff = cv2.absdiff(img1, img2)
    return np.sum(diff)
