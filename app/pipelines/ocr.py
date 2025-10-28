import pytesseract
from PIL import Image
import cv2
import numpy as np
from app.config import settings

# Configure Tesseract path if provided
if settings.TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD

def _rgb_to_pil(rgb: np.ndarray) -> Image.Image:
    return Image.fromarray(rgb)

def extract_text(
    rgb_image: np.ndarray,
    lang: str | None = None,
    oem: int | None = None,
    psm: int | None = None,
) -> str:
    lang = lang or settings.OCR_LANG
    oem = settings.OCR_OEM if oem is None else oem
    psm = settings.OCR_PSM if psm is None else psm
    config = f"--oem {oem} --psm {psm}"
    pil = _rgb_to_pil(rgb_image)
    text = pytesseract.image_to_string(pil, lang=lang, config=config)
    return text

def to_searchable_pdf_bytes(
    rgb_image: np.ndarray,
    lang: str | None = None,
    oem: int | None = None,
    psm: int | None = None,
) -> bytes:
    lang = lang or settings.OCR_LANG
    oem = settings.OCR_OEM if oem is None else oem
    psm = settings.OCR_PSM if psm is None else psm
    config = f"--oem {oem} --psm {psm}"
    pil = _rgb_to_pil(rgb_image)
    pdf_bytes = pytesseract.image_to_pdf_or_hocr(pil, extension='pdf', lang=lang, config=config)
    return pdf_bytes
