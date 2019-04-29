
# coding: utf-8

# In[38]:


import SimpleITK as sitk
import os
import json
import pandas as pd
import csv
from fiducial_to_image import extract_fiducials
import ntpath
import argparse

# In[76]:


for file in os.listdir("../SmallData/"):
    base, _ = os.path.splitext(file)
    base, _ = os.path.splitext(base)


# In[10]:


# returns "_RE_LE"
def get_fiducial_file_identifier():
    fid_file_identifier = ""
    fids = get_fiducial_keys()
    for fid in fids:
        fid_file_identifier += "_" + fid
    return fid_file_identifier


# In[7]:


# Returns ['RE', 'LE']
def get_fiducial_keys():
    fids = []
    with open("../fiducials.json", "rb") as f:
        fids = json.load(f)['fiducials']
    return fids


# In[52]:



def get_expected_fiducial_data(file_path):
    fcsv_filename = ntpath.basename(file_path)
    image_name_prefix, _ = os.path.splitext(fcsv_filename)
    image_name = image_name_prefix + "_t1w.nii.gz"
    image_path = file_path.replace(fcsv_filename, "") + image_name
    image = sitk.ReadImage(image_path)
    ordered_fiducials = extract_fiducials(file_path)
    expected_fiducial_data = []
    for fiducial_key in get_fiducial_keys():
        expected_index_data = image.TransformPhysicalPointToIndex(ordered_fiducials[fiducial_key])
        expected_fiducial_data.extend(expected_index_data)
    return expected_fiducial_data


def fiducials_from_image(image_file_name):  
    print(image_file_name)
    image = sitk.ReadImage("..SmallDataTest/" + image_file_name)
    arr = sitk.GetArrayFromImage(image)
    return arr


def image_name_from_fcsv(fcsv_path):
    fcsv_file_name = ntpath.basename(fcsv_path)
    base, _ = os.path.splitext(fcsv_file_name)
    return base + get_fiducial_file_identifier() + ".nii.gz"

# In[58]:
def extract_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fcsv", help="The path to the .fcsv file", required=True)
    return parser.parse_args()


def main(argv):
    #file_path = "../SmallDataTest/0001_27588.fcsv"
    print(get_expected_fiducial_data(argv.fcsv))
    print(fiducials_from_image(image_name_from_fcsv(argv.fcsv)))


if __name__ == "__main__":
    main(extract_args())

