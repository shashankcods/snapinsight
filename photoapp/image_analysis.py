import torch
import clip
from PIL import Image
import numpy as np
import cv2



def classify_image(image_path):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device)
    
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    categories = [
    # General Environments
    "daylight scene", "moonlit night", "indoor", "portrait", "sunset",
    "foggy", "landscape", "urban", "macro", "underwater",

    # Nature & Outdoor
    "mountains", "sea/ocean", "rivers/lakes", "desert", "forest", "snowy landscape",
    "countryside", "waterfall", "cave", "volcanic landscape",

    # Sky & Space
    "space", "stars and galaxies", "northern lights", "thunderstorm",

    # Specialty Photography
    "wildlife", "bird photography", "astrophotography", "fireworks",
    "concert photography", "long exposure", "black and white photography",

    # Architecture & Urban Scenes
    "historic architecture", "modern skyscrapers", "street photography",
    "abandoned buildings", "traditional Asian architecture",

    # Art & Abstract
    "high contrast", "minimalist", "moody dark tones", "pastel aesthetic",
    "golden hour", "blue hour", "cinematic look",

    # Vehicles & Technology
    "automotive photography", "aircraft photography", "sci-fi themed photography",
    "industrial photography", "neon lights and cyberpunk",

    # People & Lifestyle
    "candid street portrait", "studio photography", "silhouette photography",
    "festival and celebrations", "sports photography",
]

    
    text_inputs = torch.cat([clip.tokenize(f"a photo of a {c}") for c in categories]).to(device)
    
    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text_inputs)
        similarity = (image_features @ text_features.T).softmax(dim=-1)
    
    category_idx = similarity.argmax().item()
    return categories[category_idx]

def get_ideal_values(image_category):
    ideal_values = {
    # General Environments
    "daylight scene": {"temperature": 1.0, "tint": 1.0, "exposure": 1.0, "contrast": 1.0, "highlights": 1.0, "shadows": 1.0, "whites": 1.0, "blacks": 1.0, "vibrance": 1.0, "saturation": 1.0},
    "moonlit night": {"temperature": 0.8, "tint": 0.9, "exposure": 0.7, "contrast": 1.2, "highlights": 0.6, "shadows": 0.5, "whites": 0.7, "blacks": 0.8, "vibrance": 0.7, "saturation": 0.7},
    "indoor": {"temperature": 1.1, "tint": 1.0, "exposure": 0.9, "contrast": 1.1, "highlights": 1.0, "shadows": 0.9, "whites": 1.0, "blacks": 1.0, "vibrance": 0.9, "saturation": 0.9},
    "portrait": {"temperature": 1.0, "tint": 1.0, "exposure": 1.1, "contrast": 1.0, "highlights": 1.1, "shadows": 1.0, "whites": 1.1, "blacks": 1.0, "vibrance": 1.0, "saturation": 1.0},
    "sunset": {"temperature": 1.3, "tint": 1.2, "exposure": 0.8, "contrast": 1.2, "highlights": 1.2, "shadows": 0.8, "whites": 1.1, "blacks": 0.9, "vibrance": 1.2, "saturation": 1.2},
    "foggy": {"temperature": 0.9, "tint": 1.0, "exposure": 0.7, "contrast": 0.5, "highlights": 0.6, "shadows": 0.7, "whites": 0.6, "blacks": 0.6, "vibrance": 0.6, "saturation": 0.6},
    "landscape": {"temperature": 1.0, "tint": 1.0, "exposure": 1.0, "contrast": 1.1, "highlights": 1.0, "shadows": 0.9, "whites": 1.0, "blacks": 1.0, "vibrance": 1.1, "saturation": 1.1},
    "urban": {"temperature": 1.0, "tint": 1.0, "exposure": 1.0, "contrast": 1.2, "highlights": 1.0, "shadows": 0.8, "whites": 1.0, "blacks": 0.9, "vibrance": 1.0, "saturation": 1.0},
    "macro": {"temperature": 1.0, "tint": 1.0, "exposure": 1.0, "contrast": 1.1, "highlights": 1.0, "shadows": 0.9, "whites": 1.0, "blacks": 1.0, "vibrance": 1.1, "saturation": 1.1},
    "underwater": {"temperature": 0.7, "tint": 1.1, "exposure": 0.8, "contrast": 1.0, "highlights": 0.7, "shadows": 0.6, "whites": 0.8, "blacks": 0.7, "vibrance": 0.8, "saturation": 0.8},

    # Nature & Outdoor
    "mountains": {"temperature": 1.0, "tint": 1.0, "exposure": 1.0, "contrast": 1.1, "highlights": 1.0, "shadows": 0.9, "whites": 1.0, "blacks": 1.0, "vibrance": 1.1, "saturation": 1.1},
    "sea/ocean": {"temperature": 0.9, "tint": 1.0, "exposure": 1.0, "contrast": 1.0, "highlights": 1.0, "shadows": 0.8, "whites": 1.0, "blacks": 0.9, "vibrance": 1.0, "saturation": 1.0},
    "rivers/lakes": {"temperature": 0.9, "tint": 1.0, "exposure": 1.0, "contrast": 1.0, "highlights": 1.0, "shadows": 0.8, "whites": 1.0, "blacks": 0.9, "vibrance": 1.0, "saturation": 1.0},
    "desert": {"temperature": 1.2, "tint": 1.0, "exposure": 1.1, "contrast": 1.1, "highlights": 1.1, "shadows": 0.8, "whites": 1.1, "blacks": 0.9, "vibrance": 1.1, "saturation": 1.1},
    "forest": {"temperature": 0.9, "tint": 1.0, "exposure": 0.9, "contrast": 1.1, "highlights": 0.9, "shadows": 0.8, "whites": 1.0, "blacks": 0.9, "vibrance": 1.1, "saturation": 1.1},
    "snowy landscape": {"temperature": 0.8, "tint": 1.0, "exposure": 1.1, "contrast": 1.2, "highlights": 1.1, "shadows": 0.9, "whites": 1.1, "blacks": 0.9, "vibrance": 1.0, "saturation": 1.0},
    "countryside": {"temperature": 1.0, "tint": 1.0, "exposure": 1.0, "contrast": 1.1, "highlights": 1.0, "shadows": 0.9, "whites": 1.0, "blacks": 1.0, "vibrance": 1.1, "saturation": 1.1},
    "waterfall": {"temperature": 0.9, "tint": 1.0, "exposure": 1.0, "contrast": 1.1, "highlights": 1.0, "shadows": 0.8, "whites": 1.0, "blacks": 0.9, "vibrance": 1.0, "saturation": 1.0},
    "cave": {"temperature": 0.7, "tint": 1.0, "exposure": 0.6, "contrast": 1.0, "highlights": 0.5, "shadows": 0.4, "whites": 0.6, "blacks": 0.5, "vibrance": 0.6, "saturation": 0.6},
    "volcanic landscape": {"temperature": 1.3, "tint": 1.1, "exposure": 0.9, "contrast": 1.2, "highlights": 1.1, "shadows": 0.8, "whites": 1.1, "blacks": 0.9, "vibrance": 1.2, "saturation": 1.2},

    # Sky & Space
    "space": {"temperature": 0.6, "tint": 1.0, "exposure": 0.5, "contrast": 1.2, "highlights": 0.6, "shadows": 0.4, "whites": 0.7, "blacks": 0.5, "vibrance": 0.8, "saturation": 0.8},
    "stars and galaxies": {"temperature": 0.6, "tint": 1.0, "exposure": 0.5, "contrast": 1.2, "highlights": 0.6, "shadows": 0.4, "whites": 0.7, "blacks": 0.5, "vibrance": 0.8, "saturation": 0.8},
    "northern lights": {"temperature": 0.7, "tint": 1.1, "exposure": 0.8, "contrast": 1.2, "highlights": 1.0, "shadows": 0.6, "whites": 1.0, "blacks": 0.7, "vibrance": 1.2, "saturation": 1.2},
    "thunderstorm": {"temperature": 0.8, "tint": 1.0, "exposure": 0.7, "contrast": 1.2, "highlights": 0.8, "shadows": 0.5, "whites": 0.9, "blacks": 0.6, "vibrance": 0.9, "saturation": 0.9},

    # Specialty Photography
    "wildlife": {"temperature": 1.0, "tint": 1.0, "exposure": 1.0, "contrast": 1.1, "highlights": 1.0, "shadows": 0.9, "whites": 1.0, "blacks": 1.0, "vibrance": 1.1, "saturation": 1.1},
    "bird photography": {"temperature": 1.0, "tint": 1.0, "exposure": 1.0, "contrast": 1.1, "highlights": 1.0, "shadows": 0.9, "whites": 1.0, "blacks": 1.0, "vibrance": 1.1, "saturation": 1.1},
    "astrophotography": {"temperature": 0.6, "tint": 1.0, "exposure": 0.5, "contrast": 1.2, "highlights": 0.6, "shadows": 0.4, "whites": 0.7, "blacks": 0.5, "vibrance": 0.8, "saturation": 0.8},
    "fireworks": {"temperature": 1.0, "tint": 1.0, "exposure": 0.8, "contrast": 1.2, "highlights": 1.0, "shadows": 0.6, "whites": 1.0, "blacks": 0.7, "vibrance": 1.2, "saturation": 1.2},
    "concert photography": {"temperature": 1.0, "tint": 1.0, "exposure": 0.8, "contrast": 1.2, "highlights": 1.0, "shadows": 0.6, "whites": 1.0, "blacks": 0.7, "vibrance": 1.2, "saturation": 1.2},
    "long exposure": {"temperature": 1.0, "tint": 1.0, "exposure": 0.8, "contrast": 1.2, "highlights": 1.0, "shadows": 0.6, "whites": 1.0, "blacks": 0.7, "vibrance": 1.2, "saturation": 1.2},
    "black and white photography": {"temperature": 1.0, "tint": 1.0, "exposure": 1.0, "contrast": 1.2, "highlights": 1.0, "shadows": 0.8, "whites": 1.0, "blacks": 0.9, "vibrance": 0.0, "saturation": 0.0},

    # Architecture & Urban Scenes
    "historic architecture": {"temperature": 1.0, "tint": 1.0, "exposure": 1.0, "contrast": 1.1, "highlights": 1.0, "shadows": 0.9, "whites": 1.0, "blacks": 1.0, "vibrance": 1.0, "saturation": 1.0},
    "modern skyscrapers": {"temperature": 1.0, "tint": 1.0, "exposure": 1.0, "contrast": 1.2, "highlights": 1.0, "shadows": 0.8, "whites": 1.0, "blacks": 0.9, "vibrance": 1.0, "saturation": 1.0},
    "street photography": {"temperature": 1.0, "tint": 1.0, "exposure": 1.0, "contrast": 1.1, "highlights": 1.0, "shadows": 0.9, "whites": 1.0, "blacks": 1.0, "vibrance": 1.0, "saturation": 1.0},
    "abandoned buildings": {"temperature": 0.9, "tint": 1.0, "exposure": 0.8, "contrast": 1.1, "highlights": 0.8, "shadows": 0.7, "whites": 0.9, "blacks": 0.8, "vibrance": 0.9, "saturation": 0.9},
    "traditional Asian architecture": {"temperature": 1.0, "tint": 1.0, "exposure": 1.0, "contrast": 1.1, "highlights": 1.0, "shadows": 0.9, "whites": 1.0, "blacks": 1.0, "vibrance": 1.0, "saturation": 1.0},

    # Art & Abstract
    "high contrast": {"temperature": 1.0, "tint": 1.0, "exposure": 1.0, "contrast": 1.5, "highlights": 1.2, "shadows": 0.5, "whites": 1.2, "blacks": 0.5, "vibrance": 1.2, "saturation": 1.2},
    "minimalist": {"temperature": 1.0, "tint": 1.0, "exposure": 1.0, "contrast": 1.0, "highlights": 1.0, "shadows": 1.0, "whites": 1.0, "blacks": 1.0, "vibrance": 0.5, "saturation": 0.5},
    "moody dark tones": {"temperature": 0.8, "tint": 1.0, "exposure": 0.7, "contrast": 1.2, "highlights": 0.6, "shadows": 0.5, "whites": 0.7, "blacks": 0.8, "vibrance": 0.7, "saturation": 0.7},
    "pastel aesthetic": {"temperature": 1.0, "tint": 1.0, "exposure": 1.0, "contrast": 0.8, "highlights": 1.0, "shadows": 0.9, "whites": 1.0, "blacks": 1.0, "vibrance": 0.8, "saturation": 0.8},
    "golden hour": {"temperature": 1.3, "tint": 1.2, "exposure": 0.8, "contrast": 1.2, "highlights": 1.2, "shadows": 0.8, "whites": 1.1, "blacks": 0.9, "vibrance": 1.2, "saturation": 1.2},
    "blue hour": {"temperature": 0.7, "tint": 1.1, "exposure": 0.8, "contrast": 1.1, "highlights": 0.9, "shadows": 0.7, "whites": 1.0, "blacks": 0.8, "vibrance": 0.9, "saturation": 0.9},
    "cinematic look": {"temperature": 1.0, "tint": 1.0, "exposure": 0.8, "contrast": 1.2, "highlights": 1.0, "shadows": 0.6, "whites": 1.0, "blacks": 0.7, "vibrance": 1.2, "saturation": 1.2},

    # Vehicles & Technology
    "automotive photography": {"temperature": 1.0, "tint": 1.0, "exposure": 1.0, "contrast": 1.2, "highlights": 1.0, "shadows": 0.8, "whites": 1.0, "blacks": 0.9, "vibrance": 1.0, "saturation": 1.0},
    "aircraft photography": {"temperature": 1.0, "tint": 1.0, "exposure": 1.0, "contrast": 1.2, "highlights": 1.0, "shadows": 0.8, "whites": 1.0, "blacks": 0.9, "vibrance": 1.0, "saturation": 1.0},
    "sci-fi themed photography": {"temperature": 0.7, "tint": 1.1, "exposure": 0.8, "contrast": 1.2, "highlights": 1.0, "shadows": 0.6, "whites": 1.0, "blacks": 0.7, "vibrance": 1.2, "saturation": 1.2},
    "industrial photography": {"temperature": 0.9, "tint": 1.0, "exposure": 0.8, "contrast": 1.2, "highlights": 0.9, "shadows": 0.7, "whites": 1.0, "blacks": 0.8, "vibrance": 0.9, "saturation": 0.9},
    "neon lights and cyberpunk": {"temperature": 0.7, "tint": 1.1, "exposure": 0.8, "contrast": 1.2, "highlights": 1.0, "shadows": 0.6, "whites": 1.0, "blacks": 0.7, "vibrance": 1.2, "saturation": 1.2},

    # People & Lifestyle
    "candid street portrait": {"temperature": 1.0, "tint": 1.0, "exposure": 1.0, "contrast": 1.1, "highlights": 1.0, "shadows": 0.9, "whites": 1.0, "blacks": 1.0, "vibrance": 1.0, "saturation": 1.0},
    "studio photography": {"temperature": 1.0, "tint": 1.0, "exposure": 1.0, "contrast": 1.1, "highlights": 1.0, "shadows": 0.9, "whites": 1.0, "blacks": 1.0, "vibrance": 1.0, "saturation": 1.0},
    "silhouette photography": {"temperature": 1.0, "tint": 1.0, "exposure": 0.8, "contrast": 1.2, "highlights": 1.0, "shadows": 0.6, "whites": 1.0, "blacks": 0.7, "vibrance": 1.0, "saturation": 1.0},
    "festival and celebrations": {"temperature": 1.0, "tint": 1.0, "exposure": 1.0, "contrast": 1.2, "highlights": 1.0, "shadows": 0.8, "whites": 1.0, "blacks": 0.9, "vibrance": 1.2, "saturation": 1.2},
    "sports photography": {"temperature": 1.0, "tint": 1.0, "exposure": 1.0, "contrast": 1.2, "highlights": 1.0, "shadows": 0.8, "whites": 1.0, "blacks": 0.9, "vibrance": 1.0, "saturation": 1.0},
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
    weight = {
        "temperature": 15, "tint": 15, "exposure": 25, "contrast": 25,  # Lowered exposure & contrast weight
        "saturation": 15, "vibrance": 15, "highlights": 15, "shadows": 15, 
        "whites": 15, "blacks": 15
    }

    expected_variation = {
        "temperature": 0.5, "tint": 0.4, "exposure": 1.2, "contrast": 1.0,  # Increased expected variation
        "saturation": 0.6, "vibrance": 0.6, "highlights": 0.7, "shadows": 0.7, 
        "whites": 0.8, "blacks": 0.8
    }

    for key in current_values:
        diff = abs(current_values[key] - ideal_values[key])
        norm_diff = diff / (expected_variation.get(key, 0.5) + 1e-6)

        # Adjusted log penalty (less aggressive for exposure & contrast)
        penalty = np.log1p(norm_diff * 5) * weight.get(key, 20)  

        # Base score calculation
        raw_score = max(0, 100 - penalty)
        scores[key] = min(100, round(raw_score))

        # Adjust lower score limits more leniently for exposure & contrast
        if key in ["exposure", "contrast"]:
            if norm_diff > 1.5:
                scores[key] = min(scores[key], 60)  # Was 50
            elif norm_diff > 1.0:
                scores[key] = min(scores[key], 75)  # Was 65

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





