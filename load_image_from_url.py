import requests
from PIL import Image
from io import BytesIO
import torch
import numpy as np

class LoadImageFromURL:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"url": ("STRING", {"default": ""})}}
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "load"
    CATEGORY = "image"

    def load(self, url):
        response = requests.get(url, timeout=10)
        img = Image.open(BytesIO(response.content)).convert("RGB")
        img = np.array(img).astype(np.float32) / 255.0
        return (torch.from_numpy(img).unsqueeze(0),)

NODE_CLASS_MAPPINGS = {"LoadImageFromURL": LoadImageFromURL}
NODE_DISPLAY_NAME_MAPPINGS = {"LoadImageFromURL": "Load Image From URL"}
