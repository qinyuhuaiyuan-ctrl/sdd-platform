from pathlib import Path
from fastapi import APIRouter, HTTPException
from config import SKILLS_DIR
from models import FileContent, FileWrite
from services.file_service import read_file, write_file

router = APIRouter(prefix="/api/skills", tags=["skills"])

SKILL_STAGES = ["brainstorming", "writing-plans", "subagent-driven-development", "finishing-a-development-branch"]


@router.get("")
async def list_skills():
    skills = []
    for name in SKILL_STAGES:
        skill_dir = SKILLS_DIR / name
        files = []
        if skill_dir.exists():
            for f in skill_dir.rglob("*"):
                if f.is_file():
                    files.append(str(f.relative_to(SKILLS_DIR)))
        skills.append({"name": name, "files": files})
    return {"skills": skills}


@router.get("/{stage}/{path:path}")
async def get_skill_file(stage: str, path: str) -> FileContent:
    full_path = (SKILLS_DIR / stage / path).resolve()
    try:
        full_path.relative_to((SKILLS_DIR / stage).resolve())
    except ValueError:
        raise HTTPException(status_code=403, detail="Access denied")
    try:
        content = read_file(full_path)
        return FileContent(path=str(full_path.relative_to(SKILLS_DIR)), content=content)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")


@router.put("/{stage}/{path:path}")
async def put_skill_file(stage: str, path: str, body: FileWrite):
    full_path = (SKILLS_DIR / stage / path).resolve()
    try:
        full_path.relative_to((SKILLS_DIR / stage).resolve())
    except ValueError:
        raise HTTPException(status_code=403, detail="Access denied")
    write_file(full_path, body.content)
    return {"ok": True}
