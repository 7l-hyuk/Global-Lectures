from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes.auth import auth_router
from src.routes.dubbing import dubbing_router
from src.routes.video import video_router


app = FastAPI()

origins = [
    "http://localhost:3000"
]
routes = [
    auth_router,
    dubbing_router,
    video_router
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in routes:
    app.include_router(router)
