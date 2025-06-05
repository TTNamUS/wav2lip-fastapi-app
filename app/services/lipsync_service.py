import base64
import logging
from app.services.file_utils import save_temp_file, remove_files
from app.models.wav2lip_inference import run_wav2lip
from fastapi import WebSocketDisconnect

logger = logging.getLogger("lipsync_service")

async def process_lipsync_ws(websocket):
    await websocket.accept()
    try:
        data = await websocket.receive_json()
        base64_image = data.get("base64_image")
        base64_audio = data.get("base64_audio")
        if not base64_image or not base64_audio:
            await websocket.send_json({"status": "error", "detail": "Missing base64_image or base64_audio"})
            return

        temp_img_path = save_temp_file(base64_image, "img")
        temp_audio_path = save_temp_file(base64_audio, "audio")

        try:
            output_video_path = run_wav2lip(temp_img_path, temp_audio_path)
        except Exception as e:
            await websocket.send_json({"status": "error", "detail": str(e)})
            remove_files([temp_img_path, temp_audio_path])
            return

        with open(output_video_path, "rb") as vf:
            video_b64 = base64.b64encode(vf.read()).decode("utf-8")
        await websocket.send_json({
            "status": "done",
            "video_base64": f"data:video/mp4;base64,{video_b64}"
        })
        await websocket.close()
        remove_files([temp_img_path, temp_audio_path])
        remove_files([output_video_path], remove_dirs=True)
    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"Error while processing WS: {e}")
        try:
            await websocket.send_json({"status": "error", "detail": str(e)})
        except:
            pass