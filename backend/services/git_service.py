# backend/services/git_service.py
import subprocess
from pathlib import Path
from services.file_service import scan_file_tree


def _run(cmd: list[str], cwd: Path) -> str:
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())
    return result.stdout.strip()


def git_log(repo_path: Path, max_count: int = 20) -> list[dict]:
    output = _run(
        ["git", "log", f"--max-count={max_count}", "--format=%H|%s|%aI|%an"],
        repo_path
    )
    entries = []
    for line in output.split('\n'):
        if not line:
            continue
        parts = line.split('|', 3)
        entries.append({
            "hash": parts[0][:7],
            "message": parts[1],
            "date": parts[2],
            "author": parts[3]
        })
    return entries


def git_status(repo_path: Path) -> dict:
    branch = _run(["git", "rev-parse", "--abbrev-ref", "HEAD"], repo_path)
    status_out = _run(["git", "status", "--porcelain"], repo_path)
    changed = [line[3:] for line in status_out.split('\n') if line] if status_out else []
    return {"branch": branch, "clean": len(changed) == 0, "changed_files": changed}


def scan_repo_tree(repo_path: Path) -> list[dict]:
    return scan_file_tree(repo_path)
