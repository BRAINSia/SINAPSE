
# coding: utf-8

# In[88]:


import os
import SimpleITK as sitk
import matplotlib.pyplot as plt
import glob


# In[103]:

PUTAMEN_ID = 12
file_end = "lr_combined_dense_seg.nii.gz"


def get_putamen_image(file_path, index=0, size=0):
    im = sitk.ReadImage(file_path)
    putamen = (im==PUTAMEN_ID)*255
    putamen_array = sitk.GetArrayFromImage(putamen)    
    lssf = sitk.LabelShapeStatisticsImageFilter()
    lssf.Execute(putamen)
    [x_min, y_min, z_min, x_size, y_size, z_size] = lssf.GetBoundingBox(255)
    putamen_array = sitk.GetArrayFromImage(putamen)
    middle_of_putamen = (z_min+int(z_size/2))
#     plt.imshow(putamen_array[:, middle_of_putamen, :], cmap='gray')
    putamen_png_name = file_path.replace(file_end, "lr_combined_putamen_dense_seg.png")
    if size is 0:
        print("Saving to " + putamen_png_name)
    else:
        print("Saving [{0} of {1}] to {2}".format(index, size, putamen_png_name))
    plt.axis('off')
    plt.imsave(fname=putamen_png_name, cmap='gray', arr=putamen_array[:, middle_of_putamen, :])
#     plt.savefig(putamen_png_name)


if __name__ == "__main__":
    path = "/Shared/johnsonhj/2018Projects/20181002_LesionMappingBAW/20181017_niftinet_data_inputs/images/"
    file_list = os.listdir(path)
    filtered_file_list = glob.glob(path + "*" + file_end)
    list_length = filtered_file_list.__len__()
    for index, file_path in enumerate(filtered_file_list):
        print(file_path)
        get_putamen_image(file_path, index=index, size=list_length)

