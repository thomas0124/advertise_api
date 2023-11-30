from fastapi import FastAPI, File, UploadFile
import easyocr
from PIL import Image
import io

app = FastAPI()

reader = easyocr.Reader(['en'])  # 'en'は英語の言語コードです

@app.get("/")
def read_root():
    return {"message": "Hello World!"}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}

@app.post("/extract_text/")
async def extract_text_from_image(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))

    # 画像からテキストを抽出
    result = reader.readtext(image)

    # OCRの結果を抽出したテキストに変換
    extracted_text = ' '.join([entry[1] for entry in result])

    return {"extracted_text": extracted_text}
