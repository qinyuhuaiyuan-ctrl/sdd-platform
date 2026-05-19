# backend/models.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StageInfo(BaseModel):
    id: int
    name: str
    display_order: int
    status: str  # locked | active | completed
    skill_file: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class StagesResponse(BaseModel):
    stages: list[StageInfo]
    current_stage: str

class AdvanceStageResponse(BaseModel):
    from_stage: str
    to_stage: str
    skill_command: str

class FileContent(BaseModel):
    path: str
    content: str

class FileWrite(BaseModel):
    content: str

class GitLogEntry(BaseModel):
    hash: str
    message: str
    date: str
    author: str

class GitStatus(BaseModel):
    branch: str
    clean: bool
    changed_files: list[str]

class RefreshResponse(BaseModel):
    file_tree: list[dict]
    recent_commits: list[GitLogEntry]
