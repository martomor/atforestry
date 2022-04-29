from PIL import Image
import cv2
import numpy as np
from .utils import get_model
from PIL import Image
import matplotlib.image as mpimg
from io import BytesIO

model = get_model()

labels = ['slash_burn',
 'water',
 'habitation',
 'partly_cloudy',
 'road',
 'artisinal_mine',
 'cultivation',
 'bare_ground',
 'clear',
 'conventional_mine',
 'haze',
 'selective_logging',
 'primary',
 'agriculture',
 'cloudy',
 'blooming',
 'blow_down']

def map_predictions(prediction):
    results = prediction[0] > 0.2
    true_index_values = [i for i, x in enumerate(results) if x]
    tags_results = [labels[x] for x in true_index_values]
    return tags_results

def predict_land_cover(image_file):
    image_data = BytesIO(image_file)
    file_bytes = np.asarray(bytearray(image_data.read()), dtype=np.uint8)
    img_array = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    img_reshape = cv2.resize(src = img_array, dsize=(128, 128))
    img_reshape = np.expand_dims(img_reshape, axis=0)
    prediction = model.predict(img_reshape)
    tags_results = map_predictions(prediction)
    return tags_results

