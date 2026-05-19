from pathlib import Path
from fastapi import APIRouter, HTTPException
from config import TEMPLATES_DIR
from models import FileContent, FileWrite
from services.file_service import read_file, write_file, scan_file_tree

router = APIRouter(prefix="/api/templates", tags=["templates"])


@router.get("")
async def list_templates():
    if not TEMPLATES_DIR.exists():
        return {"templates": []}
    items = []
    for f in TEMPLATES_DIR.rglob("*"):
        if f.is_file():
            items.append(str(f.relative_to(TEMPLATES_DIR)))
    return {"templates": items}


@router.get("/{type}")
async def get_template(type: str) -> FileContent:
    path = TEMPLATES_DIR / type
    try:
        content = read_file(path)
        return FileContent(path=type, content=content)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Template not found")


@router.put("/{type}")
async def put_template(type: str, body: FileWrite):
    path = TEMPLATES_DIR / type
    write_file(path, body.content)
    return {"ok": True}
