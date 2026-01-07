from abc import ABC, abstractmethod

class OCREngine(ABC):
    @abstractmethod
    def extract_text(self, image): # Removed -> str type hint to be flexible
        pass