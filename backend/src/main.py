from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.user import user_router
from src.routes.dub import dub_router
from src.routes.video import video_router

app = FastAPI()

origins = [
    "http://localhost:3000",  # React 개발 서버 주소
]
routers = [
    user_router,
    dub_router,
    video_router
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in routers:
    app.include_router(router)