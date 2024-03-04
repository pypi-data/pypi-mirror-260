# tibia-ocr

OCR to read Tibia in-game text written in python

## Installation

You can install the package via pip:

```bash
pip install tibia-ocr
```

## Usage

```python
import cv2

from tibia_ocr.hash_ocr import convert_line

image = cv2.imread("data/test.png")
threshed = cv2.inRange(image, (192, 192, 192), (192, 192, 192))
out = convert_line(threshed)
print(out)
```

## Known Limitations

- `!` is detected as `i` in big font
- Can not detect spaces

## License

This project is licensed under the terms of the MIT license.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Contact

If you want to contact me you can reach me at pradishbijukchhe@gmail.com.
