import pandas as pd

from utils import get_fiducial_list


# functions for fcsv manipulation and fiducial data extraction
# ############################################################
def get_fiducials_from_file(fcsv_file: str) -> dict:
    """

    :param fcsv_file: fcsv file to extract fiducial points from
    :return: dictionary { fiducial_name -> [ x, y, z ] }
    """
    fiducial_points = {}

    # this read_csv likely needs more parameters
    fcsv_df = pd.read_csv(fcsv_file, comment='#', header=None)

    for fiducial in get_fiducial_list():
        # TODO: this likely needs formatting (LPS vs RAS)
        fiducial_points[fiducial] = fcsv_df.loc[fcsv_df[0] == fiducial].values[0][1:4]

    return fiducial_points


# run this file independently to test functions
# if __name__ == '__main__':
#     from sys import argv
#
#     print(get_fiducials_from_file(argv[1]))
# ############################################################
