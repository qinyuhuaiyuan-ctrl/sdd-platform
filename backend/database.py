import aiosqlite
from config import DATABASE_PATH


class DatabaseConnection:
    """Async context manager and awaitable for DB connections.

    Supports two usage patterns:

      # Context manager (auto-cleanup)
      async with get_db() as db:
          await db.execute(...)

      # Direct call (caller must close)
      db = await get_db()
      await db.close()
    """

    def __init__(self):
        self._conn = None

    async def _connect(self):
        conn = await aiosqlite.connect(str(DATABASE_PATH))
        conn.row_factory = aiosqlite.Row
        await conn.execute("PRAGMA journal_mode=WAL")
        self._conn = conn
        return conn

    async def __aenter__(self):
        return await self._connect()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._conn is not None:
            await self._conn.close()
            self._conn = None

    def __await__(self):
        return self._connect().__await__()

    def __getattr__(self, name):
        if self._conn is None:
            raise RuntimeError(
                "Connection not initialised. Use 'await get_db()' or 'async with get_db()'."
            )
        return getattr(self._conn, name)


def get_db():
    return DatabaseConnection()


async def init_db():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    async with get_db() as db:
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
