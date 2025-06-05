import base64
import json
import asyncio
import websockets
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger("lipsync_test")

WS_URI = "ws://localhost:8000/ws/lipsync"

def encode_file_to_datauri(filepath, mime):
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    with open(filepath, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{b64}"

async def lipsync_ws_test(image_path, audio_path, out_path="output.mp4"):
    img_ext = os.path.splitext(image_path)[1].lower()
    audio_ext = os.path.splitext(audio_path)[1].lower()
    img_mime = "image/png" if img_ext == ".png" else "image/jpeg"
    audio_mime = "audio/wav" if audio_ext == ".wav" else "audio/mp3"

    img_data_uri = encode_file_to_datauri(image_path, img_mime)
    audio_data_uri = encode_file_to_datauri(audio_path, audio_mime)

    payload = {"base64_image": img_data_uri, "base64_audio": audio_data_uri}

    async with websockets.connect(WS_URI) as ws:
        logger.info("Sending data to server...")
        await ws.send(json.dumps(payload))
        while True:
            try:
                response = await asyncio.wait_for(ws.recv(), timeout=60)
            except asyncio.TimeoutError:
                logger.error("Timeout while waiting for server response.")
                break
            data = json.loads(response)
            if data.get("status") == "done":
                logger.info("Received result successfully.")
                video_data = data["video_base64"].split(",")[1]
                with open(out_path, "wb") as vf:
                    vf.write(base64.b64decode(video_data))
                logger.info(f"Saved output video: {out_path}")
                break
            else:
                logger.error(f"Server error: {data.get('detail')}")
                break

if __name__ == "__main__":
    IMAGE_PATH = "andrew-ng.png"
    AUDIO_PATH = "test.wav"
    OUT_PATH = "output.mp4"

    try:
        asyncio.run(lipsync_ws_test(IMAGE_PATH, AUDIO_PATH, OUT_PATH))
    except Exception as e:
        logger.error(f"Test failed: {e}")