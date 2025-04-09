import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                            QHBoxLayout, QWidget, QFileDialog, QLabel, QSplitter,
                            QFrame, QTextEdit, QScrollArea)
from PyQt5.QtGui import QPixmap, QImage, QFont, QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWebEngineWidgets import QWebEngineView
import fitz  # PyMuPDF
from PDF_OCR import ocr_pdf  
from PDF_AI_Summarise import generate_pdf_summary
from PDF_AI_Question import generate_pdf_question

class PDFToolGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.pdf_path = None
        self.current_page = 0
        self.total_pages = 0
        self.initUI()
        
    def initUI(self):
        # Set window properties
        self.setWindowTitle("PDF AI Assistant Tool")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #f0f0f0;")
        
        # Main layout
        main_layout = QHBoxLayout()
        
        # Left sidebar for buttons
        left_panel = QWidget()
        left_panel.setStyleSheet("background-color: #2c3e50;")
        left_panel.setFixedWidth(200)
        
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(10, 20, 10, 20)
        left_layout.setSpacing(15)
        
        # App title
        title_label = QLabel("PDF AI TOOLKIT")
        title_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(title_label)
        
        left_layout.addSpacing(20)
        
        # File select button
        self.select_file_btn = self.create_button("Select PDF", self.select_pdf)
        left_layout.addWidget(self.select_file_btn)
        
        left_layout.addSpacing(30)
        
        # Function buttons
        self.ocr_btn = self.create_button("OCR PDF", self.ocr_pdf_function)
        left_layout.addWidget(self.ocr_btn)
        
        self.summarize_btn = self.create_button("Summarize PDF", self.summarize_pdf_function)
        left_layout.addWidget(self.summarize_btn)
        
        self.ask_btn = self.create_button("Ask Question", self.ask_question_function)
        left_layout.addWidget(self.ask_btn)
        
        left_layout.addStretch()
        
        # Center panel for PDF viewing
        self.center_panel = QWidget()
        center_layout = QVBoxLayout(self.center_panel)
        
        # PDF viewer
        self.pdf_view = QScrollArea()
        self.pdf_view.setWidgetResizable(True)
        self.pdf_view.setStyleSheet("background-color: white; border: 1px solid #cccccc;")
        
        self.pdf_content = QLabel("Select a PDF to view")
        self.pdf_content.setAlignment(Qt.AlignCenter)
        self.pdf_content.setStyleSheet("font-size: 16px; color: #555;")
        
        self.pdf_view.setWidget(self.pdf_content)
        
        # Nav controls
        nav_layout = QHBoxLayout()
        self.prev_btn = QPushButton("Previous")
        self.prev_btn.clicked.connect(self.prev_page)
        self.page_label = QLabel("Page: 0/0")
        self.page_label.setAlignment(Qt.AlignCenter)
        self.next_btn = QPushButton("Next")
        self.next_btn.clicked.connect(self.next_page)
        
        nav_layout.addWidget(self.prev_btn)
        nav_layout.addWidget(self.page_label)
        nav_layout.addWidget(self.next_btn)
        
        center_layout.addWidget(self.pdf_view)
        center_layout.addLayout(nav_layout)
        
        # Right panel for AI 
        self.right_panel = QWidget()
        self.right_panel.setFixedWidth(300)
        self.right_panel.setStyleSheet("background-color: #ecf0f1; border-left: 1px solid #bdc3c7;")
        
        right_layout = QVBoxLayout(self.right_panel)
        
        ai_title = QLabel("AI Assistant")
        ai_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        ai_title.setAlignment(Qt.AlignCenter)
        
        self.ai_output = QTextEdit()
        self.ai_output.setReadOnly(True)
        self.ai_output.setPlaceholderText("AI responses will appear here...")
        self.ai_output.setStyleSheet("background-color: white; border: 1px solid #ddd; border-radius: 5px;")
        
        self.ai_input = QTextEdit()
        self.ai_input.setPlaceholderText("Type your question here...")
        self.ai_input.setStyleSheet("background-color: white; border: 1px solid #ddd; border-radius: 5px;")
        self.ai_input.setMaximumHeight(100)
        
        self.send_btn = QPushButton("Send")
        self.send_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        
        right_layout.addWidget(ai_title)
        right_layout.addWidget(self.ai_output)
        right_layout.addWidget(self.ai_input)
        right_layout.addWidget(self.send_btn)
        
        # Add panels to layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(self.center_panel, 1)
        main_layout.addWidget(self.right_panel)
        
        #  central widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        
        # Initialize with buttons disabled
        self.update_ui_state(False)
    
    def create_button(self, text, function):
        btn = QPushButton(text)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(function)
        return btn
    
    def select_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select PDF File", "", "PDF Files (*.pdf)"
        )
        
        if file_path:
            self.pdf_path = file_path
            self.current_page = 0
            self.load_pdf()
            self.update_ui_state(True)
    
    def load_pdf(self):
        try:
            # Open  PDF document
            self.doc = fitz.open(self.pdf_path)
            self.total_pages = len(self.doc)
            
            # Update page label
            self.page_label.setText(f"Page: {self.current_page + 1}/{self.total_pages}")
            
            # Display first page
            self.display_page(self.current_page)
            
        except Exception as e:
            self.pdf_content.setText(f"Error loading PDF: {str(e)}")
    
    def display_page(self, page_num):
        if self.doc and 0 <= page_num < self.total_pages:
            # Get the page
            page = self.doc[page_num]
            
            # Render page to pixmap
            zoom = 1.5  # Adjust zoom factor for readability
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            
            # Convert to QImage
            img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
            
            # Display image in label
            pixmap = QPixmap.fromImage(img)
            
            self.pdf_content = QLabel()
            self.pdf_content.setPixmap(pixmap)
            self.pdf_content.setAlignment(Qt.AlignCenter)
            
            # Update scroll area
            self.pdf_view.setWidget(self.pdf_content)
            
            # Update page label
            self.page_label.setText(f"Page: {page_num + 1}/{self.total_pages}")
    
    def next_page(self):
        if self.pdf_path and self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.display_page(self.current_page)
    
    def prev_page(self):
        if self.pdf_path and self.current_page > 0:
            self.current_page -= 1
            self.display_page(self.current_page)
    
    def update_ui_state(self, pdf_loaded):
        # Enable/disable nav buttons
        self.prev_btn.setEnabled(pdf_loaded)
        self.next_btn.setEnabled(pdf_loaded)
        
        # Enable function buttons when PDF is loaded
        self.ocr_btn.setEnabled(pdf_loaded)
        self.summarize_btn.setEnabled(pdf_loaded)
        self.ask_btn.setEnabled(pdf_loaded)
    
    #------FUNCTION FOR OCR PDF----------
    def ocr_pdf_function(self):
        if not self.pdf_path:
            self.ai_output.setText("Error: No PDF selected")
            return
            
        # Ask user if they want to save to downloads or temp
        from PyQt5.QtWidgets import QMessageBox
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Save Location")
        msg_box.setText("Where would you like to save the OCR'd PDF?")
        downloads_button = msg_box.addButton("Downloads", QMessageBox.ActionRole)
        temp_button = msg_box.addButton("Temp Folder", QMessageBox.ActionRole)
        cancel_button = msg_box.addButton("Cancel", QMessageBox.RejectRole)
        
        msg_box.exec_()
        
        if msg_box.clickedButton() == cancel_button:
            return
            
        output_path = None
        if msg_box.clickedButton() == downloads_button:
            # Get downloads folder path
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
            input_filename = os.path.basename(self.pdf_path)
            base_name = os.path.splitext(input_filename)[0]
            output_path = os.path.join(downloads_path, f"{base_name}_ocr.pdf")
        
        # Show processing message
        self.ai_output.setText("Processing OCR... This may take a while.")
        QApplication.processEvents()  # Update UI
        
        try:
            # Call the OCR function
            ocr_pdf(self.pdf_path, output_path)
            
            # Show success message with file location
            if output_path:
                self.ai_output.setText(f"OCR completed successfully!\nSaved to: {output_path}")
            else:
                self.ai_output.setText("OCR completed successfully!\nSaved to temporary folder.")
                
        except Exception as e:
            self.ai_output.setText(f"Error during OCR: {str(e)}")

    #------FUNCTION FOR SUMMARIZE PDF WITH AI----------
    def summarize_pdf_function(self):
        if not self.pdf_path:
            self.ai_output.setText("Error: No PDF selected")
            return
            
        self.ai_output.setText("Extracting text from PDF for summarization...")
        QApplication.processEvents()  # Update UI
        
        try:
            # Extract text from current PDF
            text = ""
            for page_num in range(self.total_pages):
                page = self.doc[page_num]
                text += page.get_text()
                
            if not text.strip():
                self.ai_output.setText("No text found in PDF. Try using OCR first.")
                return
                
            self.ai_output.setText("Generating summary... Please wait.")
            QApplication.processEvents()  # Update UI
            
            # Generate summary using the imported function
            summary = generate_pdf_summary(text)
            
            # Display the summary
            self.ai_output.setText(summary)
            
        except Exception as e:
            self.ai_output.setText(f"Error generating summary: {str(e)}")
    
    #------FUNCTION FOR ASK AI A QUESTION IN PDF----------
    def ask_question_function(self):
        if not self.pdf_path:
            self.ai_output.setText("Error: No PDF selected")
            return
            
        question = self.ai_input.toPlainText().strip()
        if not question:
            self.ai_output.setText("Please enter a question to ask about the PDF.")
            return
            
        self.ai_output.setText("Processing your question... Please wait.")
        QApplication.processEvents()  # Update UI
        
        try:
            # Extract text from current PDF
            text = ""
            for page_num in range(self.total_pages):
                page = self.doc[page_num]
                text += page.get_text()
                
            if not text.strip():
                self.ai_output.setText("No text found in PDF. Try using OCR first.")
                return
                
            # Generate answer using the imported function
            answer = generate_pdf_question(question, text)
            
            # Display the answer
            self.ai_output.setText(f"Q: {question}\n\nA: {answer}")
            
        except Exception as e:
            self.ai_output.setText(f"Error processing question: {str(e)}")
            
        # Clear the input field after processing
        self.ai_input.clear()

def main():
    app = QApplication(sys.argv)
    window = PDFToolGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
