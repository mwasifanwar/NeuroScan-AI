import numpy as np
from app.pipelines.scan import scan_document

def test_scan_document_identity():
    rgb = np.zeros((200, 200, 3), dtype=np.uint8)
    warped, enhanced = scan_document(rgb)
    assert warped.shape == rgb.shape
    assert enhanced.shape == rgb.shape
