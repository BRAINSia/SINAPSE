import slicer #this import statement has to be commented out for the time being when generating html docs
import time
import argparse
import os.path

"""
Description:
This script works by calling the python packaged with slicer using the --python-script cmd call, and running slicer
without its gui, using --no-main-window
The specific path to the slicer .exe file that you want to use must be provided
If you dont want to have to include the path to hte python script, you can move it to the current directory and then
call the script using CreateSegmentationFile.py
Where it is located
"""

"""
Inputs:
ColorTableInput: text file containing the lookup table information that is to be applied to the labelmap
LabelMapInput: Labelmap with numerical labels corresponding to the ColorTable
FileOutputLocation: directory were segmentation file is to be written

Output:
Segmentation file of type .seg.nrrd to directory [FileOutputLocation]

"""


# add in list parse to be called

# add in a LUT parse


def write_segmentation_file(ColorTableInput, LabelMapInput, FileOutputLocation):
    """

    This function takes in a ColorTable, LabelMap, and FileOutput Location, and creates and writes a segmentation Image

    :param ColorTableInput: ColorTable to use

    :param LabelMapInput: LabelMap to use

    :param FileOutputLocation: Desired file output location for segmentation images

    :returns:	int -- returncodePlaceholder



    **Slicer Functions used by write_segmentation_file:**

        *loadColorTable()*: Loads in a colortable corresponding to whatever the ColorTableInput for the write_segmentation_file function is

        *loadLabelVolume()*: Loads in the corresponding labelmapvolume that LabelMapInput references

        *getNode()*: returns displaynode for current volume loaded into slicer

        *getDisplayNode()*: returns the display node for whatever input node is provided

        *SetAndObserveColorNodeID()*: this is used to set the colornode to the current LUT that has been provided

        *AddNewNodeByClass()*: slicer creates a new node based off the input string provided. in this case the input string for a segmentation node is
        'vtkMRMLSegmentationNode'

        *ImportLabelmapToSegmentationNode( [volume] , [segmentation node])* : imports volume provided and creates segmentations. New segmentations are saved to segment node

        *saveNode( [nodepath] , [outputfilepath] )*: segmentation node is written and saved as a .seg.nrrd file


    """

    # check to make sure Lookuptable and Labelmaps exist before continuing. If they do not exist , exit and return an error

    if os.path.isfile(ColorTableInput):
        print("colortable exists")
    else:
        print("ERROR: LookUpTable Does Not Exist. Exiting script")
        slicer.util.exit()
        sys.exit()

    if os.path.isfile(LabelMapInput):
        print("LabelMap exists")
    else:
        print("ERROR: LabelMap does not exist. Exiting script")
        slicer.util.exit()
        sys.exit()

    # if output directory doesnt exist, create the directory for storing the segmentation output
    if not os.path.exists(FileOutputLocation):
        os.makedirs(FileOutputLocation)

    # file ending is going to be .nii.gz (crop off the last 7 elements of string )
    # use rfind to find last occurance of "/" in the file path
    filenameLocation = LabelMapInput.rfind("/")
    totalLength = len(LabelMapInput)

    # filename+1 excludes the / found , so that the string outputted is just the SubjectFileName for the LabelMap
    # crop off .nii.gz of the filenameLocation string, to get the current ID. (last 7 elements of filenameLocation)
    # FileID is what Slicer uses for the Main node label, being the filename with the filetype stripped off the end
    FileID = LabelMapInput[filenameLocation + 1:totalLength - 7]
    currentSubjectFileName = FileID + ".seg.nrrd"

    fullOutputPath = FileOutputLocation + "/" + currentSubjectFileName

    print("\n")
    print ("current LabelVolume Slicer Node ID:		 " + str(FileID))
    print("\n")

    # load in the lookuptable
    slicer.util.loadColorTable(ColorTableInput)
    # load in labelvolume
    slicer.util.loadLabelVolume(LabelMapInput)

    singlenode = slicer.util.getNode(FileID)  # FileID is the file name stripped of the ending filetype identifiers
    # display node contains the reference to the colortable that is currently being used
    displayNode = singlenode.GetDisplayNode()

    # GetColorNodeID() finds the label for the current Color table being used
    colorNodeID = displayNode.GetColorNodeID()
    # so far as long as only one color table is loaded, the node will be labeled as "vtkMRMLColorTableNode1"
    displayNode.SetAndObserveColorNodeID("vtkMRMLColorTableNode1")

    labelmapVolumeNode = getNode(FileID)
    # create the segmentation node
    seg = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLSegmentationNode')
    # import the loaded labelmap to the segmentation, labelmap volume already has lookup table applied
    slicer.modules.segmentations.logic().ImportLabelmapToSegmentationNode(labelmapVolumeNode, seg)

    t0 = time.time()

    # save node as output file
    # file will be written out based off the FileID that was provided to Slicer,
    slicer.util.saveNode(slicer.mrmlScene.GetNodeByID("vtkMRMLSegmentationNode1"), fullOutputPath)

    t1 = time.time()

    total = t1 - t0

    print(total, " Time")
    # have to save as a .seg.nrrd file, otherwise data will be corrupted
    print("\n")
    print("Segmentation file is created")
    print("\n")

    # exit command
    slicer.util.exit()

    return


# need to wrap the call of the function with this, so that the sphinx documentation is generated properly
if __name__ == '__main__':

    # argument parsing for all arguments after the call of this script
    parser = argparse.ArgumentParser()
    # argpasre only takes into account the arguments that are passed AFTER the python script call.
    parser.add_argument("LookUpTable",
                        help="location of lookuptable to be applied to LabelMap")  # equivalent to sys.argv[1] after script
    parser.add_argument("LabelMap",
                        help="location of labelmap to create segmentation file")  # equivalent to sys.argv[2] after script
    parser.add_argument("FileOutputLocation",
                        help="output location of segmentation file that has been created")  # equivalent to sys.argv[3] after script
    args = parser.parse_args()

    # argument dict to individual variables
    ColorTableInput = args.LookUpTable
    LabelMapInput = args.LabelMap
    FileOutputLocation = args.FileOutputLocation
    ttotal = time.time()
    write_segmentation_file(ColorTableInput, LabelMapInput, FileOutputLocation)
    ttotalend = time.time()
    alltime = ttotalend - ttotal

    print(alltime)
