import os
import subprocess
import uuid
import logging
from pathlib import Path

logger = logging.getLogger("wav2lip_inference")
logging.basicConfig(level=logging.INFO)

INFERENCE_SCRIPT = str(Path(__file__).parent/ "Wav2Lip"/ "inference.py")
CHECKPOINT_PATH = str(Path(__file__).parent.parent.parent/ "checkpoints" / "Wav2Lip.pth")
OUTPUT_DIR_TEMP = str(Path(__file__).parent/ "Wav2Lip"/ "result")
os.makedirs(OUTPUT_DIR_TEMP, exist_ok=True)

def run_wav2lip(face_image_path: str, audio_path: str) -> str:
    output_fname = f"{uuid.uuid4().hex}.mp4"
    output_path = os.path.join(OUTPUT_DIR_TEMP, output_fname)

    cmd = [
        "uv",
        "run",
        INFERENCE_SCRIPT,
        "--checkpoint_path", CHECKPOINT_PATH,
        "--face", face_image_path,
        "--audio", audio_path,
        "--outfile", output_path
    ]

    logger.info(f"Running Wav2Lip: {' '.join(cmd)}")
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        logger.info("Wav2Lip inference completed")
    except subprocess.CalledProcessError as e:
        logger.error(f"Wav2Lip inference error: {e.stderr.decode()}")
        raise RuntimeError(f"Wav2Lip inference failed: {e.stderr.decode()}")
    return output_path