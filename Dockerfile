FROM runpod/worker-comfyui:5.8.6-base

# Custom Scripts
RUN cd /comfyui/custom_nodes && \
    git clone https://github.com/pythongosssss/ComfyUI-Custom-Scripts.git && \
    cd ComfyUI-Custom-Scripts && pip install -r requirements.txt 2>/dev/null || true

# KJNodes
RUN cd /comfyui/custom_nodes && \
    git clone https://github.com/kijai/ComfyUI-KJNodes.git && \
    cd ComfyUI-KJNodes && pip install -r requirements.txt 2>/dev/null || true

# ComfyUI-Impact-Pack
RUN cd /comfyui/custom_nodes && \
    git clone https://github.com/ltdrdata/ComfyUI-Impact-Pack.git && \
    cd ComfyUI-Impact-Pack && pip install -r requirements.txt 2>/dev/null || true

COPY load_image_from_url.py /comfyui/custom_nodes/load_image_from_url.py
COPY extra_model_paths.yaml /comfyui/extra_model_paths.yaml
