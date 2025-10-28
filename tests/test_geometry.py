import numpy as np
from app.utils.geometry import order_points

def test_order_points_basic():
    pts = np.array([[100, 300],[300, 300],[300, 100],[100, 100]], dtype="float32")
    rect = order_points(pts)
    assert rect.shape == (4,2)
