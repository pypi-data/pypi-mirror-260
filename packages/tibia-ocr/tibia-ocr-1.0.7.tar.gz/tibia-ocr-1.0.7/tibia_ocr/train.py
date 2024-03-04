"""Main module"""

from __future__ import annotations

import json
import os
from argparse import ArgumentParser
from typing import Dict
from typing import List

import cv2
import numpy as np

from tibia_ocr.utils import crop
from tibia_ocr.utils import get_hash

DEFAULT_DATA = (
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567892"
)


def main():
    """Main function"""
    parser = ArgumentParser()
    parser.add_argument("input", help="input file")
    parser.add_argument("output", help="output file")
    parser.add_argument("--data", default=DEFAULT_DATA)
    parser.add_argument("--debug", help="debug", action="store_true")
    args = parser.parse_args()
    data = list(args.data)

    image = cv2.imread(args.input)
    white = np.array([255, 255, 255])
    threshed = cv2.inRange(image, white, white)
    contours, _ = cv2.findContours(
        threshed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    contours = list(contours)
    contours.sort(key=lambda c: cv2.boundingRect(c)[0])
    model: List[Dict[str, str | int]] = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        letter_image = crop(threshed, (x, y, w, h))
        letter_hash = get_hash(letter_image)
        letter = data.pop(0)
        if args.debug:
            cv2.imshow(
                "",
                cv2.resize(letter_image, None, fx=50, fy=50, interpolation=0),
            )
            cv2.setWindowTitle("", letter)
            cv2.waitKey()
            cv2.destroyWindow("")
        model.append(
            {
                "letter": letter,
                "hash": letter_hash,
                "width": w,
                "height": h,
            }
        )

    dirname = os.path.dirname(args.output)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    with open(args.output, "w") as file_pointer:
        json.dump(model, file_pointer, indent=2)


if __name__ == "__main__":
    main()
