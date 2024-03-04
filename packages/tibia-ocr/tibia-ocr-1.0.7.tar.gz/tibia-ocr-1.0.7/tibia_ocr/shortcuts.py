from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from cv2.typing import MatLike

from tibia_ocr.constants import BIG_FONT
from tibia_ocr.hash_ocr import convert_line
from tibia_ocr.hash_ocr import convert_paragraph


def convert(img: MatLike, font: Path | str = BIG_FONT):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)
    return convert_line(img, font=font)


def convert_in_range(
    img: MatLike, upper: MatLike, lower: MatLike, font: Path | str = BIG_FONT
):
    img = cv2.inRange(img, upper, lower)
    return convert_line(img, font=font)


def convert_red(img: MatLike, font: Path | str = BIG_FONT):
    lowerb = np.array([(17, 17, 176)])
    upperb = np.array([255, 255, 255])
    return convert_in_range(img, lowerb, upperb, font=font)


def convert_paragraph_in_range(
    img: MatLike, upper: MatLike, lower: MatLike, font: Path | str = BIG_FONT
):
    img = cv2.inRange(img, upper, lower)
    return convert_paragraph(img, font=font)


def convert_number_threshed(img: MatLike, font: Path | str = BIG_FONT):
    try:
        return int(convert_line(img, font=font))
    except ValueError:
        return -1


def convert_number(img: MatLike, font: Path | str = BIG_FONT):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)
    return convert_number_threshed(img, font=font)


def convert_number_in_range(
    img: MatLike, lower: MatLike, upper: MatLike, font: Path | str = BIG_FONT
):
    try:
        img = cv2.inRange(img, lower, upper)
        return int(convert_line(img, font=font))
    except ValueError:
        return -1


def convert_number_red(img: MatLike, font: Path | str = BIG_FONT):
    lowerb = np.array([(17, 17, 176)])
    upperb = np.array([255, 255, 255])
    return convert_number_in_range(img, lowerb, upperb, font=font)


def convert_number_green(img: MatLike, font: Path | str = BIG_FONT):
    lowerb = np.array([(17, 170, 17)])
    upperb = np.array([255, 255, 255])
    return convert_number_in_range(img, lowerb, upperb, font=font)
