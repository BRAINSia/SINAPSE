#!/usr/bin/env bash
# Author: "abpwrs"
# Date: 20190422

# args:
# 1 -- directory of images to convert
# 2 -- optional ext of image

# must be run from project root



# input validation
if [[ $# -lt 1 ]]; then
	echo "Usage: $0 <images-directory> <optional-image-ext>"
	exit
fi

# script here
EXT="_t1w.nii.gz"
IMAGE_DIR=$1

if [[ $# -eq 2 ]]; then
	EXT=$2
fi

for fcsv_fn in $IMAGE_DIR/*.fcsv; do
	fname=$(basename $fcsv_fn .fcsv)
	echo $fname
	image_param=$IMAGE_DIR$fname$EXT
	echo $image_param
	python scripts/fiducial_to_image.py -f $fcsv_fn -i $image_param 
done



