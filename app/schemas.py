from pydantic import BaseModel

class ScanOptions(BaseModel):
    ocr: bool = True
    lang: str | None = None
    oem: int | None = None
    psm: int | None = None
