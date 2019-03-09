#!/usr/bin/env bash
# Author: abpwrs
# Fri Mar  8 13:28:11 CST 2019


# Script parameters
# 1 --> directory full of images to augment
# 2 --> directory to which augmented images will be written
# 3 --> and integer (0 for images) (1 for label maps) (zero by default)
# 4 --> full path to an augmentation file you want to use (not required)
# 5 --> optional parameter to specify glob to match

if [ $# -lt 4 ]; then
    echo "Correct Usage"
    echo "${0} <full-path-to-directory-of-images> <full-path-to-output-directory> <is-label ? 1 : 0> <full-path-to-augmentation.json> <optional-glob>"
    exit -1
fi

INPUT_DIR=${1}
OUTPUT_DIR=${2}
IS_LABEL=${3}
AUG_FILE=${4}

GLOB="*"

if [ $# -eq 5 ]; then
    GLOB=${5}
fi

for input_file in ${INPUT_DIR}/$GLOB; do
    echo "Processing: ${input_file}"
    python main.py -i ${input_file} -o ${OUTPUT_DIR} -l ${IS_LABEL} -a ${AUG_FILE}
done


