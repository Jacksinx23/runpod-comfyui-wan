#!/bin/bash
echo "[link-models] Iniciando..."

COMFY=/comfyui/models

# Detecta onde o volume está montado
VOLUME=""
for candidate in /runpod-volume/ComfyUI/models /runpod-volume/models /workspace/ComfyUI/models /workspace/models; do
  if [ -d "$candidate" ]; then
    VOLUME=$candidate
    echo "[link-models] Volume encontrado em: $VOLUME"
    break
  fi
done

if [ -z "$VOLUME" ]; then
  echo "[link-models] AVISO: nenhum volume encontrado, pulando symlinks"
  exit 0
fi

for dir in diffusion_models text_encoders vae loras clip_vision upscale_models checkpoints; do
  if [ -d "$VOLUME/$dir" ]; then
    mkdir -p "$COMFY/$dir"
    for f in "$VOLUME/$dir"/*; do
      [ -e "$f" ] || continue
      fname=$(basename "$f")
      ln -sf "$f" "$COMFY/$dir/$fname" 2>/dev/null || true
      echo "[link-models] $dir/$fname"
    done
  fi
done

echo "[link-models] Concluido."
