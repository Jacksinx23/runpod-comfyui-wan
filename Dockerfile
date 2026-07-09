FROM runpod/worker-comfyui:5.8.6-base

# Copia custom nodes próprios do repo
COPY load_image_from_url.py /comfyui/custom_nodes/load_image_from_url.py
COPY qwen_image_text_encode.py /comfyui/custom_nodes/qwen_image_text_encode.py

COPY extra_model_paths.yaml /comfyui/extra_model_paths.yaml
