from fastapi import FastAPI, File, UploadFile
from PIL import Image
import io
import cv2
from test import get_status

app = FastAPI()

@app.post("/status/")
async def status(file: UploadFile = File(...)):
    file_path =  file.filename
    img_input = cv2.imread(file_path)
    return {"status": get_status(img_input)}
