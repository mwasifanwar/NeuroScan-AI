import streamlit as st
import numpy as np
import io
import base64

from app.utils.pdf import pdf_bytes_to_images
from app.utils.image_io import imdecode_image
from app.pipelines.scan import scan_document
from app.pipelines.ocr import extract_text, to_searchable_pdf_bytes

st.set_page_config(page_title="Wasif DocScanner", layout="wide")

st.title("📄 Wasif DocScanner — Scan, Enhance & OCR")

with st.sidebar:
    st.header("OCR Settings")
    ocr_on = st.toggle("Run OCR", value=True)
    lang = st.text_input("Tesseract languages (e.g. eng, eng+deu)", value="eng")
    oem = st.number_input("OEM (0..3)", value=3, min_value=0, max_value=3)
    psm = st.number_input("PSM (0..13)", value=6, min_value=0, max_value=13)

uploaded = st.file_uploader(
    "Upload an image or PDF",
    type=["png", "jpg", "jpeg", "tif", "tiff", "pdf"],
    accept_multiple_files=False
)

col1, col2 = st.columns(2)

if uploaded:
    data = uploaded.read()
    pages = []
    if uploaded.name.lower().endswith(".pdf"):
        pages = pdf_bytes_to_images(data)
    else:
        pages = [imdecode_image(data)]

    all_text = []
    scanned_pngs = []

    for idx, rgb in enumerate(pages, 1):
        with st.spinner(f"Processing page {idx} ..."):
            warped_rgb, enhanced_rgb = scan_document(rgb)
            col1.image(rgb, caption=f"Original Page {idx}", use_container_width=True)
            col2.image(enhanced_rgb, caption=f"Scanned Page {idx}", use_container_width=True)
            if ocr_on:
                text = extract_text(enhanced_rgb, lang=lang, oem=int(oem), psm=int(psm))
                all_text.append(f"## Page {idx}\n\n{text}")

      
            import cv2
            bgr = cv2.cvtColor(enhanced_rgb, cv2.COLOR_RGB2BGR)
            ok, buf = cv2.imencode(".png", bgr)
            if ok:
                scanned_pngs.append(buf.tobytes())

 
    if ocr_on and all_text:
        st.markdown("---")
        st.subheader("📝 Extracted Text")
        st.markdown("\n\n".join(all_text))

  
    if pages:
        with st.spinner("Generating searchable PDF ..."):
            pdf_parts = []
            for idx, rgb in enumerate(pages, 1):
                _, enhanced_rgb = scan_document(rgb)
                pdf_parts.append(to_searchable_pdf_bytes(enhanced_rgb, lang=lang, oem=int(oem), psm=int(psm)))
            merged = b"".join(pdf_parts)
        st.download_button(
            "⬇️ Download Searchable PDF",
            data=merged,
            file_name="scan_searchable.pdf",
            mime="application/pdf"
        )

       
        if scanned_pngs:
            import zipfile, time
            from io import BytesIO
            zbuf = BytesIO()
            with zipfile.ZipFile(zbuf, "w", zipfile.ZIP_DEFLATED) as zf:
                for i, b in enumerate(scanned_pngs, 1):
                    zf.writestr(f"page_{i:02d}.png", b)
            zbuf.seek(0)
            st.download_button("⬇️ Download Scanned PNGs (ZIP)", data=zbuf, file_name="scanned_pages.zip", mime="application/zip")
