from PIL import Image
import cairosvg
import pillow_heif
from io import BytesIO


def convert_image(input_path, output_path, output_format, quality=95):
    """Universal image converter"""
    # Handle HEIC
    if input_path.lower().endswith('.heic'):
        heif_file = pillow_heif.read_heif(input_path)
        image = Image.frombytes(
            heif_file.mode, heif_file.size, heif_file.data,
            "raw", heif_file.mode, heif_file.stride
        )
    # Handle SVG
    elif input_path.lower().endswith('.svg'):
        png_data = cairosvg.svg2png(url=input_path)
        image = Image.open(BytesIO(png_data))
    else:
        image = Image.open(input_path)

    # Convert RGBA to RGB for JPEG
    if output_format.lower() in ['jpg', 'jpeg'] and image.mode == 'RGBA':
        rgb_image = Image.new('RGB', image.size, (255, 255, 255))
        rgb_image.paste(image, mask=image.split()[3])
        image = rgb_image

    # Save
    save_kwargs = {'quality': quality} if output_format.lower() in ['jpg', 'jpeg', 'webp'] else {}
    image.save(output_path, format=output_format.upper(), **save_kwargs)
    return output_path


def resize_image(input_path, output_path, width=None, height=None, maintain_aspect=True):
    """Resize image"""
    image = Image.open(input_path)

    if maintain_aspect and (width or height):
        image.thumbnail((width or image.width, height or image.height))
    elif width and height:
        image = image.resize((width, height))

    image.save(output_path)
    return output_path
