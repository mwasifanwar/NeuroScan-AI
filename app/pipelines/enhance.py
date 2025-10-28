import cv2
import numpy as np
from skimage import exposure

def illumination_correction(gray: np.ndarray) -> np.ndarray:
    # Morphological opening to estimate background, then subtract
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (31, 31))
    background = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
    corrected = cv2.normalize(gray - background, None, 0, 255, cv2.NORM_MINMAX)
    return corrected

def unsharp_mask(gray: np.ndarray, k: float = 1.5) -> np.ndarray:
    blur = cv2.GaussianBlur(gray, (0, 0), 3)
    sharp = cv2.addWeighted(gray, 1 + k, blur, -k, 0)
    return sharp

def adaptive_binarize(gray: np.ndarray) -> np.ndarray:
    # CLAHE + adaptive threshold
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    eq = clahe.apply(gray)
    th = cv2.adaptiveThreshold(eq, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY, 35, 15)
    return th

def enhance_for_ocr(rgb: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    gray = illumination_correction(gray)
    gray = unsharp_mask(gray, 1.2)
    bw = adaptive_binarize(gray)
    return cv2.cvtColor(bw, cv2.COLOR_GRAY2RGB)
