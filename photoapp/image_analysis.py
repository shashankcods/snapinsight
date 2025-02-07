import torch
import clip
from PIL import Image
import numpy as np
import cv2

device = "cuda" if torch.cuda.is_available() else "cpu"
global_model, global_preprocess = clip.load("ViT-B/32", device)

def classify_image(image_path):
    global global_model, global_preprocess
    image = global_preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    categories = [
        "daylight scene", "moonlit night", "indoor", "portrait", "sunset", 
        "underwater", "foggy", "landscape", "urban", "macro",
    ]
    
    text_inputs = torch.cat([clip.tokenize(f"a photo of a {c}") for c in categories]).to(device)
    
    with torch.no_grad():
        image_features = global_model.encode_image(image)
        text_features = global_model.encode_text(text_inputs)
        similarity = (image_features @ text_features.T).softmax(dim=-1)
    
    category_idx = similarity.argmax().item()
    return categories[category_idx]

def get_ideal_values(image_category):
    ideal_values = {
        "daylight scene":     {"temperature": 1.0, "tint": 1.0, "exposure": 1.0, "contrast": 1.0, "highlights": 1.0, "shadows": 1.0, "whites": 1.0, "blacks": 1.0, "vibrance": 1.0, "saturation": 1.0},
        "moonlit night":      {"temperature": 0.8, "tint": 0.9, "exposure": 0.7, "contrast": 1.2, "highlights": 0.6, "shadows": 0.5, "whites": 0.7, "blacks": 0.8, "vibrance": 0.7, "saturation": 0.7},
        "indoor":            {"temperature": 1.1, "tint": 1.0, "exposure": 0.9, "contrast": 1.1, "highlights": 1.0, "shadows": 0.9, "whites": 1.0, "blacks": 1.0, "vibrance": 0.9, "saturation": 0.9},
        "portrait":          {"temperature": 1.0, "tint": 1.0, "exposure": 1.1, "contrast": 1.0, "highlights": 1.1, "shadows": 1.0, "whites": 1.1, "blacks": 1.0, "vibrance": 1.0, "saturation": 1.0},
        "sunset":            {"temperature": 1.3, "tint": 1.2, "exposure": 0.8, "contrast": 1.2, "highlights": 1.2, "shadows": 0.8, "whites": 1.1, "blacks": 0.9, "vibrance": 1.2, "saturation": 1.2},
        "foggy":             {"temperature": 0.9, "tint": 1.0, "exposure": 0.7, "contrast": 0.5, "highlights": 0.6, "shadows": 0.7, "whites": 0.6, "blacks": 0.6, "vibrance": 0.6, "saturation": 0.6},
    }
    return ideal_values.get(image_category, ideal_values["daylight scene"])

def compute_current_values(image_path):
    image = Image.open(image_path).convert("RGB")
    np_image = np.array(image)
    grayscale = image.convert("L")
    
    brightness = np.mean(np.array(grayscale)) / 255.0  
    hist = cv2.calcHist([np.array(grayscale)], [0], None, [256], [0, 256])
    midtones = np.sum(hist[85:170]) / np.sum(hist)  # Midtone balance
    exposure = (brightness + midtones) / 2

    contrast = np.std(np.array(grayscale)) / 255.0  
    
    red, green, blue = np.mean(np_image[:, :, 0]), np.mean(np_image[:, :, 1]), np.mean(np_image[:, :, 2])
    temperature = red / (blue + 1e-6)
    tint = red / (green + 1e-6)
    
    hsv = cv2.cvtColor(np_image, cv2.COLOR_RGB2HSV)
    saturation = np.mean(hsv[:, :, 1]) / 255.0
    vibrance = np.std(hsv[:, :, 1]) / 255.0  
    
    shadows = np.mean(np_image[np_image < 50]) / 255.0 if np_image[np_image < 50].size > 0 else 0.0
    highlights = np.mean(np_image[np_image > 200]) / 255.0 if np_image[np_image > 200].size > 0 else 1.0
    whites = np.mean(np_image[np_image > 230]) / 255.0 if np_image[np_image > 230].size > 0 else 1.0
    blacks = np.mean(np_image[np_image < 30]) / 255.0 if np_image[np_image < 30].size > 0 else 0.0
    
    return {
        "temperature": temperature, "tint": tint, "exposure": exposure, "contrast": contrast,
        "saturation": saturation, "vibrance": vibrance, "highlights": highlights, "shadows": shadows,
        "whites": whites, "blacks": blacks
    }

def compute_trait_scores(current_values, ideal_values):
    scores = {}
    weight = {"temperature": 20, "tint": 20, "exposure": 40, "contrast": 40, "saturation": 20, "vibrance": 20,
              "highlights": 20, "shadows": 20, "whites": 20, "blacks": 20}  
    
    for key in current_values:
        diff = abs(current_values[key] - ideal_values[key])
        scores[key] = max(0, min(100, round(100 - (weight.get(key, 20) * diff))))  
    
    return scores

def analyze_image(image_path):
    """Analyzes an image and returns computed trait scores."""
    
    # Classify the image
    category = classify_image(image_path)

    # Get ideal values for the detected category
    ideal_values = get_ideal_values(category)

    # Compute current image trait values
    current_values = compute_current_values(image_path)

    # Compute scores based on differences from ideal values
    trait_scores = compute_trait_scores(current_values, ideal_values)

    return trait_scores  # Returns a dictionary of scores





