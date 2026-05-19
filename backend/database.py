import aiosqlite
from config import DATABASE_PATH


async def get_db():
    db = await aiosqlite.connect(str(DATABASE_PATH))
    db.row_factory = aiosqlite.Row
    return db


async def init_db():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    db = await aiosqlite.connect(str(DATABASE_PATH))

    await db.executescript('''
        CREATE TABLE IF NOT EXISTS stages (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            display_order INTEGER NOT NULL UNIQUE,
            skill_file TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS project_stages (
            stage_id INTEGER PRIMARY KEY,
            status TEXT NOT NULL DEFAULT 'locked',
            started_at TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY (stage_id) REFERENCES stages(id)
        );
    ''')

    await db.executemany(
        'INSERT OR IGNORE INTO stages (id, name, display_order, skill_file) VALUES (?, ?, ?, ?)',
        [
            (1, 'brainstorming', 1, 'skills/brainstorming/SKILL.md'),
            (2, 'plan', 2, 'skills/writing-plans/SKILL.md'),
            (3, 'implement', 3, 'skills/subagent-driven-development/SKILL.md'),
            (4, 'complete', 4, 'skills/finishing-a-development-branch/SKILL.md'),
        ]
    )

    await db.executemany(
        'INSERT OR IGNORE INTO project_stages (stage_id, status) VALUES (?, ?)',
        [(1, 'active'), (2, 'locked'), (3, 'locked'), (4, 'locked')]
    )

    await db.commit()
    await db.close()
