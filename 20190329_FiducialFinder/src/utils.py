from json import load
import SimpleITK as sitk
import numpy as np
from time import strftime


# functions for uniquely identifying runs/models
# ##############################################
def get_unique_run_id() -> str:
    """

    :return: a unique string consisting of the time (to the minute) and the fiducials
    """
    unique_run_id = "uid_%s_%s" % (get_fiducial_string(), strftime("%Y%m%d_%H%M"))
    return unique_run_id


def get_fiducial_string() -> str:
    """

    :return: one string with all the fiducial names separated by '_'
    """
    return "_".join(get_fiducial_list())


def get_fiducial_list() -> list:
    """

    :return: a list of fiducial point names as strings
    """
    with open("../fiducials.json", 'r') as f:
        fiducial_list = load(f)["fiducials"]
    return fiducial_list


# ##############################################


# Scale fiducial location to be between 0-1
# these functions can take in an sitk.Image or a np.array, but not both
# ##############################################
def down_scale_fiducial(fiducial: list, arr: np.array) -> np.array:
    """

    :param fiducial:
    :param arr:
    :return:
    """
    if arr is not None:
        pass
    else:
        raise Exception("arr must be defined in the args of down_scale_fiducial")
    pass


def up_scale_fiducial(fiducial: list, arr: np.array) -> np.array:
    """

    :param fiducial:
    :param arr:
    :return:
    """
    if arr is not None:
        pass
    else:
        raise Exception("arr must be defined in the args of up_scale_fiducial")
    pass
# ##############################################


# run this file independently to test functions
# ##############################################
# if __name__ == '__main__':
#     print(get_unique_run_id())
# ##############################################
