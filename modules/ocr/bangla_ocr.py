import os
import cv2
import pytesseract
from dotenv import load_dotenv
from bnunicodenormalizer import Normalizer


class BanglaOCR:
    def __init__(self):
        self.normalizer = Normalizer()
        # Load environment variables
        load_dotenv()

        # Configure Tesseract path from .env
        tesseract_path = os.getenv("TESSERACT_PATH")
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
            print(f"Tesseract path set to: {tesseract_path}")
        else:
            raise EnvironmentError("TESSERACT_PATH not found in .env file")

    def _preprocess_image(self, image_path):
        """Enhance image for better OCR results"""
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        return thresh

    def extract_text(self, image_path):
        try:
            # Preprocess image
            processed_img = self._preprocess_image(image_path)

            # Perform OCR
            custom_config = r'--oem 3 --psm 6 -l ben'
            text = pytesseract.image_to_string(processed_img, config=custom_config)

            # Normalize Bangla text
            normalized_text = self._normalize_bangla_text(text)

            return normalized_text
        except Exception as e:
            raise Exception(f"OCR extraction failed: {str(e)}")

    def _normalize_bangla_text(self, text):
        """Normalize Bangla Unicode characters"""
        normalized = []
        for word in text.split():
            normalized_word = self.normalizer(word)
            if normalized_word:
                normalized.append(normalized_word['normalized'])
        return " ".join(normalized)
