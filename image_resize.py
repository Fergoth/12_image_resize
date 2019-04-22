import argparse
from PIL import Image
import sys
import os


def save_image(image, args):
    name, ending = os.path.splitext(args.path_to_image)
    new_image_name = name + "__{}x{}".format(*image.size) + ending
    if args.output:
        if os.path.isdir(args.output):
            os.path.join(args.output, new_image_name)
            image.save(args.output + "__")
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


def scale_new_sizes(width, height, scale):
    return width * scale, height * scale


def print_warning(new_proportion, old_proportion):
    if new_proportion != old_proportion:
        print('Пропорции не совпадают с исходными!')


def get_new_width_height(args, image):
    width, height = image.size
    old_proportion = width / height
    if (args.width or args.height) and args.scale:
        return None
    if args.scale:
        return scale_new_sizes(width, height, args.scale)
    if args.width and args.height:
        new_proportion = args.width / args.height
        print_warning(new_proportion, old_proportion)
        return args.width, args.height
    if args.height:
        return scale_new_sizes(width, height, args.height / height)
    if args.width:
        return scale_new_sizes(width, height, args.width / width)


if __name__ == '__main__':
    args = get_args()
    try:
        image = get_image(args.path_to_image)
    except IOError:
        sys.exit('Проблемы с загрузкой изображения')
    size = get_new_width_height(args, image)
    if size:
        size = tuple(map(int, size))
        new_image = image.resize(size)
        save_image(new_image, args)
    else:
        print("Требуется (Высота и(или) Ширина) или Маштаб")
