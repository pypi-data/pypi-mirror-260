from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

import cv2
import numpy as np
from cv2.typing import MatLike

from tibia_ocr.constants import BIG_FONT
from tibia_ocr.exceptions import FontNotFound
from tibia_ocr.utils import crop
from tibia_ocr.utils import get_hash


@lru_cache()
def get_model(font: Path | str):
    try:
        with open(font) as fp:
            letters = json.load(fp)
            return {l["hash"]: l for l in letters}
    except FileNotFoundError:
        raise FontNotFound(f'Font "{font}" not found.')


@lru_cache()
def get_min_width(font: Path | str):
    # returns the minimum width of a letter in the font
    model = get_model(font)
    min_width = min([l["width"] for l in model.values()])
    return min_width


@lru_cache()
def get_min_height(font: Path | str):
    # returns the minimum height of a letter in the font
    model = get_model(font)
    min_height = min([l["height"] for l in model.values()])
    return min_height


def convert_letter(
    img: MatLike, font: Path | str = BIG_FONT, debug: bool = False
) -> str:
    """Ocr a letter"""
    model_obj = get_model(font)
    _, width = img.shape[:2]
    if width == 0:
        return ""
    min_tentative_width = get_min_width(font)
    max_tentative_width = min(10, width)
    for tentative_width in reversed(
        range(min_tentative_width, max_tentative_width + 1)
    ):
        letter_image: MatLike = img[:, :tentative_width]
        contours, _ = cv2.findContours(
            letter_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        if contours == []:
            continue
        x, y, w, h = cv2.boundingRect(contours[0])
        letter_image = crop(letter_image, (x, y, w, h))
        letter_hash = get_hash(letter_image)
        letter = model_obj.get(letter_hash, None)
        if debug:
            cv2.imshow("", letter_image)
            cv2.setWindowTitle("", str(letter))
            if letter is not None:
                print(letter["letter"])
            cv2.waitKey()
            cv2.destroyWindow("")
        if letter is not None:
            remaining_image: MatLike = img[:, tentative_width:]
            letter = letter["letter"]
            return letter + convert_letter(remaining_image, font=font)
    return ""


def convert_line(
    img: MatLike, font: Path | str = BIG_FONT, debug: bool = False
):
    """Ocr a line"""
    contours, _ = cv2.findContours(
        img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    contours = list(contours)
    contours.sort(key=lambda c: cv2.boundingRect(c)[0])
    line = ""
    for contour in contours:
        # create a mask from the contour
        mask = np.zeros_like(img)
        cv2.drawContours(mask, [contour], 0, [255], -1)

        # mask the original image
        letter_image = cv2.bitwise_and(img, mask)

        # crop the letter image and convert the image to character
        x, y, w, h = cv2.boundingRect(contour)
        letter_image = crop(letter_image, (x, y, w, h))
        letter = convert_letter(letter_image, font=font)
        line += letter

        # debug
        if debug:
            cv2.imshow(
                letter,
                cv2.resize(letter_image, None, fx=30, fy=30, interpolation=0),
            )
            cv2.waitKey()
            cv2.destroyWindow(letter)
    return line


def convert_paragraph(img: MatLike, font: Path | str = BIG_FONT):
    """Ocr a paragraph"""
    start = None
    paragraph: list[str] = []
    for i, row in enumerate(img):
        non_zero = np.count_nonzero(row)
        if non_zero == 0 and start is not None:
            line: MatLike = img[start:i]
            if line.shape[0] >= get_min_height(font):
                paragraph.append(convert_line(line, font=font))
            start = None
        if non_zero > 0 and start is None:
            start = i
    if start is not None:
        line = img[start:]
        if line.shape[0] >= get_min_height(font):
            paragraph.append(convert_line(line, font=font))
    return "\n".join(paragraph)
