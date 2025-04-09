import ocrmypdf

def ocr_pdf(input_path: str, output_path: str):
    try:
        ocrmypdf.ocr(input_path, output_path, deskew=True, force_ocr=True, language='eng')
        print(f"OCR complete: {output_path}")
    except Exception as e:
        print(f"Error during OCR: {e}")
