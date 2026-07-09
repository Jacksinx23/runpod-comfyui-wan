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
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, timeout=30, headers=headers)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content)).convert("RGB")
        img_array = np.array(img).astype(np.float32) / 255.0
        img_tensor = torch.from_numpy(img_array).unsqueeze(0)
        return (img_tensor,)

NODE_CLASS_MAPPINGS = {"LoadImageFromURL": LoadImageFromURL}
NODE_DISPLAY_NAME_MAPPINGS = {"LoadImageFromURL": "Load Image From URL"}
