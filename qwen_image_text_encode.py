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
                "vae": ("VAE",),
            }
        }

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "encode"
    CATEGORY = "conditioning"

    def encode(self, text, clip, image=None, vae=None):
        tokens = clip.tokenize(text)
        cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
        result = [[cond, {"pooled_output": pooled}]]

        if image is not None:
            # Caminho semantico (VL): passa imagem para o encoder Qwen2.5-VL
            result[0][1]["reference_image"] = image

            if vae is not None:
                # Caminho de aparencia (VAE): gera reference_latents para o modelo
                # Redimensiona para ~1024x1024 antes de encodar
                t = image.movedim(-1, 1)  # B H W C -> B C H W
                h, w = t.shape[2], t.shape[3]
                target_area = 1024 * 1024
                scale = (target_area / (h * w)) ** 0.5
                th = max(16, round(h * scale / 8) * 8)
                tw = max(16, round(w * scale / 8) * 8)
                if th != h or tw != w:
                    t = torch.nn.functional.interpolate(
                        t, size=(th, tw), mode='bilinear', align_corners=False
                    )
                resized = t.movedim(1, -1)  # B C H W -> B H W C
                latent = vae.encode(resized[:, :, :, :3])
                result[0][1]["reference_latents"] = [latent]

        return (result,)

NODE_CLASS_MAPPINGS = {"QwenImageTextEncode": QwenImageTextEncode}
NODE_DISPLAY_NAME_MAPPINGS = {"QwenImageTextEncode": "Qwen Image Text Encode"}
