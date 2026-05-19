# backend/test_stage_service.py
import pytest
import asyncio
from pathlib import Path
from config import DATABASE_PATH
from database import init_db, get_db
from services.stage_service import get_stages, advance_stage


@pytest.fixture(autouse=True)
def clean_db():
    if DATABASE_PATH.exists():
        DATABASE_PATH.unlink()


@pytest.mark.asyncio
async def test_get_stages_returns_4_stages():
    await init_db()
    result = await get_stages()
    assert len(result["stages"]) == 4
    assert result["current_stage"] == "brainstorming"


@pytest.mark.asyncio
async def test_advance_from_brainstorming_fails_without_spec_file():
    await init_db()
    with pytest.raises(ValueError, match="spec\\.md"):
        await advance_stage(Path("/nonexistent"))


@pytest.mark.asyncio
async def test_advance_from_brainstorming_succeeds_with_spec():
    await init_db()
    import tempfile, subprocess
    with tempfile.TemporaryDirectory() as d:
        repo = Path(d)
        (repo / ".sdd").mkdir()
        (repo / ".sdd" / "spec.md").write_text("# Test Spec")
        subprocess.run(["git", "init"], cwd=repo, capture_output=True)
        result = await advance_stage(repo)
        assert result["to_stage"] == "plan"
        assert result["skill_command"] == "/writing-plans"
