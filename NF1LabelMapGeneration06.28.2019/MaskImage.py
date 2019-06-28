import SimpleITK as sitk
import sys
import numpy

imagefilename = sys.argv[1]
labelmapfilename = sys.argv[2]
outputfilename = sys.argv[3]


imagereader = sitk.ImageFileReader()
imagereader.SetFileName(imagefilename)
image = imagereader.Execute()

labelreader = sitk.ImageFileReader()
labelreader.SetFileName(labelmapfilename)
label = labelreader.Execute()

imageArray = sitk.GetArrayFromImage(image)
labelArray = sitk.GetArrayFromImage(label)

sitk.LabelMapMaskImageFilter()

imagesize = image.GetSize()

print(imagesize[0])
print(imagesize[1])
print(imagesize[2])

xindex = imagesize[0]
yindex = imagesize[1]
zindex = imagesize[2]

for i in range(xindex):
    for j in range(yindex):
        for k in range(zindex):
            currentImageVal = image.GetPixel(i, j, k)
            currentLabelVal = label.GetPixel(i, j, k)

            if currentLabelVal != 0:
                image.SetPixel(i, j, k, 1)

            if currentLabelVal == 0:
                image.SetPixel(i, j, k, 0)


writer = sitk.ImageFileWriter()
writer.SetFileName(outputfilename)
writer.Execute(image)
