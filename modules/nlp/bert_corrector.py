import os
import sys
import torch
from transformers import BertForMaskedLM, BertTokenizer
from core.config import Config


class BanglaBERTCorrector:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_path = self._get_model_path()

        # Verify model files exist
        required_files = ["config.json", "pytorch_model.bin", "vocab.txt"]
        for file in required_files:
            if not os.path.exists(os.path.join(self.model_path, file)):
                raise FileNotFoundError(
                    f"Missing BERT model file: {file}\n"
                    f"Expected at: {self.model_path}\n"
                    f"Files found: {os.listdir(self.model_path)}"
                )

        # Load model
        self.tokenizer = BertTokenizer.from_pretrained(self.model_path)
        self.model = BertForMaskedLM.from_pretrained(self.model_path).to(self.device)

    def _get_model_path(self):
        """Resolve model path for both development and PyInstaller environments"""
        # 1. Check if running as PyInstaller bundle
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS  # PyInstaller temp folder
            return os.path.join(base_path, "bangla-bert")

        # 2. Normal development environment
        return os.path.join(Config.MODEL_DIR, "bert", "bangla-bert")

    def correct_text(self, text):
        """Corrects Bangla text using BERT masked language modeling"""
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512  # Prevent OOM errors
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model(**inputs)

        predicted_indices = torch.argmax(outputs.logits, dim=-1)
        return self.tokenizer.decode(predicted_indices[0], skip_special_tokens=True)

    def batch_correct(self, texts):
        """Process multiple texts efficiently"""
        results = []
        for text in texts:
            results.append(self.correct_text(text))
        return results
