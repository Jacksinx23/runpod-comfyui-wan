import torch

class QwenImageTextEncode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
                "clip": ("CLIP",),
            },
            "optional": {
                "image": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "encode"
    CATEGORY = "conditioning"

    def encode(self, text, clip, image=None):
        tokens = clip.tokenize(text)
        cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
        result = [[cond, {"pooled_output": pooled}]]
        if image is not None:
            result[0][1]["reference_image"] = image
        return (result,)

NODE_CLASS_MAPPINGS = {
    "QwenImageTextEncode": QwenImageTextEncode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "QwenImageTextEncode": "Qwen Image Text Encode"
}
