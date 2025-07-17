from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit,
    QFileDialog, QMessageBox
)
from PyQt5.QtGui import QPixmap


class MainWindowUI(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self._init_ui()

    def _init_ui(self):
        # Main layout
        layout = QVBoxLayout()

        # Image selection section
        self.image_label = QLabel("Selected Image:")
        self.btn_open_image = QPushButton("Open Image")
        self.image_preview = QLabel()
        self.image_preview.setFixedSize(400, 300)

        # Results display
        self.result_label = QLabel("OCR Results:")
        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)

        # Export button
        self.btn_export = QPushButton("Export Results")
        layout.addWidget(self.btn_export)

        # Arrange widgets
        layout.addWidget(self.image_label)
        layout.addWidget(self.btn_open_image)
        layout.addWidget(self.image_preview)
        layout.addWidget(self.result_label)
        layout.addWidget(self.text_output)
        layout.addWidget(self.btn_export)

        self.setLayout(layout)

    def get_image_path(self):
        """Open file dialog to select image"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "",
            "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            pixmap = QPixmap(file_path)
            self.image_preview.setPixmap(pixmap.scaled(
                self.image_preview.size(),
                aspectRatioMode=1  # Keep aspect ratio
            ))
            return file_path
        return None

    def display_results(self, text):
        """Display OCR results"""
        self.text_output.clear()
        self.text_output.append(text)

    def show_success(self, message):
        QMessageBox.information(self, "Success", message)

    def show_error(self, message):
        """Show error message"""
        QMessageBox.critical(self, "Error", message)
