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
from router import character, guild, mythic, btusers, files, posts
from database.database import engine, Base
from middleware import use_content_type
from modules.statics.routes import router as statics_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Престиж WoW API",
    description="API Проекта гильдии World Of Warcraft \"Престиж\"",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Пользователи",
            "description": "API методы связанные с пользователями в обвязке BlizzardAPI"
        },
        {
            "name": "Гильдия",
            "description": "API методы для получения актуальной информации о гильдии"
        },
        {
            "name": "Мифик",
            "description": "API методы для получения информации о прохождении Мифик+ подземелий"
        },
        {
            "name": "Персонажи",
            "description": "API методы для получения участников гильдии"
        },
        {
            "name": "Записи",
            "description": "Функциональная часть приложения - записи"
        },
        {
            "name": "Файлы",
            "description": "Функциональная часть приложения - файлы"
        },
        {
            "name": "Статики",
            "description": "Методы для получения информации про игровые статики"
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
    tags=['Персонажи']
)

app.include_router(
    guild.router,
    prefix="/guild",
    tags=['Гильдия']
)
app.include_router(
    mythic.router,
    prefix="/mythic",
    tags=['Мифик']
)
app.include_router(
    posts.router,
    prefix="/posts",
    tags=['Записи']
)
app.include_router(
    btusers.router,
    prefix="/users",
    tags=['Пользователи']
)
app.include_router(
    files.router,
    prefix="/files",
    tags=['Файлы']
)
app.include_router(
    statics_router,
    prefix="/statics",
    tags=['Статики']
)

app.mount("/static", StaticFiles(directory="static"))

# Entry point
if __name__ == "__main__":
    uvicorn.run("main:app", host=app_server, port=app_port, reload=True)
