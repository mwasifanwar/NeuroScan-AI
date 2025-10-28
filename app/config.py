import os

class Settings:
    TESSERACT_CMD: str | None = os.getenv("TESSERACT_CMD")
    OCR_LANG: str = os.getenv("OCR_LANG", "eng")
    OCR_OEM: int = int(os.getenv("OCR_OEM", "3"))  # 0..3
    OCR_PSM: int = int(os.getenv("OCR_PSM", "6"))  # 0..13

settings = Settings()
