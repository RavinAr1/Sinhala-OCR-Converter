# Use Python runtime as a parent image
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-sin \
    libtesseract-dev \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*


# Setup a non-root user (for Hugging Face Security)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH


    
# Set the working directory
WORKDIR $HOME/app



# Copy backend requirements and install
# --chown=user so the new user owns these files
COPY --chown=user backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code
COPY --chown=user backend ./backend

# Create uploads directory - temporary file storage
RUN mkdir -p uploads && chmod 777 uploads

# Expose the port
EXPOSE 7860

# Run the application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"]