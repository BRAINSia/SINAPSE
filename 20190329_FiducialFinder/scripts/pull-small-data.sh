#!/usr/bin/env bash
temp_dir=/tmp/temporary_data_`date +%Y%m%d`
git clone git@github.uiowa.edu:SINAPSE/UIOWA2018_LesionMapping.git $temp_dir 
cp $temp_dir/SmallData/* ./SmallData/
rm -rf $temp_dir

