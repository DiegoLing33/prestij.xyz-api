#  ██╗░░░░░██╗███╗░░██╗░██████╗░░░░██████╗░██╗░░░░░░█████╗░░█████╗░██╗░░██╗
#  ██║░░░░░██║████╗░██║██╔════╝░░░░██╔══██╗██║░░░░░██╔══██╗██╔══██╗██║░██╔╝
#  ██║░░░░░██║██╔██╗██║██║░░██╗░░░░██████╦╝██║░░░░░███████║██║░░╚═╝█████═╝░
#  ██║░░░░░██║██║╚████║██║░░╚██╗░░░██╔══██╗██║░░░░░██╔══██║██║░░██╗██╔═██╗░
#  ███████╗██║██║░╚███║╚██████╔╝░░░██████╦╝███████╗██║░░██║╚█████╔╝██║░╚██╗
#  ╚══════╝╚═╝╚═╝░░╚══╝░╚═════╝░░░░╚═════╝░╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
#
#  Developed by Yakov V. Panov (C) Ling • Black 2020
#  @site http://ling.black
from hashlib import md5
from typing import List

from fastapi import APIRouter, Depends
from fastapi import File, UploadFile

from config import default_files_path
from database import get_db
from database.files.models import FileModel
from database.files.schemas import FileSchema
from wow.utils.users import BlizzardUsersUtils

router = APIRouter()


@router.post(
    "/upload",
    summary="Uploads the files"
)
async def create_upload_files(token: str, files: List[UploadFile] = File(...), db=Depends(get_db)):
    blizzard_id = BlizzardUsersUtils.id__safe(token)
    data = []
    for file in files:
        ext = file.filename.split('.')
        ext = ext[len(ext) - 1]
        temp_name = md5(file.filename.encode()).hexdigest() + '.' + ext
        with open(default_files_path + '/' + temp_name, 'wb') as f:
            cnt = await file.read()
            f.write(cnt)
        db.add(FileModel(
            user_id=blizzard_id,
            real_name=file.filename,
            file_name=temp_name,
            directory_name=''
        ))
        data.append({
            'temp_name': temp_name,
            'file_path': 'http://server.prestij.xyz/static/files/' + temp_name
        })
        db.commit()
    return data


@router.get(
    "/",
    summary='Returns user files list',
    response_model=List[FileSchema]
)
async def get_files(token: str, db=Depends(get_db)):
    blizzard_id = BlizzardUsersUtils.id__safe(token)
    return db.query(FileModel).filter(FileModel.user_id == blizzard_id).all()
