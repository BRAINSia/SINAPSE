#!/bin/bash
#each one of these currently contains 17 points to create the transform
#current file containing paths is /home/kknoernschild/atlasinputs.csv

#when calling from command line use .....
# [arg1  = bash file location csv]
# [arg2 = file directory with all images and their individual fcsv]

#general file structure for the final output file is 
#$[subj_study]_5AtlasAntsOutput
# will always use nearest neighbor for segmentation NearestNeighbor_label_AffineTransform-Linearimage.nii"

#450  860 1009 1740 seconds for 2/3/4/5 radius 2 subjects


#every subject session is saved as its own folder. I can go manually join these before we send them out
#
#
#	subject
#
#		-antsJointFusionResults
#			- [SubjectNameAndSession]_5AtlasTestOutput_[SegTransformType]_label_[ImageTransformType]-linear.nii
#
#		-ImageFilesLinear - contains the atlas images transformed to the image space using linear interpolation
#
#			- [atlasnumber]_Label_2_[SubjectNameAndSession]_[TransformName].nii
#				- ex)	atlas0_Linear_2_sub-Luise274_ses-20150615_run-100555_T1w.nii 	
#
#		-ImageFilesNearestNeighbor - contains the atlas segmentation images transformed to image space using nearest neighbor interpolation
#
#			- [atlasnumber]_Label_2_[SubjectNameAndSession]_[TransformName].nii	
#				- ex)	atlas0_Label_2_sub-Luise274_ses-20150615_run-100555_T1w_AffineTransform.nii
#
#		-TransformFiles (contains transform and inverse transform files for both the linear image and atlas seg transforms)
#	
#			- transform files name structure --- [atlasnumber]_[SubjectNameAndSession]_[TransformType].h5
#				- ex)	testatlas0_2_sub-Luise274_ses-20150615_run-100555_T1w_AffineTransform_Linear.h5
#							                                OR			 
#							 --- [atlasnumber]_[SubjectNameAndSession]_[TransformType]_Inverse.h5
#				- ex)	testatlas0_2_sub-Luise274_ses-20150615_run-100555_T1w_AffineTransform_Linear_Inverse.h5
#
#
#


## 	copy secondary script and use n = 20 instead of n = 5






start=$SECONDS

declare -a fcsv_path
declare -a atlas_path
declare -a atlas_seg

declare -i count=0

while IFS=, read -r col1 col2 col3
do
	fcsv_path[$count]=$col1
	atlas_path[$count]=$col2
	atlas_seg[$count]=$col3
	((count++))

done < $1


declare -a atlas_fcsv_filepaths
declare -a atlas_img_filepaths
declare -a atlas_label_filepaths

lenatlas=${#fcsv_path[@]}
echo $lenatlas
for ((n=0;n<lenatlas;n++))
do
	atlas_fcsv_filepaths[$n]=${fcsv_path[$n]}
	atlas_img_filepaths[$n]=${atlas_path[$n]}
	atlas_label_filepaths[$n]=${atlas_seg[$n]}
	#echo ${atlas_seg[$n]}
	#echo ${atlas_path[$n]}
	#echo ${atlas_seg[$n]}

done





# atlas_fcsv_filepaths=(${fcsv_path[0]} ${fcsv_path[1]} ${fcsv_path[2]} ${fcsv_path[3]} ${fcsv_path[4]})
# atlas_img_filepaths=(${atlas_path[0]} ${atlas_path[1]} ${atlas_path[2]} ${atlas_path[3]} ${atlas_path[4]})
# atlas_label_filepaths=(${atlas_seg[0]} ${atlas_seg[1]} ${atlas_seg[2]} ${atlas_seg[3]} ${atlas_seg[4]})


#need to find every T1w image that is located in current directory , store those into an array, with subject/folder names for file naming

#find all images 
directory=$2
array=(`find $directory -name "*.nii"`)
array3=(`find $directory -name "*.nii"`)
array2=(`find $directory -name "*.fcsv"`)


len=${#array[@]}
echo $len  #for x in $len
for ((x=3;x<len;x++))
do
#turn inputimage into a commandline input
inputImage="${array[$x]}" #change this to be an individual file name from the input when you start batch processing
inputFCSV="${array2[$x]}"
WTSFILE="$(pwd)/mplmk.wts"


printf "\n" printf "\n" printf "\n"
subj_study=`echo "$inputImage" | sed -r "s/.+\/(.+)\..+/\1/"`
echo $inputFCSV
echo $inputImage
echo $subj_study
printf "\n" printf "\n" printf "\n"

#need to get a string for filenaming that is subjectanddate_atlas.h5

#create a folder for each subject and its study, wiht the output result

mkdir -p "newAtlasMaps_run2"
mkdir -p $subj_study
mkdir -p $subj_study/TransformFiles
mkdir -p $subj_study/ImageFilesLinear
mkdir -p $subj_study/ImageFilesNearestNeighbor
mkdir -p $subj_study/antsJointFusionResults


declare -a ants_atlas_seg
declare -a atlas_new_im
declare -a atlas_new_im_only_brain
declare -a maskimagesout

	for((i=0;i<18;i++))
	do
		BINDIR=/Users/johnsonhj/src/BT-11/bin

				ONLYBRAIN="$(pwd)/${subj_study}/ImageFilesLinear/atlas${i}_Label_2_${subj_study}_${TFMTYPE2}_skull_cropped.nii"
				#crop the image to just the brain
				python ExtractBrain.py ${atlas_img_filepaths[i]} ${atlas_label_filepaths[i]} $ONLYBRAIN
				atlas_new_im_only_brain[$i]="$ONLYBRAIN"

		##### FIRST TRANSFORM FOR IMAGE ###########
				TFMTYPE=AffineTransform

				INTERPMODE=Linear
				#if [[ ${TFMTYPE} ==  "VersorRigid3DTransform" ]]; then
				#	INTERPMODE=ResampleInPlace
				#fi

				M2F_TFM="$(pwd)/${subj_study}/TransformFiles/testatlas${i}_2_${subj_study}_${TFMTYPE}_${INTERPMODE}.h5"


				#moving and fixed landmark files
				MLMKFILE=${atlas_fcsv_filepaths[i]}
				#echo $inputImage
				FLMKFILE=$inputFCSV
				#echo $inputFCSV

				${BINDIR}/BRAINSLandmarkInitializer \
				   --inputMovingLandmarkFilename "${MLMKFILE}" \
				   --inputFixedLandmarkFilename "${FLMKFILE}" \
				   --inputWeightFilename "${WTSFILE}" \
				   --outputTransformType ${TFMTYPE} \
				   --outputTransformFilename "${M2F_TFM}"

				PIXELTYPE=float
				FIMGFILE=$inputImage
				MIMGFILE=$ONLYBRAIN


				OUTFILE="$(pwd)/${subj_study}/ImageFilesLinear/atlas${i}_${INTERPMODE}_2_${subj_study}.nii"
				atlas_new_im[$i]="$OUTFILE"
				#resample image
				${BINDIR}/BRAINSResample \
				   --interpolationMode ${INTERPMODE} \
				   --warpTransform "${M2F_TFM}" \
				   --pixelType "${PIXELTYPE}" \
				   --outputVolume "${OUTFILE}" \
				   --inputVolume "${MIMGFILE}" \
				   --referenceVolume "${FIMGFILE}"

		##### SECOND TRANSFORM FOR LABELMAP ##########

				TFMTYPE2=AffineTransform			
				INPERPMODE2=NearestNeighbor
				
				#moving and fixed landmark files
				MLMKFILE2=${atlas_fcsv_filepaths[i]}
				FLMKFILE2=$inputFCSV

				M2F_TFM2="$(pwd)/${subj_study}/TransformFiles/testatlas${i}_2_${subj_study}_${TFMTYPE2}_${INPERPMODE2}.h5"

				${BINDIR}/BRAINSLandmarkInitializer \
				   --inputMovingLandmarkFilename "${MLMKFILE2}" \
				   --inputFixedLandmarkFilename "${FLMKFILE2}" \
				   --inputWeightFilename "${WTSFILE}" \
				   --outputTransformType ${TFMTYPE2} \
				   --outputTransformFilename "${M2F_TFM2}"

				PIXELTYPE2=uchar
				FIMGFILE2=$inputImage

				OutputRigid="$(pwd)/${subj_study}/ImageFilesNearestNeighbor/atlas${i}_Label_2_${subj_study}_${TFMTYPE2}.nii"
				MLABELFILE=${atlas_label_filepaths[i]}
				ants_atlas_seg[$i]=$OutputRigid
				#resample image
				${BINDIR}/BRAINSResample \
				   --interpolationMode ${INPERPMODE2} \
				   --warpTransform "${M2F_TFM2}" \
				   --pixelType "${PIXELTYPE2}" \
				   --outputVolume "${OutputRigid}" \
				   --inputVolume "${MLABELFILE}" \
				   --referenceVolume "${FIMGFILE2}"


				#create image mask of the image the atlases are being transformed to
				MaskResult="$(pwd)/${subj_study}/ImageFilesLinear/atlas${i}_Label_2_${subj_study}_${TFMTYPE2}_mask.nii"
				maskimagesout[$i]=$MaskResult
				python MaskImage.py $OUTFILE $OutputRigid $MaskResult


		done



			INPUTIMAGEANTS=$inputImage

			OUTFILE="$(pwd)/newAtlasMaps_run2/${subj_study}_5AtlasTestOutput_${TFMTYPE2}_label_${TFMTYPE}-${INTERPMODE}image.nii"
			DIMENSION=3
			SEARCHRADIUS=3
			VERBOSE=1

			${BINDIR}/antsJointFusion \
				--image-dimensionality "${DIMENSION}" \
				--target-image "${inputImage}" \
				--atlas-image "${atlas_new_im[0]}" \
				--atlas-image "${atlas_new_im[1]}" \
				--atlas-image "${atlas_new_im[2]}" \
				--atlas-image "${atlas_new_im[3]}" \
				--atlas-image "${atlas_new_im[4]}" \
				--atlas-image "${atlas_new_im[5]}" \
				--atlas-image "${atlas_new_im[6]}" \
				--atlas-image "${atlas_new_im[7]}" \
				--atlas-image "${atlas_new_im[8]}" \
				--atlas-image "${atlas_new_im[9]}" \
				--atlas-image "${atlas_new_im[10]}" \
				--atlas-image "${atlas_new_im[11]}" \
				--atlas-image "${atlas_new_im[12]}" \
				--atlas-image "${atlas_new_im[13]}" \
				--atlas-image "${atlas_new_im[14]}" \
				--atlas-image "${atlas_new_im[15]}" \
				--atlas-image "${atlas_new_im[16]}" \
				--atlas-image "${atlas_new_im[17]}" \
				--atlas-segmentation "${ants_atlas_seg[0]}" \
				--atlas-segmentation "${ants_atlas_seg[1]}" \
				--atlas-segmentation "${ants_atlas_seg[2]}" \
				--atlas-segmentation "${ants_atlas_seg[3]}" \
				--atlas-segmentation "${ants_atlas_seg[4]}" \
				--atlas-segmentation "${ants_atlas_seg[5]}" \
				--atlas-segmentation "${ants_atlas_seg[6]}" \
				--atlas-segmentation "${ants_atlas_seg[7]}" \
				--atlas-segmentation "${ants_atlas_seg[8]}" \
				--atlas-segmentation "${ants_atlas_seg[9]}" \
				--atlas-segmentation "${ants_atlas_seg[10]}" \
				--atlas-segmentation "${ants_atlas_seg[11]}" \
				--atlas-segmentation "${ants_atlas_seg[12]}" \
				--atlas-segmentation "${ants_atlas_seg[13]}" \
				--atlas-segmentation "${ants_atlas_seg[14]}" \
				--atlas-segmentation "${ants_atlas_seg[15]}" \
				--atlas-segmentation "${ants_atlas_seg[16]}" \
				--atlas-segmentation "${ants_atlas_seg[17]}" \
				--mask-image "${maskimagesout[0]}" \
				--mask-image "${maskimagesout[1]}" \
				--mask-image "${maskimagesout[2]}" \
				--mask-image "${maskimagesout[3]}" \
				--mask-image "${maskimagesout[4]}" \
				--mask-image "${maskimagesout[5]}" \
				--mask-image "${maskimagesout[6]}" \
				--mask-image "${maskimagesout[7]}" \
				--mask-image "${maskimagesout[8]}" \
				--mask-image "${maskimagesout[9]}" \
				--mask-image "${maskimagesout[10]}" \
				--mask-image "${maskimagesout[11]}" \
				--mask-image "${maskimagesout[12]}" \
				--mask-image "${maskimagesout[13]}" \
				--mask-image "${maskimagesout[14]}" \
				--mask-image "${maskimagesout[15]}" \
				--mask-image "${maskimagesout[16]}" \
				--mask-image "${maskimagesout[17]}" \
				--search-radius "${SEARCHRADIUS}" \
				--verbose "${VERBOSE}" \
				--output "${OUTFILE}"







printf "\n"
printf "\n"
printf "\n"
printf "\n"

end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"
done
