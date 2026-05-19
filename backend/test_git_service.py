# backend/test_git_service.py
import pytest
import tempfile
import subprocess
from pathlib import Path
from services.git_service import git_log, git_status, scan_repo_tree

@pytest.fixture
def temp_git_repo():
    with tempfile.TemporaryDirectory() as d:
        repo = Path(d)
        subprocess.run(["git", "init"], cwd=repo, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=repo, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, capture_output=True)
        (repo / "README.md").write_text("# test")
        subprocess.run(["git", "add", "."], cwd=repo, capture_output=True)
        subprocess.run(["git", "commit", "-m", "initial"], cwd=repo, capture_output=True)
        yield repo

def test_git_log_returns_commits(temp_git_repo):
    log = git_log(temp_git_repo)
    assert len(log) > 0
    assert log[0]["message"] == "initial"

def test_git_status_clean(temp_git_repo):
    status = git_status(temp_git_repo)
    assert status["clean"] is True

def test_git_status_dirty(temp_git_repo):
    (temp_git_repo / "new.txt").write_text("dirty")
    status = git_status(temp_git_repo)
    assert status["clean"] is False

def test_scan_repo_tree(temp_git_repo):
    tree = scan_repo_tree(temp_git_repo)
    names = [item["name"] for item in tree]
    assert "README.md" in names
