import pytest
import asyncio
from pathlib import Path
from config import DATA_DIR, DATABASE_PATH
from database import init_db, get_db


@pytest.fixture(autouse=True)
def clean_db():
    if DATABASE_PATH.exists():
        DATABASE_PATH.unlink()


@pytest.mark.asyncio
async def test_init_db_creates_tables():
    await init_db()
    db = await get_db()
    cursor = await db.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    )
    tables = [row[0] for row in await cursor.fetchall()]
    assert 'stages' in tables
    assert 'project_stages' in tables
    await db.close()


@pytest.mark.asyncio
async def test_stages_seeded():
    await init_db()
    db = await get_db()
    cursor = await db.execute(
        "SELECT name, display_order FROM stages ORDER BY display_order"
    )
    rows = await cursor.fetchall()
    assert len(rows) == 4
    assert rows[0][0] == 'brainstorming'
    assert rows[3][0] == 'complete'
    await db.close()


@pytest.mark.asyncio
async def test_project_stages_init_active_first():
    await init_db()
    db = await get_db()
    cursor = await db.execute(
        "SELECT stage_id, status FROM project_stages WHERE stage_id = 1"
    )
    row = await cursor.fetchone()
    assert row[1] == 'active'
    await db.close()
