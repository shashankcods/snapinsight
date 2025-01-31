import cv2
import numpy as np
import os

def analyze_image(image_path):
    print(f"Analyzing image: {image_path}")

    if not os.path.exists(image_path):
        return FileNotFoundError(f"Image not found: {image_path}")
    
    image = cv2.imread(image_path)
    if image is None:
        return ValueError(f"OpenCV failed to load image: {image_path}")
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray)
    contrast = np.std(gray)

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    saturation = np.mean(hsv[:, :, -1])
    sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()

    brightness_score = min(max((brightness / 255) * 100, 0), 100)
    contrast_score = min(max((contrast / 128) * 100, 0), 100)
    saturation_score = min(max((saturation / 255) * 100, 0), 100)
    sharpness_score = min(max((sharpness / 500) * 100, 0), 100)

    overall_score = (brightness_score*0.25 + contrast_score*0.25 + saturation_score*0.25 + sharpness_score*0.25)

    return brightness_score, contrast_score, saturation_score, sharpness_score, overall_score