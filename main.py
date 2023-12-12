from fastapi import FastAPI, File, UploadFile
import easyocr
from PIL import Image
import io
import cv2
from test import get_status

app = FastAPI()

reader = easyocr.Reader(['en'])  # 'en'は英語の言語コードです


@app.post("/extract_text/")
async def extract_text_from_image(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))

    # 画像からテキストを抽出
    result = reader.readtext(image)

    # OCRの結果を抽出したテキストに変換
    extracted_text = ' '.join([entry[1] for entry in result])

    return {"extracted_text": extracted_text}

@app.post("/status/")
async def status(file: UploadFile = File(...)):
    file_path =  file.filename
    img_input = cv2.imread(file_path)
    return {"status": get_status(img_input)}