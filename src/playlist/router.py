from fastapi import APIRouter, Depends, Request, WebSocket, WebSocketDisconnect
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from pytube import extract, YouTube

from src.chat.models import Message
from src.database import get_async_session, async_session_maker
from src.playlist.models import Playlist
from src.playlist.schemas import PlaylistCreate, VideoUrl

from src.settings.settings import Settings, templates
from src.settings.ws_conf import ConnectionManager

router = APIRouter(
    prefix="/playlist",
    tags=["Playlist"]
)

ws_manager = ConnectionManager()
current_video_id = '1IFnKHhBv7w'


@router.get("")
async def get_playlist(session: AsyncSession = Depends(get_async_session)):
    query = select(Playlist)
    data = await session.execute(query)
    return {"status": "success", "data": data.mappings().all()}


@router.post("")
async def add_to_playlist(playlist: PlaylistCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Playlist).values(**playlist.dict())
    data = await session.execute(stmt)
    await session.commit()
    return {"status": "201 success", "data": data.mappings().all()}


@router.get("/player")
async def get_video_page(request: Request):
    return templates.TemplateResponse(
        "playlist/player.html",
        {
            "request": request,
            "API_KEY": Settings.YOUTUBE_API_KEY,
            "video_id": '',
            "WS_URL": Settings.WS_URL,
        })


@router.post("/song_add")
async def play_new_video(url: str):
    video_id = extract.video_id(url)
    age_permission = extract.is_age_restricted(url)
    private = extract.is_private(url)
    lenth = YouTube(url)
    print("clients", ws_manager.active_connections)
    await ws_manager.broadcast(video_id)
    return {
        "message": f"New video started: {video_id}",
        "video_lenth": lenth.length,
        "data": [age_permission, private]
    }


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received data from client: {data}")
    except WebSocketDisconnect:
        await ws_manager.disconnect(websocket)