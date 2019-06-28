#!/bin/bash

MLMKFILE="/Shared/johnsonhj/2018Projects/20180514_MiniPig_BIDS/fcsv_Im_Pairs/sub-Ada165/ses-20130321/anat/sub-Ada165_ses-20130321_run-094402_T1w_markup.fcsv"
FLMKFILE="/Shared/johnsonhj/2018Projects/20180514_MiniPig_BIDS/fcsv_Im_Pairs/non-zipped_ATLASIMS/M135P100_20131202_3DT1TFEhrs_strip_markup.fcsv"
WTSFILE="$(pwd)/mplmk.wts"

BINDIR=/Users/johnsonhj/src/BT-11/bin

TFMTYPE=AffineTransform

M2F_TFM="$(pwd)/pippa2grace_${TFMTYPE}.h5"

INTERPMODE=Linear
if [[ ${TFMTYPE} ==  "VersorRigid3DTransform" ]]; then
  INTERPMODE=ResampleInPlace
fi

${BINDIR}/BRAINSLandmarkInitializer \
   --inputMovingLandmarkFilename "${MLMKFILE}" \
   --inputFixedLandmarkFilename "${FLMKFILE}" \
   --inputWeightFilename "${WTSFILE}" \
   --outputTransformType ${TFMTYPE} \
   --outputTransformFilename "${M2F_TFM}"

MIMGFILE="/Shared/johnsonhj/2018Projects/20180514_MiniPig_BIDS/fcsv_Im_Pairs/sub-Ada165/ses-20130321/anat/sub-Ada165_ses-20130321_run-094402_T1w.nii"
FIMGFILE="/Shared/johnsonhj/2018Projects/20180514_MiniPig_BIDS/fcsv_Im_Pairs/non-zipped_ATLASIMS/M135P100_20131202_3DT1TFEhrs_strip.nii"
PIXELTYPE=float

OUTFILE="$(pwd)/warped_${TFMTYPE}_${PIXELTYPE}_${INTERPMODE}_Ada165_2_Lucrezia135.nii"


${BINDIR}/BRAINSResample \
   --interpolationMode ${INTERPMODE} \
   --warpTransform "${M2F_TFM}" \
   --pixelType "${PIXELTYPE}" \
   --outputVolume "${OUTFILE}" \
   --inputVolume "${MIMGFILE}" \
   --referenceVolume "${FIMGFILE}"

echo lsl "${OUTFILE}"  "${FIMGFILE}"
