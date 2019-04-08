#!/usr/bin/env bash
# Author: "abpwrs"
# Date: 20190403

# args:
# 1 -- the name of the network you want to add

if [[ $# -ne 1 ]]; then
	echo "Usage: $0 <name-of-network>"
	exit -1
fi

# script:

PROJECT_ROOT=$(pwd)
NETWORK_NAME=${1}

# make a directory for:
# source code --> networks/
# model checkpoints --> models/
# model predictions --> preds/
mkdir -p ${PROJECT_ROOT}/networks/${NETWORK_NAME}
mkdir -p ${PROJECT_ROOT}/models/${NETWORK_NAME}
mkdir -p ${PROJECT_ROOT}/preds/${NETWORK_NAME}

touch ${PROJECT_ROOT}/networks/${NETWORK_NAME}/${NETWORK_NAME}.py
touch ${PROJECT_ROOT}/models/${NETWORK_NAME}/.gitkeep
touch ${PROJECT_ROOT}/preds/${NETWORK_NAME}/.gitkeep

# provide a the default paths in the config.ini for ease of use
cat > ${PROJECT_ROOT}/networks/${NETWORK_NAME}/${NETWORK_NAME}_config.ini << EOF
; ${NETWORK_NAME} Configuration File
; the following file path are provided for your convenience
;
; model output and data csv file directory
; ${PROJECT_ROOT}/models/${NETWORK_NAME}/
;
; prediction output directory
; ${PROJECT_ROOT}/preds/${NETWORK_NAME}/
;
; network source code directory
; ${PROJECT_ROOT}/networks/${NETWORK_NAME}/
;
;
;;; your config here ;;;


EOF