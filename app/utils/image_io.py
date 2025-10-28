import cv2
import numpy as np
from typing import Tuple

def imread_rgb(path: str) -> np.ndarray:
    bgr = cv2.imread(path, cv2.IMREAD_COLOR)
    if bgr is None:
        raise ValueError(f"Unable to read image: {path}")
    return cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

def imdecode_image(file_bytes: bytes) -> np.ndarray:
    arr = np.frombuffer(file_bytes, dtype=np.uint8)
    bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if bgr is None:
        raise ValueError("Unable to decode uploaded image.")
    return cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

def to_bgr(img: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

def to_gray(img_rgb: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

def encode_png(img_rgb: np.ndarray) -> Tuple[bytes, str]:
    bgr = to_bgr(img_rgb)
    ok, buf = cv2.imencode(".png", bgr)
    if not ok:
        raise RuntimeError("PNG encode failed")
    return buf.tobytes(), "image/png"
