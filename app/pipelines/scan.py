import cv2
import numpy as np
from typing import Tuple
from app.utils.geometry import four_point_transform, auto_deskew
from app.pipelines.enhance import enhance_for_ocr

def find_document_contour(edged: np.ndarray) -> np.ndarray | None:
    contours, _ = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            return approx.reshape(4, 2)
    return None

def preprocess_for_edges(gray: np.ndarray) -> np.ndarray:
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    edged = cv2.Canny(blur, 50, 150)
    edged = cv2.dilate(edged, np.ones((3,3), np.uint8), iterations=1)
    edged = cv2.erode(edged, np.ones((3,3), np.uint8), iterations=1)
    return edged

def scan_document(rgb: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    edged = preprocess_for_edges(gray)

    quad = find_document_contour(edged)
    if quad is not None:
        warped = four_point_transform(cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR), quad)
        warped_rgb = cv2.cvtColor(warped, cv2.COLOR_BGR2RGB)
    else:
        
        warped_rgb = rgb.copy()

    gray_w = cv2.cvtColor(warped_rgb, cv2.COLOR_RGB2GRAY)
    deskewed_gray, _ = auto_deskew(gray_w)
    deskewed_rgb = cv2.cvtColor(deskewed_gray, cv2.COLOR_GRAY2RGB)

    enhanced_rgb = enhance_for_ocr(deskewed_rgb)
    return warped_rgb, enhanced_rgb
