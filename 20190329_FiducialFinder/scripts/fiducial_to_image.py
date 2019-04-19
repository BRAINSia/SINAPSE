import SimpleITK as sitk
import pandas as pd
import os
import numpy as np
import argparse


def f2I(img, fid):
    ind = img.TransformPhysicalPointToIndex(fid)
    ind = np.reshape(ind, (3,1))
    out_img = sitk.GetImageFromArray(ind)
    return out_img


def get_array_from_fiducial(directory, identifier):
    fcsv=pd.read_csv(os.path.join(directory, '{identifier}.fcsv'.format(identifier=identifier)), comment='#', header=None)
    fcsv[1] = -fcsv[1]
    fcsv[2] = -fcsv[2]
    LE = fcsv.loc[fcsv[0] == 'LE'].values[0][1:4] # physical point 3-tuple of left eye

    LE = np.array(LE)
    return LE


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    img = "0001_27588_t1w.nii.gz"
    identifier = "0001_27588"
    in_img = sitk.ReadImage(os.path.join("../SmallData", img))
    LE = get_array_from_fiducial("../SmallData", identifier)
    resulting_image = f2I(in_img, LE)
    sitk.WriteImage(resulting_image, os.path.join("../SmallData", '{identifier}_LE.nii.gz'.format(identifier=identifier)))



if __name__ == "__main__":

    main()
