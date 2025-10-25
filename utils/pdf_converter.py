import os

from pdf2docx import Converter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import pypandoc
from pdf2image import convert_from_path

def pdf_to_word(pdf_path, output_path):
    """Convert PDF to DOCX"""
    cv = Converter(pdf_path)
    cv.convert(output_path)
    cv.close()
    return output_path

def pdf_to_images(pdf_path, output_folder, dpi=300, format='png'):
    """Convert PDF pages to images"""
    images = convert_from_path(pdf_path, dpi=dpi)
    image_paths = []
    for i, image in enumerate(images):
        img_path = os.path.join(output_folder, f'page_{i+1}.{format}')
        image.save(img_path, format.upper())
        image_paths.append(img_path)
    return image_paths
