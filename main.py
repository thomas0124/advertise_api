from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image
import io
import cv2
import numpy as np

app = FastAPI()

def convert_to_grayscale(file):
    # 画像を読み込む
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    # グレースケールに変換
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # グレースケール画像をバイトデータに変換
    retval, buffer = cv2.imencode('.jpg', gray_img)
    gray_img_bytes = buffer.tobytes()

    return gray_img_bytes

@app.post("/")
async def convert_to_grayscale_api(file: UploadFile = File(...)):
    gray_img_bytes = convert_to_grayscale(file)

    return StreamingResponse(io.BytesIO(gray_img_bytes), media_type="image/jpeg")

@app.get("/")
def read_root():
    return {"message": "Hello World!"}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}
