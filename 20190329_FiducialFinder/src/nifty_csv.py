from glob import glob
from os.path import join, isdir
from os import mkdir

# import pandas as pd
from numpy import array
from numpy.random import permutation

from utils import get_unique_run_id

TRAINING_PERCENTAGE = 0.7
VALIDATION_PERCENTAGE = 0.2
INFERENCE_PERCENTAGE = 0.1


# functions for generating NiftyNet csv files
# ###########################################
# this assumes all files will be in the same directory
# if this isn't the case when we get the data, we can adjust this method

def generate_csvs(data_dir: str, image_t1_glob: str, image_t2_glob: str, label_csv_glob: str, output_dir: str) -> None:
    """

    :param data_dir: the base directory containing all of the data
    :param image_t1_glob: a glob that uniquely identifies t1 images
    :param image_t2_glob: a glob that uniquely identifies t2 images
    :param label_csv_glob: a glob that uniquely identifies label csvs/fcsvs
    :param output_dir: the directory to write the new niftynet csvs to
    :return:
    """
    # load file names
    images_t1 = glob(join(data_dir, image_t1_glob))
    images_t2 = glob(join(data_dir, image_t2_glob))
    label_fcsvs = glob(join(data_dir, label_csv_glob))

    # making the assumption that lexical sort aligns pairs
    images_t1.sort()
    images_t2.sort()
    label_fcsvs.sort()

    # safety check that everything is the same length
    print(len(images_t1), len(images_t2), len(label_fcsvs))
    assert len(images_t1) == len(images_t2)
    assert len(images_t1) == len(label_fcsvs)

    # shuffle the data the same way
    # images_t1 = array(images_t1)
    # images_t2 = array(images_t2)
    # label_csvs = array(label_csvs)
    # perm = permutation(len(images_t1))
    # images_t1 = images_t1[perm]
    # images_t2 = images_t2[perm]
    # label_csvs = label_csvs[perm]

    total_size = len(images_t1)
    training_size = int(TRAINING_PERCENTAGE * total_size)
    validation_size = int(VALIDATION_PERCENTAGE * total_size)
    inference_size = int(INFERENCE_PERCENTAGE * total_size)
    print("training samples: %d \nvalidation samples: %d \ninference samples: %d" % (
        training_size, validation_size, inference_size))

    # get the number of digits so that the key is the correct size
    digits = len(str(len(images_t1)))

    # create the ouput_dir if it does not exist
    if not isdir(output_dir):
        mkdir(output_dir)

    # open all the csv files to be written to
    u_id = get_unique_run_id()
    image_t1_csv = open(join(output_dir, "%s_t1.csv" % u_id), 'w')
    image_t2_csv = open(join(output_dir, "%s_t2.csv" % u_id), 'w')
    labels_csv = open(join(output_dir, "%s_labels.csv" % u_id), 'w')
    data_split_csv = open(join(output_dir, "%s_split.csv" % u_id), 'w')

    # use a closure to make the writing to csvs cleaner
    def write_to_csvs(p_key: str, array_index: int, subset_string: str) -> None:
        image_t1_csv.write("{key},{fname}\n".format(key=p_key, fname=images_t1[array_index]))
        image_t2_csv.write("{key},{fname}\n".format(key=p_key, fname=images_t2[array_index]))
        labels_csv.write("{key},{fname}\n".format(key=p_key, fname=label_fcsvs[array_index]))
        data_split_csv.write("{key},{subset}\n".format(key=p_key, subset=subset_string))
        return

    # pre compute the training + validation size
    training_plus_validation = training_size + validation_size
    for index in range(len(images_t1)):
        # this key links together the label_fcsv,t1 & t2 images
        primary_key = str(index).zfill(digits)

        if index < training_size:
            # write all of the training set
            write_to_csvs(p_key=primary_key, array_index=index, subset_string="Training")

        elif index < training_plus_validation:
            # write all of the validation set
            write_to_csvs(p_key=primary_key, array_index=index, subset_string="Validation")

        else:
            # write all remaining as inference
            write_to_csvs(p_key=primary_key, array_index=index, subset_string="Inference")

    image_t1_csv.close()
    image_t2_csv.close()
    labels_csv.close()
    data_split_csv.close()

    return

# run this file independently to test functions
# if __name__ == '__main__':
#     generate_csvs(
#         data_dir="/Users/abpwrs/research/SINAPSE/20190329_FiducialFinder/SmallData/",
#         image_t1_glob="*_t1w.nii.gz",
#         image_t2_glob="*_t2w.nii.gz",
#         label_csv_glob="*.fcsv",
#         output_dir="/Users/abpwrs/test_csv_out/"
#     )
# ###########################################
