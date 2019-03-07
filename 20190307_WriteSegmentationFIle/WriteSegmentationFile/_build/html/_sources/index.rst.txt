.. CreateSegmentationFile documentation master file, created by
   sphinx-quickstart on Fri Mar  1 11:30:50 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

CreateSegmentationFile documentation
==================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Description
============================

   * This script works by calling the python packaged with slicer using the --python-script cmd call, and running slicer
     without its gui, using --no-main-window
   * The specific path to the slicer .exe file that you want to use must be provided
   * If you dont want to have to include the path to hte python script, you can move it to the current directory and
     then call the script using CreateSegmentationFile.py Where it is located



*an example call of MainFunctionSegmentation.py would be:*

   /PATHTO/Slicer --no-main-window --python-script
   /PATHTO/MainFunctionSegmentation.py /PATHTO/LUT.txt
   /PATHTO/inputimage.nii.gz /PATHTO/outputfolder


===========================


Function
================================================


.. automodule:: MainFunctionSegmentation
   :members:

