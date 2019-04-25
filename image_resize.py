import argparse
from PIL import Image
import sys
import os



def generate_output_path(path_to_image,output_path,image):
    name, ending = os.path.splitext(path_to_image)
    new_image_name = '{}__{}x{}{}'.format(name, *image.size, ending)
    if output_path:
        os.path.join(output_path, new_image_name)
        return output_path
    else:
        os.path.join(path_to_image,new_image_name)
        return path_to_image


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('path_to_image', help='Path to converting image')
    parser.add_argument('-ph', '--height', help='New image height', type=int)
    parser.add_argument('-pw', '--width', help='New image width', type=int)
    parser.add_argument(
        '-ps', '--scale',
        help='Scale for resizing image',
        type=float
    )
    parser.add_argument(
        '-out',
        '--output',
        help='Path to directory where we save rescaling image'
    )
    args = parser.parse_args()
    return args


def get_image(path):
    image = Image.open(path)
    return image


def scale_new_sizes(width, height, scale):
    return int(width * scale), int(height * scale)


def is_equal_proportion(new_proportion, old_proportion, e = 0.001):
    return new_proportion - old_proportion < e


def get_new_width_height(width, height, scale, image):
    old_width, old_height = image.size
    if scale:
        return scale_new_sizes(old_width, old_height, scale)
    if width and height:
        return width, height
    if height:
        return scale_new_sizes(old_width, old_height, height / old_height)
    if width:
        return scale_new_sizes(old_width, old_height, width / old_width)


def validate_args(width, height, scale, output_dir):
    if (width or height) and scale:
        raise argparse.ArgumentTypeError('Требуется (Высота и(или) Ширина) или Маштаб')
    if output_dir and not output_dir.isdir(output_dir):
        raise argparse.ArgumentTypeError('Неправильный путь к директории')
    if not any((width, height, scale)):
        raise argparse.ArgumentTypeError('Не указаны аргументы для изменения размера')
    if ((width and width <= 0)
        or (height and height <= 0)
        or (scale and scale <= 0)
    ):
        raise argparse.ArgumentTypeError('Размеры должны быть не отрицательными')



if __name__ == '__main__':
    args = get_args()

    width = args.width
    height = args.height
    scale = args.scale
    path_to_image = args.path_to_image
    output_dir = args.output
    try:
        validate_args(width, height, scale, output_dir)
    except argparse.ArgumentTypeError as e:
        sys.exit(e)
    try:
        image = get_image(path_to_image)
    except IOError:
        sys.exit('Проблемы с загрузкой изображения')

    new_width, new_height = get_new_width_height(width, height, scale, image)
    old_width, old_height = image.size

    new_proportion = new_width / new_height
    old_proportion = old_width / old_height

    if not is_equal_proportion(new_proportion,old_proportion):
        print('Пропорции не совпадают с исходными!')

    new_image = image.resize(new_width, new_height)
    output_path = generate_output_path(path_to_image, output_dir, image)
    image.save(output_path)

