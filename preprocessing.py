import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image

IMG_SIZE = (224, 224)

def preprocess_image(image: Image.Image):
    # ensure RGB
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # resize image
    image = image.resize(IMG_SIZE, Image.Resampling.LANCZOS)

    # convert to array
    img_array = img_to_array(image) / 255.0

    # add batch dimension
    return np.expand_dims(img_array, axis=0)