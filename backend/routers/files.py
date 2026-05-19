from pathlib import Path
from fastapi import APIRouter, HTTPException
from config import PROJECT_REPO_PATH
from models import FileContent, FileWrite
from services.file_service import read_file, write_file

router = APIRouter(prefix="/api/files", tags=["files"])


@router.get("/{path:path}")
async def get_file(path: str) -> FileContent:
    full_path = PROJECT_REPO_PATH / path
    try:
        full_path.resolve().relative_to(PROJECT_REPO_PATH.resolve())
    except ValueError:
        raise HTTPException(status_code=403, detail="Access denied")
    try:
        content = read_file(full_path)
        return FileContent(path=path, content=content)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")


@router.put("/{path:path}")
async def put_file(path: str, body: FileWrite):
    full_path = PROJECT_REPO_PATH / path
    try:
        full_path.resolve().relative_to(PROJECT_REPO_PATH.resolve())
    except ValueError:
        raise HTTPException(status_code=403, detail="Access denied")
    write_file(full_path, body.content)
    return {"ok": True}
