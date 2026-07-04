FROM runpod/worker-comfyui:5.8.6-base

COPY extra_model_paths.yaml /comfyui/extra_model_paths.yaml
COPY link-models.sh /link-models.sh
RUN chmod +x /link-models.sh

ENV PRE_START_SCRIPT=/link-models.sh
