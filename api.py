from fastapi import FastAPI, File, UploadFile
from PIL import Image
import io
from conversion import convert_existing_image
from common import Resolution

app = FastAPI()


@app.post("/get_mosaic_for_photo/")
async def get_mosaic_for_photo(file: UploadFile = File(...)):
    i = Image.open(io.BytesIO(file.file.read()))
    res = convert_existing_image(i, Resolution(30, 30))
    return res
