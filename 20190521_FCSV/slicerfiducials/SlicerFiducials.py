# -*- coding: utf-8 -*-
# File: SlicerFiducials.py
# Author: Arjit Jain <thearjitjain@gmail.com>
import pandas as pd
import itk
import numpy as np

indices = [
    "AC",
    "BPons",
    "CM",
    "LE",
    "PC",
    "RE",
    "RP",
    "RP_front",
    "SMV",
    "VN4",
    "callosum_left",
    "callosum_right",
    "dens_axis",
    "genu",
    "l_caud_head",
    "l_corp",
    "l_front_pole",
    "l_inner_corpus",
    "l_lat_ext",
    "l_occ_pole",
    "l_prim_ext",
    "l_sup_ext",
    "l_temp_pole",
    "lat_left",
    "lat_right",
    "lat_ven_left",
    "lat_ven_right",
    "left_cereb",
    "left_lateral_inner_ear",
    "m_ax_inf",
    "m_ax_sup",
    "mid_basel",
    "mid_lat",
    "mid_prim_inf",
    "mid_prim_sup",
    "mid_sup",
    "optic_chiasm",
    "r_caud_head",
    "r_corp",
    "r_front_pole",
    "r_inner_corpus",
    "r_lat_ext",
    "r_occ_pole",
    "r_prim_ext",
    "r_sup_ext",
    "r_temp_pole",
    "right_lateral_inner_ear",
    "rostrum",
    "rostrum_front",
    "top_left",
    "top_right",
]

header = {}
header[
    "original_markup"
] = "# Markups fiducial file version = 4.10\n# CoordinateSystem = 0\n# columns = id,x,y,z,ow,ox,oy,oz,vis,sel,lock,label,desc,associatedNodeID\n"
header["original"] = "#label,x,y,z,sel,vis\n"


class SlicerFiducials:
    def __init__(
        self,
        name: str = None,
        df: pd.DataFrame = None,
        image: str = None,
        convertRAStoLPS: bool = True,
    ):
        """
        constructor for this class. this class can be initialized by either the name(path) of the fcsv file or by
        a pandas dataframe object. fcsv file is read only when no dataframe has been passed.
        :param name: path of the fcsv file
        :param df: pandas dataframe object
        :param image: path to the image
        :param convertRAStoLPS: whether to convert Right-Anterior-Superior to Left-Posterior-Superior
        """
        if name is None and df is None:
            raise ValueError
        self.name = name
        self.df = df
        self.image_path = image
        self.convertRAStoLPS = convertRAStoLPS
        self.image = None
        if self.image_path is not None:
            self.image = itk.imread(self.image_path)
        self.standard = None
        self.length = None
        self.fiducialToPhysical = {}
        if self.df is None:
            self.df = pd.read_csv(self.name, comment="#", header=None)
        self.set_params()
        self.create_dict()
        print(self.df)

    def __str__(self):
        return str(self.fiducialToPhysical)

    def euclidean_distance(self, fid1: str, fid2: str) -> float:
        """
        :param fid1: label of fiducial 1
        :param fid2: label of fiducial 2
        :return: the eucliedean distance between fid1 and fid2 in the pixel space
        """
        return np.linalg.norm(
            self.fiducialToPhysical[fid1] - self.fiducialToPhysical[fid2]
        )

    def __iter__(self):
        """
        :return: an iterable of the form label, point where label is a string and point is the 3D location
        """
        return iter(self.fiducialToPhysical.items())

    @staticmethod
    def diff_files(file1, file2):
        """
        :param file1:
        :param file2:
        :return: SlicerFiducials object calculating the difference between corresponding fiducials of file1 and file2
        """
        if file1.length != file2.length:
            raise ValueError
        df = file1.df.copy()
        df2 = file2.df.copy()
        df["x"] = df["x"] - df2["x"]
        df["y"] = df["y"] - df2["y"]
        df["z"] = df["z"] - df2["z"]
        return SlicerFiducials(df=df)

    def names(self):
        """
        :return: list of labels of all the fiducials in the object
        """
        return list(self.df["label"])

    def set_params(self):
        """
        :return:
        """
        self.length = self.df.shape[0]
        if self.df.shape[1] == 6:
            self.standard = "original"
            self.df.columns = ["label", "x", "y", "z", "sel", "vis"]

        elif self.df.shape[1] == 14:
            self.standard = "original_markup"
            self.df.columns = [
                "id",
                "x",
                "y",
                "z",
                "ow",
                "ox",
                "oy",
                "oz",
                "vis",
                "sel",
                "lock",
                "label",
                "desc",
                "associatedNodeID",
            ]
        else:
            raise "Please check your input FCSV file"
        self.df.index = self.df["label"]
        self.df = self.df.reindex(labels=indices)

    def create_dict(self):
        """
        :return:
        """
        labels = self.df["label"]
        x = np.array(self.df["x"]).reshape(-1, 1)
        y = np.array(self.df["y"]).reshape(-1, 1)
        z = np.array(self.df["z"]).reshape(-1, 1)
        if self.convertRAStoLPS:
            x = -1 * x
            y = -1 * y
        vector = np.concatenate((x, y, z), axis=1)
        self.fiducialToPhysical = dict(zip(labels, vector))

    def get_format(self, format: str) -> pd.DataFrame:
        """
        :param format: desired format
        :return: dataframe in the desired format
        """
        dfToReturn = None
        if format == "original":
            dfToReturn = pd.DataFrame(self.df[["label", "x", "y", "z", "sel", "vis"]])
        elif format == "original_markup":
            ow_ox_oy = pd.DataFrame(
                np.zeros((self.length, 3), dtype=float), columns=["ow", "ox", "oy"]
            )
            ow_ox_oy.index = self.df.index
            lock = pd.DataFrame(np.zeros((self.length, 1)), columns=["lock"])
            lock.index = self.df.index
            oz = pd.DataFrame(np.ones((self.length, 1), dtype=float), columns=["oz"])
            oz.index = self.df.index
            id = pd.DataFrame(
                ["vtkMRMLMarkupsFiducialNode_" + str(i) for i in np.arange(self.length)]
            )
            id.index = self.df.index
            temp_df = pd.concat(
                (
                    id,
                    self.df[["x", "y", "z"]],
                    ow_ox_oy,
                    oz,
                    self.df[["vis", "sel"]],
                    lock,
                    self.df["label"],
                ),
                ignore_index=False,
                axis=1,
            ).round(3)
            temp_df = temp_df.reindex(
                columns=temp_df.columns.tolist() + ["desc", "associatedNodeID"]
            )
            temp_df.columns = [
                "id",
                "x",
                "y",
                "z",
                "ow",
                "ox",
                "oy",
                "oz",
                "vis",
                "sel",
                "lock",
                "label",
                "desc",
                "associatedNodeID",
            ]
            dfToReturn = pd.DataFrame(temp_df)
        else:
            raise NotImplementedError
        dfToReturn.index = dfToReturn["label"]
        return dfToReturn.reindex(labels=indices)

    def query(self, name: str, space: str = "physical") -> np.ndarray:
        """
        query for single landmark point using label. by default in physical space
        :param name: label of the landmark point
        :param space: 'physical' or 'index'.
        :return:
        """
        physical = self.fiducialToPhysical[name]
        if space == "index":
            assert self.image_path is not None
            return np.array(
                self.image.TransformPhysicalPointToContinuousIndex(physical)
            )
        return physical

    def write(self, name: str, format: str = "original") -> None:
        """
        Writes data to file in the desired format
        :param name: path to save
        :param format: format to save in
        :return:
        """
        format_df = self.get_format(format)
        file = open(name, "w")
        file.write(header[format])
        format_df.to_csv(file, index=False, header=False, float_format="%.3f")
        file.close()
