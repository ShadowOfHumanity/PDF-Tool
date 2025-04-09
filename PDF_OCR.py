import ocrmypdf
import fitz  
from PDF_AI_Question import analyze_pdf
import os
import tempfile
from pathlib import Path

ocr_output_text = None

def ocr_pdf(input_path: str, output_path: str = None):
    global ocr_output_text
    
    # If no output path , create in temp directory
    if output_path is None:
        temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Temp")
        # Create temp directory if it doesn't exist
        os.makedirs(temp_dir, exist_ok=True)
        # Generate output filename from input name with _ocr suffix
        input_filename = os.path.basename(input_path)
        base_name = os.path.splitext(input_filename)[0]
        output_path = os.path.join(temp_dir, f"{base_name}_ocr.pdf")
    
    try:
        # OCR on PDF
        ocrmypdf.ocr(input_path, output_path, deskew=True, force_ocr=True, language='eng')
        print(f"OCR complete: {output_path}")

        # Extract text from OCR-processed PDF
        with fitz.open(output_path) as pdf:
            ocr_output_text = ""
            for page in pdf:
                ocr_output_text += page.get_text()

        print("OCR text extracted and saved.")
        analyze_pdf(ocr_output_text)  
    except Exception as e:
        print(f"Error during OCR: {e}")
