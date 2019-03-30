from json import load
from time import strftime


# functions for uniquely identifying runs/models
# ##############################################
def get_unique_run_id() -> str:
    unique_run_id = "uid_%s_%s" % (get_fiducial_string(), strftime("%Y%m%d_%H%M"))
    return unique_run_id


def get_fiducial_string() -> str:
    return "_".join(get_fiducial_list())


def get_fiducial_list() -> list:
    with open("../fiducials.json", 'r') as f:
        fiducial_list = load(f)["fiducials"]
    return fiducial_list

# run this file independently to test functions
# if __name__ == '__main__':
#     print(get_unique_run_id())
# ##############################################
