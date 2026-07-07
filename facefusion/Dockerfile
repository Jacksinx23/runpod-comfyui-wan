FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y \
    python3 python3-pip git ffmpeg curl libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# FaceFusion 3.x (pin a stable tag)
RUN git clone https://github.com/facefusion/facefusion.git --branch 3.1.1 .

# Deps + onnxruntime CUDA
RUN pip3 install --upgrade pip && \
    python3 install.py --onnxruntime cuda --skip-conda

# Baixa os modelos (face_swapper + face_enhancer + detectores) na imagem
RUN python3 facefusion.py force-download

RUN pip3 install runpod

COPY handler.py /app/handler.py

CMD ["python3", "-u", "handler.py"]
