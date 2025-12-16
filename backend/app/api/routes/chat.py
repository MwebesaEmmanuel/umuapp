from __future__ import annotations

import asyncio
import json
from datetime import datetime
from collections import defaultdict

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, status
from jose import JWTError
from sqlmodel import Session, select

from app.api.deps import CurrentUser, DbSession, get_current_user
from app.core.security import decode_token
from app.db.engine import get_engine
from app.models.chat import ChatMessage, ChatRoom
from app.schemas.chat import ChatMessagePublic, ChatRoomCreate, ChatRoomPublic


router = APIRouter()


class RoomConnectionManager:
    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._rooms: dict[int, set[WebSocket]] = defaultdict(set)

    async def connect(self, room_id: int, websocket: WebSocket) -> None:
        async with self._lock:
            self._rooms[room_id].add(websocket)

    async def disconnect(self, room_id: int, websocket: WebSocket) -> None:
        async with self._lock:
            if room_id in self._rooms:
                self._rooms[room_id].discard(websocket)
                if not self._rooms[room_id]:
                    del self._rooms[room_id]

    async def broadcast(self, room_id: int, payload: dict) -> None:
        message = json.dumps(payload)
        async with self._lock:
            sockets = list(self._rooms.get(room_id, set()))
        for ws in sockets:
            try:
                await ws.send_text(message)
            except Exception:
                pass


manager = RoomConnectionManager()


@router.get("/rooms", response_model=list[ChatRoomPublic])
def list_rooms(db: DbSession) -> list[ChatRoomPublic]:
    rooms = db.exec(select(ChatRoom).order_by(ChatRoom.created_at.desc())).all()
    return [ChatRoomPublic.model_validate(r.model_dump()) for r in rooms]


@router.post("/rooms", response_model=ChatRoomPublic)
def create_room(payload: ChatRoomCreate, db: DbSession, user: CurrentUser) -> ChatRoomPublic:
    room = ChatRoom(name=payload.name, is_public=payload.is_public)
    db.add(room)
    db.commit()
    db.refresh(room)
    return ChatRoomPublic.model_validate(room.model_dump())


@router.get("/rooms/{room_id}/messages", response_model=list[ChatMessagePublic])
def list_room_messages(room_id: int, db: DbSession, limit: int = 50) -> list[ChatMessagePublic]:
    limit = max(1, min(200, limit))
    rows = db.exec(
        select(ChatMessage)
        .where(ChatMessage.room_id == room_id)
        .order_by(ChatMessage.sent_at.desc())
        .limit(limit)
    ).all()
    rows = list(reversed(rows))
    return [ChatMessagePublic.model_validate(r.model_dump()) for r in rows]


def _user_from_ws_token(db: DbSession, token: str):
    try:
        payload = decode_token(token)
        subject = payload.get("sub")
        if not subject:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return get_current_user(db=db, token=token)


@router.websocket("/ws/rooms/{room_id}")
async def ws_room(websocket: WebSocket, room_id: int):
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=4401)
        return

    engine = get_engine()
    with Session(engine) as db:
        try:
            user = _user_from_ws_token(db, token)
        except HTTPException:
            await websocket.close(code=4401)
            return

        room = db.exec(select(ChatRoom).where(ChatRoom.id == room_id)).one_or_none()
        if not room:
            await websocket.close(code=4404)
            return

    await websocket.accept()
    await manager.connect(room_id, websocket)
    await manager.broadcast(
        room_id,
        {
            "type": "system",
            "message": f"{user.email} joined",
            "at": datetime.utcnow().isoformat(),
        },
    )

    try:
        with Session(engine) as db:
            while True:
                data = await websocket.receive_text()
                message_text = data.strip()
                if not message_text:
                    continue
                if len(message_text) > 2000:
                    await websocket.send_text(json.dumps({"type": "error", "message": "Too long"}))
                    continue

                msg = ChatMessage(room_id=room_id, sender_user_id=user.id, body=message_text)
                db.add(msg)
                db.commit()
                db.refresh(msg)

                await manager.broadcast(
                    room_id,
                    {
                        "type": "message",
                        "id": msg.id,
                        "room_id": msg.room_id,
                        "sender_user_id": msg.sender_user_id,
                        "body": msg.body,
                        "sent_at": msg.sent_at.isoformat(),
                    },
                )
    except WebSocketDisconnect:
        await manager.disconnect(room_id, websocket)
        await manager.broadcast(
            room_id,
            {
                "type": "system",
                "message": f"{user.email} left",
                "at": datetime.utcnow().isoformat(),
            },
        )
        return
