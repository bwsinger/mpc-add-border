import argparse
import os
import errno
import sys
from pathlib import Path
from PIL import Image, ImageDraw
from PIL.Image import Resampling
import time

# ---------------------------------------------------------
# Handle command line arguments
# ---------------------------------------------------------

description = 'Adds a black 1/8 inch bleed edge around a MTG proxy and converts to jpg'

parser = argparse.ArgumentParser(description=description)

# Arguments
parser.add_argument('inputPath', type=str, help='The path to the input directory containing Magic card images.')
parser.add_argument('-o', '--output', type=str, default=None, help='The output directory. Defaults to <currentPath>/output')
parser.add_argument('-r', '--recursive', action='store_true', help='Include all image files in subdirectories of <inputPath>')
parser.add_argument('-s', '--scale', type=float, default=1.0, help='Scale of final image. Percentage as a decimal. 1=same scale as original. Default=1.0')

args = parser.parse_args()
input_dir = getattr(args, 'inputPath').replace('\'', '').replace('"', '')
output_dir = getattr(args, 'output') if getattr(args, 'output') is not None else Path(Path(input_dir).parent, 'output').resolve()
recursive = getattr(args, 'recursive') if os.name != 'nt' else False
scale = getattr(args, 'scale')

# ---------------------------------------------------------
# Get files and paths
# ---------------------------------------------------------

glob_match = '**/*' if recursive else '*'

image_types = {".jpg", ".JPG", ".png", ".PNG"}

if os.name != 'nt':
    flag = not Path(output_dir).is_relative_to(Path(input_dir))

    # Restrict file matches to the desired image formats and exclude the output directory
    files = (p.resolve() for p in Path(input_dir).glob(glob_match) if (flag or not p.resolve().is_relative_to(Path(output_dir))) and p.suffix in image_types)
else:
    # Windows paths are fucky
    files = (p.resolve() for p in Path(str(input_dir)).glob(glob_match) if p.suffix in image_types)

try:
    os.mkdir(output_dir)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

# ---------------------------------------------------------
# Process all images
# ---------------------------------------------------------

files_count = 0
total_process_time = 0

for file in files:
    tic = time.perf_counter()

    with Image.open(file) as im:

        # file.stem is just the name, file.name is the name plus extension
        file_name = file.stem
        
        # Save as jpg
        out_file = Path(output_dir, file_name + '.jpg')

        # print(f'Editing "{out_file.name}"', end='\r')
        print(f'Editing "{out_file.name}"')

        # Black out the rounded corners of the original image

        width, height = im.size

        # Find size of corner triangles
        # '0.08' is a magic number that's roughly the right ratio for a mtg card
        triangle_ratio = 0.08
        triangle_corner_size = round(width*triangle_ratio)

        # Points start top left going clockwise
        draw = ImageDraw.Draw(im)

        # Top left corner
        draw.polygon([
            (0, 0),
            (triangle_corner_size, 0),
            (0, triangle_corner_size)],
            fill=(0, 0, 0),
            # outline=(255,0,0)
        )

        # Top right corner
        draw.polygon([
            (width, 0),
            (width, triangle_corner_size),
            (width-triangle_corner_size, 0)],
            fill=(0, 0, 0),
            # outline=(255,0,0)
        )

        # Bottom right corner
        draw.polygon([
            (width, height),
            (width-triangle_corner_size, height),
            (width, height-triangle_corner_size)],
            fill=(0, 0, 0),
            # outline=(255,0,0)
        )

        # Bottom left corner
        draw.polygon([
            (0, height),
            (0, height-triangle_corner_size),
            (triangle_corner_size, height)],
            fill=(0, 0, 0),
            # outline=(255,0,0)
        )

        # width of final image -> 2.48031 inch
        # height of final image -> 3.46457 inch
        # find what 1/8 inch is in file’s DPI
        pixels_per_eighth_inch = (height / (3.46457 + 0.125)) / 8

        new_size = (round(width + pixels_per_eighth_inch), round(height + pixels_per_eighth_inch))

        print(f'Width: {width}, height: {height}, NewSize: {new_size}')

        # Make a black image the size of the original plus the eighth inch border
        im_with_border = Image.new("RGB", new_size)

        # This is some voodoo. Source: https://stackoverflow.com/questions/11142851/adding-borders-to-an-image-using-python#answer-11143078
        box = tuple((n - o) // 2 for n, o in zip(new_size, im.size))
        im_with_border.paste(im, box)

        # Resize the image
        if scale != 1:
            _, height = im_with_border.size
            im_with_border.thumbnail([sys.maxsize, height * scale], Resampling.LANCZOS)

        im_with_border.save(out_file)

        files_count += 1

        toc = time.perf_counter()
        total_process_time += (toc - tic)
        print(f'Time elapsed: {toc - tic:0.4f}s')

print()
print(f'Total processing time: {total_process_time:0.4f}s')
print(f'Average file processing time: {total_process_time / files_count:0.4f}s')
print()

if files_count == 0:
    print(f'There are no .jpg or .png files in directory: "{input_dir}"')
    exit(1)
else:
    print(f'Process complete. Edited {files_count} images.')
    exit(0)