#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2024-03-30 09:51:30
# @Author  : Dahir Muhammad Dahir (dahirmuhammad3@gmail.com)
# @Link    : link
# @Version : 1.0.0


from fastapi import WebSocket
from pydantic import BaseModel, ConfigDict
from enum import Enum
from datetime import datetime


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, chat_room_id: str = ""):
        await websocket.accept()
        if chat_room_id:
            self.add_connection(websocket, chat_room_id)

    def add_connection(self, websocket: WebSocket, chat_room_id: str):
        if chat_room_id not in self.active_connections:
            self.active_connections[chat_room_id] = []
        # only append if the connection is not already in the list
        if websocket not in self.active_connections[chat_room_id]:
            self.active_connections[chat_room_id].append(websocket)

    def disconnect(self, websocket: WebSocket, chat_room_id: str):
        if chat_room_id in self.active_connections:
            try:
                self.active_connections[chat_room_id].remove(websocket)
            except ValueError:
                pass
            if not self.active_connections[chat_room_id]:
                del self.active_connections[chat_room_id]

    async def send_to_self(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, chat_room_id: str):
        for connection in self.active_connections.get(chat_room_id, []):
            await connection.send_text(message)

    async def broadcast_to_others(
        self, message: str, chat_room_id: str, sender: WebSocket
    ):
        for connection in self.active_connections.get(chat_room_id, []):
            # await connection.send_text(message)
            if connection != sender:
                await connection.send_text(message)

    async def broadcast_bytes(self, message: bytes, chat_room_id: str):
        for connection in self.active_connections.get(chat_room_id, []):
            await connection.send_bytes(message)


chat_manager = ConnectionManager()


class PacketType(str, Enum):
    message_send = "message-send"
    message_receive = "message-receive"
    recent_messages = "recent-messages"
    list_message_request = "list-message-request"
    list_message_response = "list-message-response"
    chat_join = "chat-join"
    chat_join_notify = "chat-join-notify"
    chat_leave = "chat-leave"
    typing = "typing"
    typing_notify = "typing-notify"


class MyBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class MessageSendPayload(BaseModel):
    message: str
    room_id: str


class MessageSendPacket(BaseModel):
    type: PacketType = PacketType.message_send
    payload: MessageSendPayload


class MessageReceivePayload(MyBaseModel):
    room_id: str
    sender_id: str
    message: str
    timestamp: datetime = datetime.now()


class MessageReceivePacket(BaseModel):
    type: PacketType = PacketType.message_receive
    payload: MessageReceivePayload


class RecentMessage(MyBaseModel):
    sender_id: str
    message: str
    timestamp: datetime = datetime.now()


class RecentRoomMessage(BaseModel):
    room_id: str
    messages: list[RecentMessage]


class RecentMessagePayload(BaseModel):
    recent_messages: list[RecentRoomMessage]


class RecentMessagePacket(BaseModel):
    type: PacketType = PacketType.recent_messages
    payload: RecentMessagePayload


class ChatJoinPayload(BaseModel):
    notice: str = "join"


class ChatJoinPacket(BaseModel):
    type: PacketType = PacketType.chat_join
    payload: ChatJoinPayload


class ChatJoinNotifyPayload(BaseModel):
    participant_id: str


class ChatJoinNotifyPacket(BaseModel):
    type: PacketType = PacketType.chat_join_notify
    payload: ChatJoinNotifyPayload


class ChatLeavePayload(BaseModel):
    participant_id: str


class ChatLeavePacket(BaseModel):
    type: PacketType = PacketType.chat_leave
    payload: ChatLeavePayload


class TypingPayload(BaseModel):
    is_typing: bool
    room_id: str


class TypingPacket(BaseModel):
    type: PacketType = PacketType.typing
    payload: TypingPayload


class TypingNotifyPayload(BaseModel):
    room_id: str
    participant_id: str
    is_typing: bool


class TypingNotifyPacket(BaseModel):
    type: PacketType = PacketType.typing
    payload: TypingNotifyPayload


class ListMessageRequestPayload(BaseModel):
    room_id: str
    limit: int = 10
    skip: int = 0
    order: str = "desc"


class ListMessageRequestPacket(BaseModel):
    type: PacketType = PacketType.list_message_request
    payload: ListMessageRequestPayload


class ListMessageResponsePayload(MyBaseModel):
    room_id: str
    messages: list[MessageReceivePayload] | None
    total_count: int | None = None


class ListMessageResponsePacket(BaseModel):
    type: PacketType = PacketType.list_message_response
    payload: ListMessageResponsePayload
