#!/usr/bin/env bash
# Author: abpwrs
# Fri Mar  8 13:13:13 CST 2019

if [ $# -ne 1 ]; then
	echo "... Incorrect Usage ..."
	echo "Usage: ${0} ProjectNameNoSpaces"
	exit -1
fi

DATE=`date +%Y%m%d`
PROJECT_NAME=${1}
DIR_NAME="${DATE}_${PROJECT_NAME}"

mkdir ${DIR_NAME}

pushd ${DIR_NAME}
	echo "# ${PROJECT_NAME}" >> README.md
popd

git add ${DIR_NAME}


