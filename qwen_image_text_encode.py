import torch

class QwenImageTextEncode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "conditioning": ("CONDITIONING",),
                "clip": ("CLIP",),
            },
            "optional": {
                "image": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "encode"
    CATEGORY = "conditioning"

    def encode(self, conditioning, clip, image=None):
        # Se não tem imagem, retorna o conditioning original
        if image is None:
            return (conditioning,)

        # Tenta usar o clip para encodar com a imagem
        try:
            tokens = clip.tokenize("")
            if hasattr(clip, 'encode_from_tokens_scheduled'):
                cond, pooled = clip.encode_from_tokens_scheduled(tokens)
            else:
                cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)

            # Injeta a imagem no conditioning
            result = []
            for c in conditioning:
                n = [c[0], c[1].copy() if isinstance(c[1], dict) else {}]
                if image is not None:
                    n[1]["reference_image"] = image
                result.append(n)
            return (result,)
        except Exception:
            return (conditioning,)


NODE_CLASS_MAPPINGS = {
    "QwenImageTextEncode": QwenImageTextEncode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "QwenImageTextEncode": "Qwen Image Text Encode"
}
