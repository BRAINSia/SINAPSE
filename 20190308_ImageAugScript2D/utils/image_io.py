from os.path import join
from SimpleITK import Image, ImageFileReader, ImageFileWriter


def read_im(full_file_name: str) -> Image:
    reader = ImageFileReader()
    reader.SetFileName(full_file_name)
    return reader.Execute()


# assumes dictionary is {file_name_str -> sitk.Image}
def write_dir(base_dir: str, images: dict) -> None:
    writer = ImageFileWriter()
    writer.SetUseCompression(True)
    for file_name, image in images.items():
        writer.SetFileName(join(base_dir, file_name))
        writer.Execute(image)


def write_im(full_file_name: str, image: Image) -> None:
    writer = ImageFileWriter()
    writer.SetUseCompression(True)
    writer.SetFileName(full_file_name)
    writer.Execute(image)
