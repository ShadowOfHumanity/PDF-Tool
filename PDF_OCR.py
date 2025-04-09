import ocrmypdf
import fitz  
from PDF_AI_Question import analyze_pdf
import os
import tempfile
from pathlib import Path
import shutil
import platform
import subprocess

ocr_output_text = None

def find_ghostscript():
    
    #  check for bundled ghostscript in a 'gs' directory next to application
    script_dir = os.path.dirname(os.path.abspath(__file__))
    bundled_gs_dir = os.path.join(script_dir, "ghostscript")
    
    # Check if bundled ghostscript exist
    if os.path.exists(bundled_gs_dir):
        if platform.system() == "Windows":
            gs_exe = os.path.join(bundled_gs_dir, "bin", "gswin64c.exe")
            if os.path.exists(gs_exe):
                return gs_exe
        else:  # Linux/Mac
            gs_exe = os.path.join(bundled_gs_dir, "bin", "gs")
            if os.path.exists(gs_exe):
                return gs_exe
    
    # If no bundled look in common installation directories on Windows
    if platform.system() == "Windows":
        common_paths = [
            r"C:\Program Files\gs\gs*\bin\gswin64c.exe",
            r"C:\Program Files (x86)\gs\gs*\bin\gswin32c.exe"
        ]
        
        for pattern in common_paths:
            import glob
            matches = sorted(glob.glob(pattern), reverse=True)
            if matches:
                return matches[0]
    
    return None

def ocr_pdf(input_path: str, output_path: str = None):
    global ocr_output_text
    
    # If no output path create in temp directory
    if output_path is None:
        temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Temp")
        # Create temp directory if it NO exist
        os.makedirs(temp_dir, exist_ok=True)
       
        input_filename = os.path.basename(input_path)
        base_name = os.path.splitext(input_filename)[0]
        output_path = os.path.join(temp_dir, f"{base_name}_ocr.pdf")
    
    try:
        # fdind ghostscript executable
        gs_path = find_ghostscript()
        
        if not gs_path:
            raise RuntimeError(
                "Ghostscript not found. Please install ghostscript or place it in a 'ghostscript' "
                "folder next to this application. Visit https://ghostscript.com/releases/gsdnld.html "
                "to download."
            )
        
        # Create minimal env with only needed variables
        minimal_env = {
            'PATH': os.path.dirname(gs_path) + os.pathsep + os.environ.get('PATH', ''),
            'SYSTEMROOT': os.environ.get('SYSTEMROOT', '')
        }
        
        # For Windows, add somevariables
        if platform.system() == "Windows":
            minimal_env['TEMP'] = os.environ.get('TEMP', '')
            minimal_env['TMP'] = os.environ.get('TMP', '')
        
        # Run OCR directly with subprocess instead of using ocrmypdf.ocr
        cmd = [
            'ocrmypdf',
            '--deskew',
            '--force-ocr',
            '--language', 'eng',
            input_path,
            output_path
        ]
        
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, env=minimal_env)
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
        raise
