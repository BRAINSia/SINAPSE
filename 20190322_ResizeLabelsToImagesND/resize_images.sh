#!/usr/bin/env bash
# Author: abpwrs
# Fri Mar 22 11:27:44 CDT 2019

# Script parameters
# 1 --> directory full of labels to resize
# 2 --> directory full of images to which labels will be re-sized
# 3 --> output directory where re-sized images will be written to


if [[ $# -lt 3 ]]; then
    echo "Correct Usage"
    echo "${0} <full-path-to-label-dir> <full-path-to-image-dir> <full-path-to-output-dir>"
    exit -1
fi

LABEL_DIR=${1}
IMAGE_DIR=${2}
OUT_DIR=${3}

# create file of sorted images
SORTED_FILE="sorted_files_for_resizing.csv"
rm ${SORTED_FILE}
touch ${SORTED_FILE}
python ./sort_files.py -i ${IMAGE_DIR} -l ${LABEL_DIR} -o ${SORTED_FILE}

# use sorted files to run resizing script
while IFS=, read -r image_file label_file
do
    if [[ -f ${image_file} && -f ${label_file} ]]; then
        echo "processing: ${label_file}"
        python main.py -i ${image_file} -l ${label_file} -o ${OUT_DIR} &>/dev/null
    fi
done < ${SORTED_FILE}

rm ${SORTED_FILE}
