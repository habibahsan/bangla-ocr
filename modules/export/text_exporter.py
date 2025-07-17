import os
from datetime import datetime
from docx import Document


class TextExporter:
    @staticmethod
    def export_txt(text, output_dir="output"):
        """Export text to a TXT file"""
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(output_dir, f"bangla_ocr_{timestamp}.txt")

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)
        return filename

    @staticmethod
    def export_docx(text, output_dir="output"):
        """Export text to a DOCX file"""
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(output_dir, f"bangla_ocr_{timestamp}.docx")

        doc = Document()
        doc.add_paragraph(text)
        doc.save(filename)
        return filename
