from fastapi import FastAPI, File, UploadFile
import cv2
import numpy as np
from pathlib import Path
from typing import List

app = FastAPI()

def get_status(img_raw):
    def calculate_hsv_values(hsv_list):
        N = int(len(hsv_list)/3)
        h, s, v = np.zeros((N),np.uint8), np.zeros((N),np.uint8), np.zeros((N),np.uint8)
        for i in range(N):
            h[i], s[i], v[i] = hsv_list[i*3], hsv_list[i*3+1], hsv_list[i*3+2]
        return h, s, v

    def calculate_ave_median_mode(h, s, v):
        ave = [int(np.sum(h)/max(np.count_nonzero(h),1)), int(np.mean(s)), int(np.mean(v))]
        median = [int(np.median(h[np.nonzero(h)])) if h[np.nonzero(h)].size != 0 else 0, int(np.median(s)), int(np.median(v))]
        mode = [np.unique(h,return_counts=True)[0][np.argmax(np.unique(h,return_counts=True)[1])],
                np.unique(s,return_counts=True)[0][np.argmax(np.unique(s,return_counts=True)[1])],
                np.unique(v,return_counts=True)[0][np.argmax(np.unique(v,return_counts=True)[1])]]
        return ave, median, mode

    def calculate_status(h, use, ave, median, mode, gray_var):
        type_list: str = ['Red','Yellow','Green', 'Blue', 'Keyplate']
        h += 30*use
        chara_type = type_list[0] if (162<h or h<=18) else type_list[1] if np.sum(h) == 0 and mode[2] >= 126 else type_list[4] if np.sum(h) == 0 else [type_list[i+1] for i in range(4) if (i+1)*36-18<h and h<=(i+1)*36+18][0]
        HP = int(((3000-1000)/255)*ave[2] + 1000)
        A = int(((1000-300)/255)*median[1] + 300)
        B = int(((1000-300)/255)*median[2] + 300)
        C = int(((1000-300)/255)*(255-mode[1]) + 300)
        D = int(((1000-300)/255)*(255-mode[2]) + 300)
        S = int(((1000-300)/255)*ave[0] + 300) + int(gray_var / 10)
        S = min(S,1000)
        return [chara_type, HP, A, B, C, D, S]

    img_re = cv2.resize(img_raw, dsize=(100,100))
    img = cv2.blur(img_re, (5, 5))
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    hsv_list = hsv.ravel()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray_var = np.var(gray.ravel())
    h, s, v = calculate_hsv_values(hsv_list)
    ave, median, mode = calculate_ave_median_mode(h, s, v)
    showimg = np.zeros((300,300,3),np.uint8)
    use_ave = 1 if mode[2]<22 or mode[1] < 20 else 0
    showimg[:,:] = [ave[0],ave[1],ave[2]] if use_ave else [mode[0],mode[1],mode[2]]
    return calculate_status(showimg[0][0][0], use_ave, ave, median, mode, gray_var)

@app.post("/status/")
async def status(files: List[UploadFile] = File(...)):
    try:
        # Create a directory for file uploads if it doesn't exist
        upload_dir = Path("uploads")
        upload_dir.mkdir(parents=True, exist_ok=True)

        # Save the uploaded file
        file_location = upload_dir / files[0].filename
        with open(file_location, "wb") as buffer:
            buffer.write(files[0].file.read())

        # Read the saved file using OpenCV
        img_input = cv2.imread(str(file_location))
        
        status = get_status(img_input)
        
        return {"status": status}

    except Exception as e:
        return {"error": str(e)}
