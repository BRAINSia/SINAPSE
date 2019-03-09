from SimpleITK import Image, VectorIndexSelectionCast, sitkUInt16, Cast

PIXEL_TYPE = sitkUInt16


def condense_label_map(image: Image) -> Image:
    tmp = image[:, :, 0]
    tmp = tmp > 0
    tmp = Cast(tmp, PIXEL_TYPE)
    return tmp


def select_image_channel(image: Image, channel: int) -> Image:
    return Cast(VectorIndexSelectionCast(image, index=channel), PIXEL_TYPE)
