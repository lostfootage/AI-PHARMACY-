%%writefile app.py
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from model import extract_prescription_data
from huggingface_model import extract_prescription_data_hf
from PIL import Image
import pytesseract
import shutil
import os

app = FastAPI()

@app.post("/upload/")
async def upload_prescription(file: UploadFile = File(...), method: str = Form('simple')):
    try:
        file_location = f"temp_{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        if file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img = Image.open(file_location)
            script_text = pytesseract.image_to_string(img)
        elif file.filename.lower().endswith('.txt'):
            with open(file_location, 'r', encoding='utf-8') as f:
                script_text = f.read()
        else:
            return JSONResponse(content={"error": "Unsupported file type."}, status_code=400)

        if method == "huggingface":
            structured_data = extract_prescription_data_hf(script_text)
        else:
            structured_data = extract_prescription_data(script_text)

        os.remove(file_location)
        return {"extracted_data": structured_data}

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
