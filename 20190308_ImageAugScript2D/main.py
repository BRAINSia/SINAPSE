from json import load
from os.path import split
from argparse import ArgumentParser
from utils.augmentation import augment_data
from utils.image_io import read_im, write_dir
from utils.prep import condense_label_map, select_image_channel


def parse_args():
    parser = ArgumentParser(description="Main program for 2D image augmentation")
    parser.add_argument(
        "-i", "--input-file",
        help="input file to be augmented",
        required=True
    )
    parser.add_argument(
        "-o", "--output-dir",
        help="output directory to write augmented data to",
        required=True
    )
    parser.add_argument(
        "-l", "--is-label",
        help="set to 1 if you are augmenting a label map",
        default=0,
        required=False
    )
    parser.add_argument(
        "-a", "--augment",
        help="path to augmentation.json",
        default="",
        required=False
    )
    return parser.parse_args()


def main(argv):
    if argv.augment:
        with open(argv.augment) as f:
            aug_conf = load(f)
    else:
        # if no configuration is given, provide a default config
        aug_conf = {
            "flip_LR": 1,
            "flip_UD": 0,
            "rotate": 1,
            "deg_of_rotation": [-20, 20]
        }

    short_file_name = split(argv.input_file)[1]

    image = read_im(full_file_name=argv.input_file)

    # check if you are working with a scalar or vector image

    if bool(int(argv.is_label)):
        image = condense_label_map(image=image)
    else:
        # this currently just selects a channel, but could be converted to greyscale
        image = select_image_channel(image=image, channel=0)

    images = augment_data(image=image, fname=short_file_name, settings=aug_conf, is_label=bool(argv.is_label))

    write_dir(base_dir=argv.output_dir, images=images)

    return 0


if __name__ == '__main__':
    main(parse_args())
