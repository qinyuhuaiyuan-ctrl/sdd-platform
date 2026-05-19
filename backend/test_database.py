import pytest
import asyncio
from pathlib import Path
from config import DATA_DIR, DATABASE_PATH
from database import init_db, get_db


@pytest.fixture(autouse=True)
def clean_db(monkeypatch, tmp_path):
    """Override DATABASE_PATH with an isolated temp file per test."""
    db_path = tmp_path / "test.db"
    monkeypatch.setattr("config.DATABASE_PATH", db_path)


@pytest.mark.asyncio
async def test_init_db_creates_tables():
    await init_db()
    async with get_db() as db:
        cursor = await db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        tables = [row[0] for row in await cursor.fetchall()]
    assert 'stages' in tables
    assert 'project_stages' in tables


@pytest.mark.asyncio
async def test_stages_seeded():
    await init_db()
    async with get_db() as db:
        cursor = await db.execute(
            "SELECT name, display_order FROM stages ORDER BY display_order"
        )
        rows = await cursor.fetchall()
    assert len(rows) == 4
    assert rows[0][0] == 'brainstorming'
    assert rows[3][0] == 'complete'


@pytest.mark.asyncio
async def test_project_stages_init_active_first():
    await init_db()
    async with get_db() as db:
        cursor = await db.execute(
            "SELECT stage_id, status FROM project_stages ORDER BY stage_id"
        )
        rows = await cursor.fetchall()
    assert len(rows) == 4
    assert rows[0][1] == 'active'
    for row in rows[1:]:
        assert row[1] == 'locked', f"Expected stage {row[0]} to be 'locked' but got '{row[1]}'"
