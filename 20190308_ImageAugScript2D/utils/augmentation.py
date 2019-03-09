from numpy import identity, array, pi
from SimpleITK import Image, Resample, FlipImageFilter, AffineTransform, sitkNearestNeighbor, sitkLinear


def insert_suffix(file_name: str, suffix: str) -> str:
    name = intersperse(file_name.split('.'), '.')
    return "{name}_{suffix}{ext}".format(name=name[0], suffix=suffix, ext=''.join(name[1:]))


def intersperse(seq, value):
    res = [value] * (2 * len(seq) - 1)
    res[::2] = seq
    return res


def augment_data(image: Image, fname: str, settings: dict, is_label: bool) -> dict:
    flip = FlipImageFilter()

    images = {fname: image}
    if bool(settings["flip_LR"]):
        axis = (True, False)
        flip.SetFlipAxes(axis)

        tmp = {}
        for k, v in images.items():
            temp_image = flip.Execute(v)
            tmp[insert_suffix(k, "LR")] = temp_image

        for k, v in tmp.items():
            images[k] = v

    if bool(settings["flip_UD"]):
        axis = (False, True)
        flip.SetFlipAxes(axis)

        tmp = {}
        for k, v in images.items():
            temp_image = flip.Execute(v)
            tmp[insert_suffix(k, "UD")] = temp_image

        for k, v in tmp.items():
            images[k] = v

    if bool(settings["rotate"]):
        tmp = {}
        for k, v in images.items():
            for deg in range(int(settings["deg_of_rotation"][0]), int(settings["deg_of_rotation"][1]) + 1):
                if deg != 0:
                    r_im, deg = rotate(image=v, degrees=int(deg), is_label=is_label)
                    tmp[insert_suffix(k, "R%03d" % deg)] = r_im

        for k, v in tmp.items():
            images[k] = v

    return images


def rotate(image: Image, degrees=10.0, is_label=False):
    if degrees < 0:
        degrees = 360 - abs(degrees)
    get_dimension = image.GetDimension()
    dimension1 = get_dimension
    dimension = dimension1
    transform = AffineTransform(dimension)
    radians = pi * degrees / 180
    transform.Rotate(axis1=1, axis2=0, angle=radians)
    if is_label:
        interpolator = sitkNearestNeighbor
    else:
        interpolator = sitkLinear
    return __resample(image=image, transform=transform, interpolator=interpolator), degrees


def __resample(image, transform, interpolator):
    # Output image Origin, Spacing, Size, Direction are taken from the reference
    # image in this call to Resample
    transform.SetCenter(
        image.TransformContinuousIndexToPhysicalPoint(array(image.GetSize()) / 2)
    )

    output_direction = identity(2).flatten()
    extreme_pts = [
        image.TransformContinuousIndexToPhysicalPoint((0, 0)),
        image.TransformContinuousIndexToPhysicalPoint((image.GetWidth(), 0)),
        image.TransformContinuousIndexToPhysicalPoint(
            (image.GetWidth(), image.GetHeight())
        ),
        image.TransformContinuousIndexToPhysicalPoint((0, image.GetHeight())),
    ]

    inv = transform.GetInverse()
    transformed_extreme_pts = [inv.TransformPoint(pt) for pt in extreme_pts]
    min_x = min(transformed_extreme_pts)[0]
    min_y = min(transformed_extreme_pts, key=lambda p: p[1])[1]
    max_x = max(transformed_extreme_pts)[0]
    max_y = max(transformed_extreme_pts, key=lambda p: p[1])[1]

    # Use the original spacing (arbitrary decision).
    output_spacing = image.GetSpacing()
    # origin of the output image
    output_origin = [min_x, min_y]
    # Compute grid size based on the physical size and spacing.
    output_size = [
        int((max_x - min_x) / output_spacing[0]),
        int((max_y - min_y) / output_spacing[1]),
    ]
    output_image = Image(output_size, image.GetPixelIDValue())
    output_image.SetOrigin(output_origin)
    output_image.SetDirection(output_direction)
    output_image.SetSpacing(output_spacing)

    return Resample(image, output_image, transform, interpolator)
