FROM runpod/worker-comfyui:5.8.6-base

# Deps de análise facial do PuLID
RUN pip install --no-cache-dir insightface onnxruntime-gpu facexlib timm einops ftfy

# Custom nodes: PuLID-Flux + utilidades
WORKDIR /comfyui/custom_nodes
RUN git clone https://github.com/balazik/ComfyUI-PuLID-Flux.git || true
RUN git clone https://github.com/cubiq/ComfyUI_essentials.git || true

# aponta os modelos pro volume montado em /runpod-volume
COPY extra_model_paths.yaml /comfyui/extra_model_paths.yaml

WORKDIR /comfyui
