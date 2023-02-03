"""
API interface for converting images to wordle mosaics.
"""
import io

from fastapi import FastAPI, File, UploadFile
from PIL import Image
from conversion import convert_existing_image
from common import Resolution

app = FastAPI()


@app.post("/get_mosaic_for_photo/")
async def get_mosaic_for_photo(file: UploadFile = File(...)):
    """
    Processed the uploaded file and turns it into a mosaic image.
    """
    # TODO add a check to verify the file is actually a image.
    i = Image.open(io.BytesIO(file.file.read()))
    res = convert_existing_image(i, Resolution(30, 30))
    return res
