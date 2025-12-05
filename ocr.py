# ocr.py
from PIL import Image
import pytesseract
# If tesseract is not in PATH on Windows, set tesseract_cmd, e.g.:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image_path_or_pil):
    """Accepts a PIL image object or a file path. Returns extracted text."""
    if isinstance(image_path_or_pil, str):
        img = Image.open(image_path_or_pil)
    else:
        img = image_path_or_pil
    # Convert to grayscale to improve OCR
    img = img.convert('L')
    text = pytesseract.image_to_string(img, lang='eng')
    return text