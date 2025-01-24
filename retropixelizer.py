import argparse
import os
import sys
from PIL import Image, ImageEnhance
from termcolor import colored


def error(message):
    print(colored("ERROR!", "red", attrs=["reverse", "bold"]) + " " + message)


def main():
    parser = argparse.ArgumentParser(
        prog="retropixelizer.py",
        description="RetroPixelizer is a simple tool that converts a square image to an old-style monochrome pixelated image.",
    )
    parser.add_argument("-i", "--infile", type=str, help="input image", required=True)
    parser.add_argument("-o", "--outfile", type=str, help="output image", required=True)
    parser.add_argument(
        "-s",
        "--size",
        type=str,
        help="side size in pixel (default: 64)",
        default=64,
        required=False,
    )
    parser.add_argument(
        "-c",
        "--colors",
        type=int,
        help="colors (default: 8)",
        default=8,
        required=False,
    )
    parser.add_argument(
        "-f",
        "--contrast-factor",
        type=float,
        help="contrast factor (default: 1.5)",
        default=1.5,
        required=False,
    )
    args = parser.parse_args()
    in_file = args.infile
    out_file = args.outfile
    size = args.size
    colors = args.colors
    factor = args.contrast_factor

    if not os.path.isfile(in_file):
        error('File "' + in_file + '" does not exist or is not readable.')
        sys.exit(1)

    input_image = Image.open(in_file)
    width, height = input_image.size

    if width != height:
        error("The input image must be square (ratio 1:1).")
        sys.exit(1)

    size = int(size)
    output_image = input_image.resize((size, size), resample=Image.BILINEAR).resize(
        input_image.size, Image.NEAREST
    )

    try:
        output_image = output_image.convert("RGB")
        contrast_factor = factor
        enhancer = ImageEnhance.Contrast(output_image)
        output_image = enhancer.enhance(contrast_factor)
        output_image = output_image.quantize(colors=colors)
        output_image = output_image.convert("L")
        output_image.save(out_file, optimize=False)
    except Exception:
        error('Error while saving file "' + out_file + '".')


if __name__ == "__main__":
    main()
