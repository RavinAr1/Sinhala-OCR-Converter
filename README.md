# Sinhala OCR & Document Converter

A simple OCR tool designed to digitize Sinhala documents. It converts scanned PDFs and Images into editable Word documents (`.docx`) using an enhanced Tesseract OCR engine.


## 🌐 Live Demo
Try the application online: **[Click Here](https://sinhala-ocr-converter.vercel.app/)**


## 🚀 Key Technical Implementations
* **Sinhala Character Recognition:** Optimized for standard Sinhala Unicode text using Tesseract 5.
* **Streaming Architecture:** Implements a custom page-by-page processing pipeline to handle to process files safely on free hosting services.
* **Optimized Sinhala OCR:** Fine-tuned Tesseract 5 with specific contrast enhancement and binarization preprocessing steps to maximize accuracy for Sinhala Unicode script.


## ⚠️ Current Status & Limitations
* **Accuracy:** The OCR engine (Tesseract) performs reasonably well on clear, high-contrast documents (both PDF and Images).
* **Formatting:** While basic paragraph structure is preserved, complex layouts (like multi-column news articles or tables) may lose their original positioning. 

    ( **Formatting Improvements Needed:** The document reconstruction logic is currently simple. It centers titles and aligns text based on page position, but it does not yet perfectly replicate complex indentation, bullet points, or exact font sizes from the original file. )

* **Best Results:** Can be obtained from official letters, and clear book pages.


## 🛠️ Tech Stack
* **Frontend:** Next.js, React, Tailwind CSS
* **Backend:** Python, FastAPI
* **OCR Engine:** Tesseract (with Sinhala training data)
* **Processing:** PyMuPDF (Fitz), Pillow, pdf2image
* **Deployment:** Docker (Render), Vercel
* **Document Generation:** python-docx

## 🏃‍♂️ How to Run Locally

### Prerequisites
1.  **Install Python 3.10+**
2.  **Install Tesseract OCR:**
    * Windows: [Download here](https://github.com/UB-Mannheim/tesseract/wiki)
    
         **Important:** During install, select "Sinhala" in "Additional Script Data".
    * **macOS (Homebrew):**

            brew install tesseract
            brew install tesseract-lang
            
    
3.  **Install Poppler:**
    *  **Windows:** Download Poppler from [Here](https://github.com/oschwartz10612/poppler-windows/releases/tag/v25.12.0-0)  and add the `bin` folder to the System PATH.

    * **macOS:** `brew install poppler`


### Installation
```bash
# 1. Clone the repo
git clone <https://github.com/RavinAr1/Sinhala-OCR-Converter.git>
cd sinhala-ocr

# 2. Create Virtual Environment
python -m venv venv

# Activate Virtual Environment:
.\venv\Scripts\activate  # Windows

source venv/bin/activate # macOS / Linux

# 3. Install Dependencies
pip install -r backend/requirements.txt

# 4. Setup Frontend
# Make sure you are in the root folder with venv activated
cd frontend
npm install

# Configuration

Rename the .env.example file to .env.local 
#(or ensure environment variables are set up as needed.)


# 4. Start the Application
# Terminal 1: Backend - Make sure you are in the root folder with venv activated
uvicorn backend.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev

```


Open a browser and natigate to : https://localhost:3000