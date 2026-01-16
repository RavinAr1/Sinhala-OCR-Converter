import pytesseract
from pytesseract import Output
from PIL import ImageEnhance
from .ocr_interface import OCREngine

class TesseractOCR(OCREngine):
    def extract_text(self, image):

        # Convert to Grayscale
        img = image.convert('L')
        
        # Increase Contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0) 
        
        # Binarization
        thresh = 200
        fn = lambda x : 255 if x > thresh else 0
        img = img.point(fn, mode='1')
        
        # Get Image Dimensions
        width, height = img.size

        
        # OCR with Tesseract
        custom_config = r'--psm 6 -c preserve_interword_spaces=1'
        

        # Data Extraction
        data = pytesseract.image_to_data(
            img, 
            lang='sin+eng', 
            config=custom_config, 
            output_type=Output.DICT
        )
        


        # Group Words into Lines with Alignment
        lines = []
        n_boxes = len(data['text'])
        
        current_line_words = []
        current_line_left = []
        current_line_right = []
        last_line_id = None 

        for i in range(n_boxes):

            # Skip Low Confidence / Empty Words
            if int(data['conf'][i]) == -1: continue
            word = data['text'][i].strip()
            if not word: continue


            # Identify Line by Block, Paragraph, Line Numbers
            line_id = (data['block_num'][i], data['par_num'][i], data['line_num'][i])

            if line_id != last_line_id:

                # Process Previous Line
                if current_line_words:
                    lines.append(self._process_line(current_line_words, current_line_left, current_line_right, width))
                
                # Start New Line
                current_line_words = []
                current_line_left = []
                current_line_right = []
                last_line_id = line_id

            current_line_words.append(word)
            current_line_left.append(data['left'][i])
            current_line_right.append(data['left'][i] + data['width'][i])

        # Process Last Line
        if current_line_words:
            lines.append(self._process_line(current_line_words, current_line_left, current_line_right, width))
        
        return lines

    # Function to process a line and determine alignment
    def _process_line(self, words, lefts, rights, page_width):
        

        text = " ".join(words)
        min_left = min(lefts)
        max_right = max(rights)
        
        align = "left" # Default
        
        # Right Alignment Check
        if min_left > (page_width * 0.5):
            align = "right"
            
        # Center Alignment Check
        elif min_left > (page_width * 0.15) and max_right < (page_width * 0.85):
            align = "center"

        return {
            "text": text,
            "align": align
        }