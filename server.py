#  ██╗░░░░░██╗███╗░░██╗░██████╗░░░░██████╗░██╗░░░░░░█████╗░░█████╗░██╗░░██╗
#  ██║░░░░░██║████╗░██║██╔════╝░░░░██╔══██╗██║░░░░░██╔══██╗██╔══██╗██║░██╔╝
#  ██║░░░░░██║██╔██╗██║██║░░██╗░░░░██████╦╝██║░░░░░███████║██║░░╚═╝█████═╝░
#  ██║░░░░░██║██║╚████║██║░░╚██╗░░░██╔══██╗██║░░░░░██╔══██║██║░░██╗██╔═██╗░
#  ███████╗██║██║░╚███║╚██████╔╝░░░██████╦╝███████╗██║░░██║╚█████╔╝██║░╚██╗
#  ╚══════╝╚═╝╚═╝░░╚══╝░╚═════╝░░░░╚═════╝░╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
#
#  Developed by Yakov V. Panov (C) Ling • Black 2020
#  @site http://ling.black

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from config import app_server, app_port
from router import character, guild, mythic, btusers, files
from router import posts
from database.database import engine, Base
from middleware import use_content_type

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Ling API Service",
    description="This is example of the Ling API Service",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "users",
            "description": "User API methods"
        },
        {
            "name": "groups",
            "description": "User role groups API methods"
        },
        {
            "name": "auth",
            "description": "Authorization API methods"
        }
    ]
)
# Middlewares
use_content_type(app)

origins = [
    "http://localhost:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    character.router,
    prefix="/characters",
    tags=['wow']
)

app.include_router(
    guild.router,
    prefix="/guild",
    tags=['wow']
)
app.include_router(
    mythic.router,
    prefix="/mythic",
    tags=['wow']
)
app.include_router(
    posts.router,
    prefix="/posts",
    tags=['wow']
)
app.include_router(
    btusers.router,
    prefix="/users",
    tags=['wow']
)
app.include_router(
    files.router,
    prefix="/files",
    tags=['wow']
)

app.mount("/static", StaticFiles(directory="static"))

# Entry point
if __name__ == "__main__":
    uvicorn.run("main:app", host=app_server, port=app_port, reload=True)
