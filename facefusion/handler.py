import base64
import os
import subprocess
import tempfile
import uuid

import runpod


def _write_b64(b64: str, path: str):
    with open(path, "wb") as f:
        f.write(base64.b64decode(b64))


def handler(event):
    inp = event.get("input", {}) or {}
    src_b64 = inp.get("source_image")
    tgt_b64 = inp.get("target_image")
    if not src_b64 or not tgt_b64:
        return {"error": "source_image e target_image (base64) sao obrigatorios"}

    # opcoes ajustaveis
    enhancer_model = inp.get("face_enhancer_model", "gfpgan_1.4")
    enhancer_blend = int(inp.get("face_enhancer_blend", 80))   # 0-100
    swapper_model = inp.get("face_swapper_model", "inswapper_128_fp16")

    work = tempfile.mkdtemp(prefix="ff_")
    src = os.path.join(work, "src.png")
    tgt = os.path.join(work, "tgt.png")
    out = os.path.join(work, f"out_{uuid.uuid4().hex}.png")

    try:
        _write_b64(src_b64, src)
        _write_b64(tgt_b64, tgt)
    except Exception as e:
        return {"error": f"base64 invalido: {e}"}

    cmd = [
        "python3", "facefusion.py", "headless-run",
        "--source-paths", src,
        "--target-path", tgt,
        "--output-path", out,
        "--processors", "face_swapper", "face_enhancer",
        "--face-swapper-model", swapper_model,
        "--face-enhancer-model", enhancer_model,
        "--face-enhancer-blend", str(enhancer_blend),
        "--execution-providers", "cuda",
        "--output-image-quality", "100",
    ]

    r = subprocess.run(cmd, cwd="/app", capture_output=True, text=True)

    if not os.path.exists(out):
        return {
            "error": "facefusion falhou",
            "stderr": (r.stderr or "")[-2500:],
            "stdout": (r.stdout or "")[-1000:],
        }

    with open(out, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()

    return {"image": img_b64}


runpod.serverless.start({"handler": handler})
