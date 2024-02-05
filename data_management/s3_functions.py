import cv2
import os
import base64


def save_image_to_directory(img_name, img):
    cv2.imwrite(os.path.join('D:\\diploma\\test_images', img_name), img)


def load_image_from_directory(img_name):
    image_path = os.path.join('D:\\diploma\\test_images', img_name)
    image = cv2.imread(image_path)
    return base64.b64encode(cv2.imencode('.jpg', image)[1].tobytes()).decode('utf-8')
