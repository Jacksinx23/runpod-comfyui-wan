FROM runpod/worker-comfyui:5.8.6-base

RUN cd /comfyui/custom_nodes && \
    git clone https://github.com/pythongosssss/ComfyUI-Custom-Scripts.git && \
    cd ComfyUI-Custom-Scripts && pip install -r requirements.txt 2>/dev/null || true

COPY extra_model_paths.yaml /comfyui/extra_model_paths.yaml
