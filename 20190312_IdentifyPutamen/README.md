# Identify Putamen

A web tool that quickly identifies the quality of input or output data for deep learning models.

## Setup

Run the available_putamen_files_to_csv.py function to extract the desired files to a csv file.  Conditions of files extracted and extracting location should be changed in this function if this program is used for files other than the original putamen files (3-12-19) (See TODO in available_putamen_files_to_csv.py).

```bash
python available_putamen_files_to_csv.py
```

IF NEEDED, Change the output file name of the identified images in server.js (should be a csv)
```javascript
const outputFilePath = __dirname + <filepath>
```

Install node dependencies

```bash
npm install
```


## Program Execution

```bash
node server.js
```

Open browser to http://127.0.0.1:8081/Identify_Putamen.html

## Use of tool

![image](https://raw.githubusercontent.com/BRAINSia/SINAPSE/master/20190312_IdentifyPutamen/Identify%20Good%20Putamen_Edited.png)

Looking at the black and white image, determine if it is good or bad and click the corresponding button (the key 'b' and 'g' are shortcuts for the bad and good buttons, respectively).  Choosing good or bad automatically moves on to the next image.

If a mistake was made, the back button returns to a previous image (shortcut is '<' i.e. 'SHIFT' + ',')

To save all identified images to a file, click the Save Progress button (shortcut 's')

## Results

After using the web tool to identify 56 flagged (potentially bad) files, I opened each of them in Slicer to give a more detailed inspection.  The final evaluations were documented in manually_evaluated_identified_putamen.csv.  As we can see from this file, the following files were the only ones considered unfit for use in Deep Learning Models.

* /Shared/johnsonhj/2018Projects/20181002_LesionMappingBAW/20181017_niftinet_data_inputs/images/c0008s0018_c0008s0018t01_lr_combined_dense_seg.nii.gz
* /Shared/johnsonhj/2018Projects/20181002_LesionMappingBAW/20181017_niftinet_data_inputs/images/c0004s0020_c0004s0020t01_lr_combined_dense_seg.nii.gz
* /Shared/johnsonhj/2018Projects/20181002_LesionMappingBAW/20181017_niftinet_data_inputs/images/c0011s0003_c0011s0003t01_lr_combined_dense_seg.nii.gz
* /Shared/johnsonhj/2018Projects/20181002_LesionMappingBAW/20181017_niftinet_data_inputs/images/c0009s0002_c0009s0002t01_lr_combined_dense_seg.nii.gz
* /Shared/johnsonhj/2018Projects/20181002_LesionMappingBAW/20181017_niftinet_data_inputs/images/c0009s0009_c0009s0009t01_lr_combined_dense_seg.nii.gz
