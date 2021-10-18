from PIL import Image, ImageOps
import pytesseract
from pdf2image import convert_from_path


def ocr_image(filename):
    """
    This function will handle the core OCR processing of images.
    """
    pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
    text = pytesseract.image_to_string(Image.open(filename), lang='eng')
    return text

def cut_image(image_name, x1, x2, y1, y2, new_image_name, basewidth=174):
    imageObject = Image.open(image_name).convert('RGB')
    cropped = imageObject.crop((x1,x2,y1,y2))
    imageObject.close()
    cropped = ImageOps.invert(cropped)
    wpercent = (basewidth / float(cropped.size[0]))
    hsize = int((float(cropped.size[1]) * float(wpercent)))
    cropped = cropped.resize((basewidth, hsize), Image.ANTIALIAS)
    cropped.save(new_image_name, quality=90)

def convert_pdf_to_image(pdf_filename, image_filename):
    pages = convert_from_path(pdf_filename, 500, poppler_path=r'.\utils\poppler-0.68.0\bin')
    for page in pages:
        page.save(image_filename+'.jpg', 'JPEG')
