from argparse import ArgumentParser
from glob import glob
from os.path import isfile, join


def parse_args():
    parser = ArgumentParser(
        description="Utility program for ResizeLabelsToImages2D that matches image and label filen ames"
    )
    parser.add_argument(
        "-i", "--input-image-dir",
        help="directory of images",
        required=True
    )
    parser.add_argument(
        "-l", "--input-label-dir",
        help="directory of labels",
        required=True
    )
    parser.add_argument(
        "-o", "--output-file",
        help="output file to write aligned file names to",
        required=True
    )

    return parser.parse_args()


def sort_files(input_image_dir: str, input_label_dir: str, output_file_name: str) -> None:
    # read in file names
    images = [f for f in glob(join(input_image_dir, '*')) if isfile(f)]
    labels = [f for f in glob(join(input_label_dir, '*')) if isfile(f)]
    # these files must be named such that lexical sort aligns pairs
    images.sort()
    labels.sort()
    # make sure you have at least the correct number of each
    print("images:", len(images), "labels", len(labels))
    assert len(images) == len(labels)
    with open(output_file_name, 'w') as f:
        for im_file, lbl_file in zip(images, labels):
            f.write("{imf},{lblf}\n".format(imf=im_file, lblf=lbl_file))


if __name__ == '__main__':
    args = parse_args()
    print(args)
    sort_files(input_image_dir=args.input_image_dir, input_label_dir=args.input_label_dir,
               output_file_name=args.output_file)
