from PIL import Image
import cv2
import numpy as np
from .utils import get_model
from PIL import Image
import matplotlib.image as mpimg
from io import BytesIO

model = get_model()

def predict_land_cover(image_file):
    image_data = BytesIO(image_file)
    file_bytes = np.asarray(bytearray(image_data.read()), dtype=np.uint8)
    img_array = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    img_reshape = cv2.resize(src = img_array, dsize=(128, 128))
    img_reshape = np.expand_dims(img_reshape, axis=0)
    prediction = model.predict(img_reshape)
    return prediction