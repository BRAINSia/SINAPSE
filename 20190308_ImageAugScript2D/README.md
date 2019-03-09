# Python 2D Image Augmentation Program
> [Alex Powers](mailto:alexander-powers@uiowa.edu?subject=[GitHub]%20SINAPSE%20PythonImageAug2D)

## Setup
Create a conda env:
```bash
conda env create -f environment.yml
```
or install the required libraries directly
```bash
pip install -r requirements.txt
```

## Program Execution
```text
./augment_images.sh <full-path-to-directory-of-images> \ 
<full-path-to-output-directory> <is-label ? 1 : 0> \ 
<full-path-to-augmentation.json> <optional-glob>
```

## Augmentation Parameters
flip_LR: `1` to flip left/right, `0` to skip   
flip_UD: `1` to flip up/down, `0` to skip   
rotate: `1` to rotate, `0` to skip   
deg_of_rotation: `[-m, n]` where `m` and `n` are both positive integers   
```json
{
    "flip_LR": 1,
    "flip_UD": 0,
    "rotate": 1,
    "deg_of_rotation": [-20, 20]
}
```