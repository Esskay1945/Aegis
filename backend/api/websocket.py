from fastapi import WebSocket
from typing import List, Dict, Any
import json
import logging

logger = logging.getLogger("aegis_ws")

class WebSocketManager:
    """Manages active WebSocket connections from SOC dashboards and broadcasts live telemetry."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket client connected. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"WebSocket client disconnected. Total: {len(self.active_connections)}")

    async def broadcast(self, message_type: str, data: Any):
        if not self.active_connections:
            return

        payload = {
            "type": message_type,
            "data": data
        }
        serialized = json.dumps(payload, default=str)
        
        dead_connections = []
        for connection in self.active_connections:
            try:
                await connection.send_text(serialized)
            except Exception:
                dead_connections.append(connection)

        for dead in dead_connections:
            self.disconnect(dead)

ws_manager = WebSocketManager()
