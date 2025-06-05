from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.lipsync_service import process_lipsync_ws

router = APIRouter()

@router.websocket("/ws/lipsync")
async def lipsync_ws(websocket: WebSocket):
    await process_lipsync_ws(websocket)