from PyQt5.QtWidgets import QMainWindow, QFileDialog
from modules.ocr.bangla_ocr import BanglaOCR
from modules.nlp.bert_corrector import BanglaBERTCorrector
from modules.nlp.spacy_processor import BanglaNLPProcessor
from ui.main_window import MainWindowUI
from modules.export.text_exporter import TextExporter
import os


class BanglaOCRApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bangla OCR Application")
        self.setGeometry(100, 100, 800, 600)

        # Initialize modules and state
        self.ocr_processor = BanglaOCR()
        self.bert_corrector = BanglaBERTCorrector()
        self.nlp_processor = BanglaNLPProcessor()
        self.current_text = ""  # Initialize text storage

        # Setup UI
        self.ui = MainWindowUI(self)
        self.setCentralWidget(self.ui)

        # Connect signals
        self._connect_signals()

    def _connect_signals(self):
        self.ui.btn_open_image.clicked.connect(self._process_image)
        self.ui.btn_export.clicked.connect(self._export_results)

    def _process_image(self):
        try:
            image_path = self.ui.get_image_path()
            raw_text = self.ocr_processor.extract_text(image_path)
            corrected_text = self.bert_corrector.correct_text(raw_text)

            # Store the processed text
            self.current_text = corrected_text

            self.ui.display_results(corrected_text)

        except Exception as e:
            self.ui.show_error(f"Processing failed: {str(e)}")

    def _export_results(self):
        if not self.current_text:  # More pythonic check
            self.ui.show_error("No text to export! Process an image first.")
            return

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Results",
            "",
            "Text Files (*.txt);;Word Documents (*.docx)"
        )

        if filename:
            try:
                if filename.endswith('.txt'):
                    saved_path = TextExporter.export_txt(
                        self.current_text, os.path.dirname(filename))
                else:
                    saved_path = TextExporter.export_docx(
                        self.current_text, os.path.dirname(filename))

                self.ui.show_success(f"Exported to:\n{saved_path}")
            except Exception as e:
                self.ui.show_error(f"Export failed: {str(e)}")
