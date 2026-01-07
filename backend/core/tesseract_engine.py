import pytesseract
from PIL import ImageEnhance
from .ocr_interface import OCREngine

class TesseractOCR(OCREngine):
    def extract_text(self, image):

        # Convert to Grayscale
        img = image.convert('L')
        
        # Increase Contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0) # Double the contrast
        
        # Simple thresholding to convert to pure black and white
        thresh = 200
        fn = lambda x : 255 if x > thresh else 0
        img = img.point(fn, mode='1')
        


        # Tesseract Configuration
        custom_config = r'--psm 6 -c preserve_interword_spaces=1'
        
        raw_text = pytesseract.image_to_string(
            img, 
            lang='sin+eng', 
            config=custom_config
        )
        
        return [{
            "text": raw_text,
            "is_header": False
        }]