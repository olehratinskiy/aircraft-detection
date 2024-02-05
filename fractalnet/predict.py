import cv2
import tensorflow as tf
from tensorflow import keras
import numpy as np

print(tf.__version__)


def preprocess_image(img):
    image = cv2.imdecode(np.frombuffer(img.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    if image.shape[-1] == 4:
        image = image[:, :, :3]
    return image


# def make_predictions(img):
#     fractal_model = keras.models.load_model('D:\\diploma\\fractalnet\\fractalnet.h5')
#
#     img = img.astype(np.float32)
#     img /= 255.0
#
#     predictions = fractal_model.predict(img)
#
#     types = ['attack_helicopters', 'fighter_aircrafts', 'il-76', 'tu-22', 'tu-95', 'tu-160', 'noaircrafts']
#     aircraft_type = types[int(predictions.argmax(axis=1))]
#     accuracy = float(np.max(predictions))
#
#     return aircraft_type, accuracy


def make_predictions(img):
    fractal_model = keras.models.load_model('D:\\diploma\\fractalnet\\fractalnet.h5')

    img_resized = cv2.resize(img, (128, 128))

    img_resized = np.expand_dims(img_resized, axis=0)

    img_resized = img_resized / 255.0

    predictions = fractal_model.predict(img_resized)

    types = ['attack_helicopters', 'fighter_aircrafts', 'il-76', 'tu-22', 'tu-95', 'tu-160', 'noaircrafts']
    aircraft_type = types[int(predictions.argmax(axis=1))]
    accuracy = float(np.max(predictions))

    return aircraft_type, accuracy

