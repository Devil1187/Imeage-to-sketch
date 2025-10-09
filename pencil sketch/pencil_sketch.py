



"""
pencil_sketch.py
Convert an input image into a pencil sketch using OpenCV.
Usage examples:
  python pencil_sketch.py -i dog.jpg -o sketch.png
  python pencil_sketch.py -i dog.jpg         # shows windows (desktop)
"""

import cv2
import argparse
import os
import sys

def pencil_sketch(input_path: str, output_path: str | None = None,
                  ksize=(21, 21), scale: float = 256.0):
    # read image
    img = cv2.imread(input_path)
    if img is None:
        raise FileNotFoundError(f"Could not read image: {input_path}")

    # convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # invert grayscale image
    inverted = 255 - gray

    # blur the inverted image (Gaussian)
    blurred = cv2.GaussianBlur(inverted, ksize, 0)

    # invert the blurred image
    inverted_blur = 255 - blurred

    # create pencil sketch by dividing the gray image by the inverted blurred image
    sketch = cv2.divide(gray, inverted_blur, scale=scale)

    # either save to disk, or show windows (desktop)
    if output_path:
        success = cv2.imwrite(output_path, sketch)
        if not success:
            raise IOError(f"Could not write output image to: {output_path}")
        print(f"Saved sketch to: {output_path}")
    else:
        cv2.imshow("Original", img)
        cv2.imshow("Pencil Sketch", sketch)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return sketch

def parse_args():
    p = argparse.ArgumentParser(description="Convert image to pencil sketch (OpenCV)")
    p.add_argument("-i", "--input", required=True, help="Input image path")
    p.add_argument("-o", "--output", default=None,
                   help="Output path (if omitted, image windows will be shown instead)")
    p.add_argument("-k", "--ksize", nargs=2, type=int, metavar=('W','H'),
                   default=[21,21],
                   help="Gaussian blur kernel size (two odd ints, default 21 21)")
    p.add_argument("-s", "--scale", type=float, default=256.0,
                   help="Scale parameter for cv2.divide (default 256.0)")
    return p.parse_args()

if __name__ == "__main__":
    args = parse_args()
    # ensure odd kernel sizes (recommended)
    kx, ky = args.ksize
    if kx % 2 == 0 or ky % 2 == 0:
        print("Warning: kernel sizes should be odd numbers. Incrementing by 1 where needed.")
        kx += kx % 2 == 0
        ky += ky % 2 == 0

    try:
        pencil_sketch(args.input, args.output, ksize=(kx, ky), scale=args.scale)
    except Exception as e:
        print("ERROR:", e)
        sys.exit(1)
