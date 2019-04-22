# Image Resizer
Resize image to new sizes.
# Description
You can give new height or new width of image (or both, or scale) that will be rescaled to new width and height
You also can give path to where you want to save new rescaled image (as default such path as path to rescaling image)
New image save as "[pic_name]__[new_width]x[new_height].jpg"
# Example
```bash
C:/12_image_resize/image_resize.py default.jpg -h
usage: image_resize.py [-h] [-ph HEIGHT] [-pw WIDTH] [-ps SCALE] [-out OUTPUT]
                       path_to_image

positional arguments:
  path_to_image         Path to converting image

optional arguments:
  -h, --help            show this help message and exit
  -ph HEIGHT, --height HEIGHT
                        New image height
  -pw WIDTH, --width WIDTH
                        New image width
  -ps SCALE, --scale SCALE
                        Scale for resizing image
  -out OUTPUT, --output OUTPUT
                        path where we save rescaling image
```
# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
