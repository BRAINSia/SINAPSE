# Resize Labels To Images N-d
> [Alex Powers](mailto:alexander-powers@uiowa.edu?subject=[GitHub]%20SINAPSE%20ResizeLabelsToImages2D)

WARNING: Files must be named such that lexical sort aligns images with the corresponding label

## Setup
Create a conda env:
```bash
conda env create -f environment.yml
```
or install the required libraries directly
```bash
pip install -r requirements.txt
```
Or install the one dependency (SimpleITK)
```bash
conda install -c simpleitk SimpleITK
```
or
```bash
pip install SimpleITK
```
## Program Execution
```text
./resize_images.sh <full-path-to-label-dir> \
<full-path-to-image-directory> <full-path-to-output-dir>
```
Note: The only parameter in the source code is pixel-type at the top of `main.py`