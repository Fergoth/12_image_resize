import argparse
from PIL import Image
import sys
import os


def save_image(image, args):
    name, ending = os.path.splitext(args.path_to_image)
    new_image_name = name + "__{}x{}".format(*image.size) + ending
    if args.output:
        if os.path.isdir(args.output):
            os.path.join(args.output,new_image_name)
            image.save(args.output+"__")
        else:
            print('Путь не является папкой')
    else:
        image.save(new_image_name)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('path_to_image', help='Path to converting image')
    parser.add_argument('-ph', '--height', help='New image height', type=int)
    parser.add_argument('-pw', '--width', help='New image width', type=int)
    parser.add_argument('-ps', '--scale',
                        help='Scale for resizing image',
                        type=float)
    parser.add_argument('-out',
                        '--output',
                        help='path where we save rescaling image')
    args = parser.parse_args()
    return args


def get_image(path):
    image = Image.open(path)
    return image


def get_new_width_height(args, image):
    width, height = image.size
    old_proportion = width/height
    if (args.width or args.height) and args.scale:
        return None
    if args.scale:
        new_height = height * args.scale
        new_width = width * args.scale
        return new_width, new_height
    if args.width and args.height:
        new_proportion = args.width/args.height
        if new_proportion != old_proportion:
            print('Пропорции не совпадают с исходными!')
        return args.width, args.height
    if args.height:
        new_height = height * (args.height/height)
        new_width = width * (args.height/height)
        return new_width, new_height
    if args.width:
        new_height = height * (args.width/width)
        new_width = width * (args.width/width)
        return new_width, new_height


if __name__ == '__main__':
    args = get_args()
    try:
        image = get_image(args.path_to_image)
    except IOError:
        sys.exit('Проблемы с загрузкой изображения')
    # size ~(width,height)
    size = get_new_width_height(args, image)
    if size:
        size = tuple(map(int, size))
        new_image = image.resize(size)
        save_image(new_image, args)
    else:
        print("Требуется (Высота и(или) Ширина) или Маштаб")

