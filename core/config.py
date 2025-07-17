import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Tesseract configuration
    TESSERACT_CONFIG = {
        "lang": "ben",
        "oem": 3,
        "psm": 6,
        "path": os.getenv("TESSERACT_PATH", None)  # Set in .env if needed
    }

    # BERT model configuration
    BERT_MODEL = "sagorsarker/bangla-bert-base"

    # Application settings
    APP_NAME = "Bangla OCR Desktop App"
    VERSION = "1.0.0"

    # File paths
    MODEL_DIR = os.path.join(os.path.dirname(__file__), "../models")
    ASSETS_DIR = os.path.join(os.path.dirname(__file__), "../assets")
