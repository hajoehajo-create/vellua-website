import urllib.request
from PIL import Image
import os

url = "https://i.scdn.co/image/ab67616d0000b273171cb89ac73e7ad198048ef7"
favicon_path = "favicon.png"

def create_favicon():
    try:
        print(f"Downloading cover from {url}...")
        urllib.request.urlretrieve(url, "temp_cover.jpg")
        
        print("Creating favicon.png...")
        img = Image.open("temp_cover.jpg")
        
        # Crop and resize to 64x64
        size = (64, 64)
        img.thumbnail(size)
        
        # If not square, crop it
        width, height = img.size
        if width != height:
            new_side = min(width, height)
            left = (width - new_side) / 2
            top = (height - new_side) / 2
            right = (width + new_side) / 2
            bottom = (height + new_side) / 2
            img = img.crop((left, top, right, bottom))
            img = img.resize(size, Image.LANCZOS)
            
        img.save(favicon_path, "PNG")
        print(f"Favicon saved to {favicon_path}")
        
        # Cleanup
        os.remove("temp_cover.jpg")
    except Exception as e:
        print(f"Error creating favicon: {e}")

if __name__ == "__main__":
    create_favicon()
