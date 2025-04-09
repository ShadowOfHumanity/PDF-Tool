# PDF AI Tool

A portable PDF tool with OCR, summarization, and question-answering capabilities.

## Making the Application Portable

This application requires Ghostscript for OCR functionality. To make it fully portable:

1. Download Ghostscript from [the official website](https://ghostscript.com/releases/gsdnld.html)
2. Extract the Ghostscript files to a folder named `ghostscript` in the same directory as the application
3. The folder structure should be:
   ```
   /PDF-Tool
     - GUI.py
     - PDF_OCR.py
     - ...other application files...
     - /ghostscript
        - /bin
           - gswin64c.exe (on Windows)
           - gs (on Linux/Mac)
        - /lib
        - ...other ghostscript files...
   ```

## Requirements

- Python 3.6+
- PyQt5
- OCRmyPDF
- PyMuPDF
- Requests

See requirements.txt for a complete list of dependencies.

## Usage

1. Run `python GUI.py` to start the application
2. Use the interface to load and process PDFs
