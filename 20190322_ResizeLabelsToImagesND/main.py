from argparse import ArgumentParser
from os.path import join, split

from SimpleITK import (Image, ReadImage, Resample, Transform, WriteImage,
                       sitkIdentity, sitkNearestNeighbor, sitkUInt16)

PIXEL_TYPE = sitkUInt16


def parse_args():
    parser = ArgumentParser(
        description="Main program for resizing labels to the same voxel size as the label"
    )
    parser.add_argument(
        "-i", "--input-image-file",
        help="image file",
        required=True
    )
    parser.add_argument(
        "-l", "--input-label-file",
        help="label to be re-sized",
        required=True
    )
    parser.add_argument(
        "-o", "--output-dir",
        help="output directory for re-sized images",
        required=True
    )
    return parser.parse_args()


# this is really just re-sampling the label into the image space
def resize(input_image_file: str, input_label_file: str) -> Image:
    input_image = ReadImage(input_image_file)
    input_label = ReadImage(input_label_file)
    identity = Transform(input_image.GetDimension(), sitkIdentity)
    interpolator = sitkNearestNeighbor  # we are working with labels, so we want the nearest neighbor

    # set up reference domain
    ref_image = Image(input_image.GetSize(), PIXEL_TYPE)
    ref_image.SetSpacing(input_image.GetSpacing())
    ref_image.SetOrigin(input_image.GetOrigin())
    ref_image.SetDirection(input_image.GetDirection())
    # re-sample image
    return Resample(input_label, ref_image, identity, interpolator)


def main(argv):
    WriteImage(
        resize(input_image_file=argv.input_image_file, input_label_file=argv.input_label_file),
        join(argv.output_dir, split(argv.input_label_file)[1])
    )


if __name__ == '__main__':
    main(parse_args())
