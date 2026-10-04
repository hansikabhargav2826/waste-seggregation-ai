# fix_images.py
import os
from PIL import Image

DATASET_DIR = "dataset"
IMG_SIZE = (224, 224)

def clean_images():
    for category in os.listdir(DATASET_DIR):
        folder = os.path.join(DATASET_DIR, category)
        if not os.path.isdir(folder):
            continue
        for file in os.listdir(folder):
            path = os.path.join(folder, file)
            try:
                img = Image.open(path)
                # Convert to RGB (3 channels)
                if img.mode != "RGB":
                    img = img.convert("RGB")
                # Resize to standard size
                img = img.resize(IMG_SIZE, Image.Resampling.LANCZOS)
                # Save back as JPEG
                img.save(path, "JPEG")
            except Exception as e:
                print(f"❌ Removing bad file: {path}")
                os.remove(path)

if __name__ == "__main__":
    clean_images()
    print("✅ Dataset cleaned and standardized!")
