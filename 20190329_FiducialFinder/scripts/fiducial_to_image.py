import SimpleITK as sitk
import pandas as pd
import os
import numpy as np
import argparse
import json
from collections import OrderedDict


def f2I(img, fid):
    ind = img.TransformPhysicalPointToIndex(fid)
    ind = np.reshape(ind, (3, 1))
    out_img = sitk.GetImageFromArray(ind)
    return out_img


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
    with open("./fiducials.json", 'rb') as f:
        pts = json.load(f)['fiducials']
    for pt in pts:
        points[pt] = fcsv.loc[fcsv[0] == pt].values[0][1:4]
    return points


def fiducials_to_image(fiducial_points, image_file_name):
    pt_list = []
    image = sitk.ReadImage(image_file_name)
    for pt in fiducial_points.values():
        pt_list += image.TransformPhysicalPointToIndex(pt)

    print(pt_list)
    arr = np.array(pt_list)
    arr = np.reshape(arr, (-1, 1))
    print(arr)
    return sitk.GetImageFromArray(arr)


def main(argv):
    # input: ../SmallData/0001_27588.fcsv

    # something for ../SmallData
    # something for 0001_27588_t1w.nii.gz

    print(argv)
    base, _ = os.path.splitext(argv.fcsv)

    fiducial_points = extract_fiducials(argv.fcsv)
    print(fiducial_points)

    output_image = fiducials_to_image(fiducial_points, argv.image)
    with open("./fiducials.json", 'rb') as f:
        pts = json.load(f)['fiducials']

    output_file_name = "{base}_{fids}.nii.gz".format(base=base, fids="_".join(pts))
    print("Writing to " + output_file_name)
    sitk.WriteImage(output_image, output_file_name)
    # print(sitk.GetArrayFromImage(output_image))
    im = sitk.ReadImage(output_file_name)
    print(sitk.GetArrayFromImage(im))


if __name__ == "__main__":
    main(extract_args())
