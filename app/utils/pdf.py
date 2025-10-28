from pdf2image import convert_from_bytes, convert_from_path
from typing import List
import numpy as np

def pdf_bytes_to_images(pdf_bytes: bytes, dpi: int = 300) -> List[np.ndarray]:
    pil_pages = convert_from_bytes(pdf_bytes, dpi=dpi)
    return [np.array(p) for p in pil_pages]

def pdf_path_to_images(pdf_path: str, dpi: int = 300) -> List[np.ndarray]:
    pil_pages = convert_from_path(pdf_path, dpi=dpi)
    return [np.array(p) for p in pil_pages]
