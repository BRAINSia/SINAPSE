import SimpleITK as sitk
import pandas as pd
import os
import numpy as np
import argparse
import json
from collections import OrderedDict
import logging

fiducials_json_path = "./fiducials.json"


logger = logging.getLogger("fid_to_img")
config = logging.basicConfig(filename="failed_conversions.log", level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')


def extract_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fcsv", help="The path to the .fcsv file", required=True)
    parser.add_argument("-i", "--image", help="The image for fcsv locations", required=True)
    return parser.parse_args()


def extract_fiducials(path):
    points = OrderedDict()
    fcsv = pd.read_csv(path, comment='#', header=None)
    fcsv[1] = -fcsv[1]
    fcsv[2] = -fcsv[2]
    with open(fiducials_json_path, 'rb') as f:
        pts = json.load(f)['fiducials']
    for pt in pts:
        points[pt] = fcsv.loc[fcsv[0] == pt].values[0][1:4]
    return points


def fiducials_to_image(fiducial_points, image_file_name):
    pt_list = []
    image = sitk.ReadImage(image_file_name)
    for pt in fiducial_points.values():
        pt_list += image.TransformPhysicalPointToIndex(pt)

    arr = np.array(pt_list)
    arr = np.reshape(arr, (-1, 1))
    return sitk.GetImageFromArray(arr)


def image_to_fiducials(image_file_name):
    image = sitk.ReadImage(image_file_name)


# Returns ['RE', 'LE']
def get_fiducial_keys():
    fids = []
    with open(fiducials_json_path, "rb") as f:
        fids = json.load(f)['fiducials']
    return fids


# returns "_RE_LE"
def get_fiducial_file_identifier():
    fid_file_identifier = ""
    fids = get_fiducial_keys()
    for fid in fids:
        fid_file_identifier += "_" + fid
    return fid_file_identifier


def validate_output_image(correct_image, output_image_file_name):
    image = sitk.ReadImage(output_image_file_name)

    correct_arr = sitk.GetArrayFromImage(correct_image)
    output_arr = sitk.GetArrayFromImage(image)

    try:
        assert(correct_arr.all() == output_arr.all())
    except AssertionError as _:
        logging.error(output_image_file_name + " incorrectly written."
                                       "\nExpected: " + str(correct_arr) +
                                        "\nActual: " + str(output_arr))



def main(argv):
    base, _ = os.path.splitext(argv.fcsv)
    base, _ = os.path.splitext(base)
    
    fiducial_points = extract_fiducials(argv.fcsv)

    output_image = fiducials_to_image(fiducial_points, argv.image)

    output_file_name = "{base}{fids}.nii.gz".format(base=base, fids=get_fiducial_file_identifier())
    print("Writing to " + output_file_name)
    sitk.WriteImage(output_image, output_file_name)
    print("Validating fiducial output image")
    validate_output_image(output_image, output_file_name)

if __name__ == "__main__":
    main(extract_args())
