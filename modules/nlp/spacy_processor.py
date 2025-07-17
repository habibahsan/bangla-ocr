import spacy
import os
from spacy.lang.bn import Bengali
from core.config import Config


class BanglaNLPProcessor:
    def __init__(self):
        self.model_path = os.path.join(Config.MODEL_DIR, "spacy/bn")

        # Try to load custom model if exists
        if os.path.exists(self.model_path):
            try:
                self.nlp = spacy.load(self.model_path)
                print("Loaded custom Bangla spaCy model")
                return
            except Exception as e:
                print(f"Failed to load custom model: {e}")

        # Fallback to blank model
        print("Using blank Bengali model")
        self.nlp = Bengali()
        self._add_basic_components()

    def _add_basic_components(self):
        if not self.nlp.has_pipe("sentencizer"):
            self.nlp.add_pipe("sentencizer")

    def process_text(self, text):
        doc = self.nlp(text)
        return {
            "sentences": [sent.text for sent in doc.sents],
            "tokens": [token.text for token in doc]
        }
