import os
import shutil
import fitz  # PyMuPDF
import re
from PIL import Image, ImageOps
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from backend.core.tesseract_engine import TesseractOCR
from pdf2image import convert_from_path

app = FastAPI()
os.makedirs("uploads", exist_ok=True)

# Initialize Tesseract
ocr_tool = TesseractOCR()

def extract_images_from_page(pdf_path, page_index, output_folder):
    """ Extracts embedded raster images (Logos/Photos) from PDFs """
    doc = None
    try:
        doc = fitz.open(pdf_path)
        page = doc[page_index]
        image_list = page.get_images(full=True)
        extracted_paths = []
        
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            if len(image_bytes) < 3000: continue 
            
            filename = f"{output_folder}/p{page_index}_{img_index}.{image_ext}"
            with open(filename, "wb") as f:
                f.write(image_bytes)
            extracted_paths.append(filename)
        return extracted_paths
    except:
        return []
    finally:
        if doc: doc.close()

@app.post("/convert")
async def convert_file(file: UploadFile = File(...)):
    # Save Uploaded File Locally                     
    file_location = f"uploads/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Prepare Word Document
    doc = Document()
    section = doc.sections[0]
    section.left_margin = Inches(0.5)
    section.right_margin = Inches(0.5)

    # Load Images from File
    ocr_images = []
    is_pdf = file.filename.lower().endswith(".pdf")
    print(f"Processing: {file.filename}")

    if is_pdf:
        try:
            
            ocr_images = convert_from_path(file_location, dpi=450)
        except Exception as e:
            return {"error": "PDF Conversion Failed", "details": str(e)}
    else:
        try:
            img = Image.open(file_location)
            img = ImageOps.exif_transpose(img) 
            ocr_images = [img] 
        except Exception as e:
            return {"error": "Invalid Image File", "details": str(e)}

    # Process Each Page/Image
    for i, ocr_img in enumerate(ocr_images):
        print(f"Processing Page {i+1}...")

        # Extract Embedded Images (Logos/Photos)
        if is_pdf:
            extracted = extract_images_from_page(file_location, i, "uploads")
            if extracted:
                if len(extracted) > 1 and i == 0:
                    tbl = doc.add_table(rows=1, cols=len(extracted))
                    tbl.autofit = True
                    for idx, path in enumerate(extracted):
                        cell = tbl.cell(0, idx)
                        p = cell.paragraphs[0]
                        r = p.add_run()
                        r.add_picture(path, width=Inches(1.2))
                        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    for path in extracted:
                        doc.add_picture(path, width=Inches(2.5))

        # OCR the Page/Image
        try:
            blocks = ocr_tool.extract_text(ocr_img)
            
            #  FALLBACK MECHANISM FOR LOW TEXT PAGES 
            full_text = "".join([b['text'] for b in blocks]).strip()
            if len(full_text) < 50 and is_pdf:
                print(f"   -> Low text on Page {i+1}. Using Image Fallback.")
                fallback_path = f"uploads/fallback_p{i}.jpg"
                ocr_img.save(fallback_path)
                doc.add_picture(fallback_path, width=Inches(6.0))
                doc.add_page_break()
                continue
            

            for block in blocks:
                raw_text = block['text']
                
                # Split into Lines and Process Each Line
                lines = raw_text.split('\n')
                
                for line in lines:
                    line = line.strip()
                    if not line: continue

                    
                    # HEADER DETECTION 
                    is_header = False
                    if len(line) < 50 and ("විභාගය" in line or "පාසල" in line or "ශ්‍රේණිය" in line):
                        is_header = True

                    
                    # DOTTED LINE DETECTION
                    needs_dots = False
                    if re.match(r'^(\d+\.|[ivx]+\.)', line):
                        # Numbered Question
                        if line.endswith("?") or line.endswith("ද?") or len(line) > 30:
                            if "......" not in line:
                                needs_dots = True

                    #  ADD TO DOCUMENT
                    p = doc.add_paragraph()
                    run = p.add_run(line)
                    run.font.name = 'Iskoola Pota'
                    
                    if is_header:
                        run.bold = True
                        run.font.size = Pt(14)
                        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    else:
                        run.font.size = Pt(11)

                    # Add Dotted Line if Needed
                    if needs_dots:
                        p_dots = doc.add_paragraph()
                        #  Adjust dots to fit the page width
                        p_dots.add_run(".............................................................................................................")

            doc.add_page_break()

        except Exception as e:
            print(f"Error on page {i+1}: {e}")
            p = doc.add_paragraph(f"[OCR Failed: {str(e)}]")
            p.runs[0].font.color.rgb = RGBColor(255, 0, 0)

    # Save and Return Document
    output_name = f"uploads/{file.filename}_converted.docx"
    doc.save(output_name)
    return FileResponse(output_name, filename=f"converted_{file.filename}.docx")