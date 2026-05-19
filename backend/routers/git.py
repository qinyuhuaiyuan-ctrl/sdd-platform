from fastapi import APIRouter
from config import PROJECT_REPO_PATH
from services.git_service import git_log, git_status, scan_repo_tree
from models import RefreshResponse

router = APIRouter(prefix="/api/git", tags=["git"])


@router.get("/log")
async def get_log():
    return git_log(PROJECT_REPO_PATH)


@router.get("/status")
async def get_status():
    return git_status(PROJECT_REPO_PATH)


@router.post("/refresh")
async def refresh() -> RefreshResponse:
    file_tree = scan_repo_tree(PROJECT_REPO_PATH)
    commits = git_log(PROJECT_REPO_PATH, max_count=10)
    return RefreshResponse(file_tree=file_tree, recent_commits=commits)
