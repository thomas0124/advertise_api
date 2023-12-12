from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image
import io
import cv2
import numpy as np

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World!"}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}
