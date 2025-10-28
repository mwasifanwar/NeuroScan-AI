from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse, StreamingResponse
import numpy as np
import cv2

from app.utils.image_io import imdecode_image, encode_png
from app.utils.pdf import pdf_bytes_to_images
from app.pipelines.scan import scan_document
from app.pipelines.ocr import extract_text, to_searchable_pdf_bytes

app = FastAPI(title="Wasif DocScanner API", version="1.0.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/scan")
async def scan(
    file: UploadFile = File(...),
    ocr: bool = Form(True),
    lang: str | None = Form(None),
    oem: int | None = Form(None),
    psm: int | None = Form(None),
):
    data = await file.read()

    images_rgb = []
    if file.filename.lower().endswith(".pdf"):
        images_rgb = pdf_bytes_to_images(data)  
    else:
        images_rgb = [imdecode_image(data)]

    pages_out = []
    full_text = []

    for rgb in images_rgb:
        warped_rgb, enhanced_rgb = scan_document(rgb)
        text = extract_text(enhanced_rgb, lang=lang, oem=oem, psm=psm) if ocr else ""
        png_bytes, _ = encode_png(enhanced_rgb)
        pages_out.append(png_bytes)
        if text:
            full_text.append(text)

    return JSONResponse({
        "pages": [len(p) for p in pages_out],  
        "text": "\n\n".join(full_text) if full_text else ""
    })

@app.post("/scan/pdf")
async def scan_to_pdf(
    file: UploadFile = File(...),
    lang: str | None = Form(None),
    oem: int | None = Form(None),
    psm: int | None = Form(None),
):
    data = await file.read()

    pdf_parts = []
    if file.filename.lower().endswith(".pdf"):
        images_rgb = pdf_bytes_to_images(data)
    else:
        images_rgb = [imdecode_image(data)]

    for rgb in images_rgb:
        _, enhanced_rgb = scan_document(rgb)
        pdf_parts.append(to_searchable_pdf_bytes(enhanced_rgb, lang=lang, oem=oem, psm=psm))

    merged = b"".join(pdf_parts)

    return StreamingResponse(iter([merged]),
                             media_type="application/pdf",
                             headers={"Content-Disposition": "attachment; filename=scan_searchable.pdf"})
